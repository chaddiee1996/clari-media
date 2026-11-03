import numpy as np, wave, sys
SR=48000
rng=np.random.default_rng(5)
def note(m): return 440*2**((m-69)/12)
def pad(freqs, dur):
    t=np.arange(int(SR*dur))/SR; s=np.zeros_like(t)
    for f in freqs:
        for det in (-0.12,0.0,0.11):
            ff=f*2**(det/12)
            s+=np.sin(2*np.pi*ff*t+rng.uniform(0,6))*0.6+0.18*np.sin(2*np.pi*2*ff*t)+0.06*np.sin(2*np.pi*3*ff*t)
    a=np.minimum(1,t/1.2); r=np.minimum(1,(dur-t)/1.0)
    return s*a*r/ (len(freqs)*3)
def piano(f, dur=3.0, vel=1.0):
    t=np.arange(int(SR*dur))/SR
    s=sum(a*np.sin(2*np.pi*f*k*t*(1+0.0004*k*k))*np.exp(-t*(1.6+k*0.9)) for k,a in [(1,1),(2,.45),(3,.18),(4,.08),(5,.04)])
    att=np.minimum(1,t/0.004)
    return vel*s*att*0.35
def reverb(x, secs=2.6, mix=0.32):
    n=int(SR*secs); ir=rng.normal(0,1,n)*np.exp(-np.arange(n)/SR*3.2); ir[:int(SR*0.02)]=0
    ir/=np.sqrt(np.sum(ir**2))
    y=np.fft.irfft(np.fft.rfft(x,len(x)+n)*np.fft.rfft(ir,len(x)+n))[:len(x)]
    return (1-mix)*x+mix*y*0.9
total=float(sys.argv[2]); bar=60/68*4
prog=[[53,57,60,64],[57,60,64,67],[50,57,60,65],[46,53,57,62]]  # Fmaj7 Am7 Dm(add) Bbmaj9-ish
L=np.zeros(int(SR*(total+3)))
t=0.0; i=0
mel=[[72,69,67,64],[72,71,67,64],[69,65,64,62],[65,64,62,60]]
while t<total:
    ch=prog[i%4]
    p=pad([note(m) for m in ch]+[note(ch[0]-12)], bar+1.2)
    s=int(t*SR); L[s:s+len(p)]+=p[:len(L)-s]*0.5
    # arpeggio of soft piano notes
    for k,m in enumerate(mel[i%4]):
        if i==0 and k<2: continue
        nt=t+k*bar/4+ (0.02 if k%2 else 0)
        pn=piano(note(m), 3.2, 0.75 if k==0 else 0.55)
        s2=int(nt*SR)
        if s2<len(L): L[s2:s2+len(pn)]+=pn[:len(L)-s2]
    t+=bar; i+=1
L=L[:int(SR*total)]
fade=np.minimum(1,np.arange(len(L))/(SR*1.5))*np.minimum(1,(len(L)-np.arange(len(L)))/(SR*2.5))
L=reverb(L)*fade
L=L/np.max(np.abs(L))*0.5
Rch=np.roll(L,int(SR*0.011))
st=np.stack([L,Rch],1)
with wave.open(sys.argv[1],'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
