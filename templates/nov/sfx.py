import numpy as np, wave, sys
SR=48000
def tick(dur=0.035, f=2600, amp=0.25):
    t=np.arange(int(SR*dur))/SR
    env=np.exp(-t*140)
    n=np.random.default_rng(1).normal(0,1,len(t))
    return amp*env*(0.6*np.sin(2*np.pi*f*t)+0.4*np.sin(2*np.pi*f*1.5*t)+0.15*n)
def whoosh(dur=0.9, amp=0.18, seed=2):
    n=np.random.default_rng(seed).normal(0,1,int(SR*dur))
    # crude band filter via moving averages
    k=24; lp=np.convolve(n,np.ones(k)/k,'same'); hp=lp-np.convolve(lp,np.ones(240)/240,'same')
    t=np.linspace(0,1,len(n)); env=np.sin(np.pi*t)**2
    return amp*hp*env/np.max(np.abs(hp))
def chime(dur=2.4, amp=0.22):
    t=np.arange(int(SR*dur))/SR
    s=sum(a*np.sin(2*np.pi*f*t)*np.exp(-t*d) for f,a,d in [(1046.5,1,2.2),(1568,0.5,3),(2093,0.25,4.5),(523.25,0.35,1.6)])
    att=np.minimum(1,t/0.005)
    return amp*s*att/2
def swell(dur=1.6, amp=0.12):
    t=np.arange(int(SR*dur))/SR
    env=(t/dur)**2*np.exp(-(t/dur)*0.5)
    s=sum(np.sin(2*np.pi*f*t) for f in (110,164.8,220))
    return amp*env*s/3
def place(track, clip, at):
    i=int(at*SR); track[i:i+len(clip)]+=clip[:max(0,len(track)-i)]
def save(name, tr):
    tr=np.clip(tr,-1,1); st=np.stack([tr,tr],1)
    with wave.open(name,'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
which=sys.argv[1]
if which=='day':
    HOOK,BEAT,N=2.6,2.7,6; END=HOOK+N*BEAT; total=END+6.2
    tr=np.zeros(int(SR*total))
    place(tr, swell(), HOOK-1.4)
    for i in range(N):
        a=HOOK+i*BEAT
        for k in range(9):  # clock rolling ticks, slowing down
            place(tr, tick(amp=0.16*(1-k/12)), a+0.03+k*0.085*(1+k*0.08))
        place(tr, whoosh(0.7,0.06,seed=i+3), a-0.25)
    place(tr, chime(), END+0.45)
    save('day-sfx.wav', tr)
else:
    HOOK=3.0; starts=[3.0,9.4,15.4]; PDF=20.4; END=PDF+3.4; total=END+5.0
    tr=np.zeros(int(SR*total))
    place(tr, whoosh(0.9,0.10,seed=7), HOOK-0.5)
    for s in starts[1:]: place(tr, whoosh(0.6,0.05,seed=int(s)), s-0.3)
    place(tr, whoosh(1.0,0.12,seed=11), PDF-0.1)
    place(tr, chime(), END+0.55)
    save('page-sfx.wav', tr)
