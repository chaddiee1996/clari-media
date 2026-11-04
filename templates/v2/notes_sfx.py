import numpy as np, wave
SR=48000; T=35.1
tr=np.zeros(int(SR*T)); rng=np.random.default_rng(3)
def place(c,at):
    i=int(at*SR); tr[i:i+len(c)]+=c[:max(0,len(tr)-i)]
def key(amp=.12):
    n=int(SR*.03); t=np.arange(n)/SR
    return amp*np.exp(-t*220)*(rng.normal(0,1,n)*.6+np.sin(2*np.pi*1800*t))
def scratch(dur=.5, amp=.05):
    n=int(SR*dur); x=rng.normal(0,1,n); x=x-np.convolve(x,np.ones(30)/30,'same')
    env=np.sin(np.linspace(0,np.pi,n))**.6*(0.6+0.4*np.sin(np.linspace(0,40,n)))
    return amp*x*env
def tick(amp=.06):
    n=int(SR*.02); t=np.arange(n)/SR; return amp*np.exp(-t*300)*np.sin(2*np.pi*2400*t)
# typing on "mid-sentence"
t0=9.96+12/30
for k in range(7): place(key(), t0+k*2.2/30)
# counter ticks
for k in range(18): place(tick(.04), 3.5+k*0.14)
# red pen underline
place(scratch(.6,.06), 21.99+26/30)
# handwriting
for at in (25.73, 26.53, 27.65): place(scratch(.9,.035), at)
tr=np.clip(tr,-1,1); st=np.stack([tr,tr],1)
with wave.open('notes-sfx.wav','wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st*32767).astype('<i2').tobytes())
