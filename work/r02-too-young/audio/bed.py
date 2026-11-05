# R2: tight minimal pulse, 112 bpm, D minor. Karplus-Strong plucked bass, rim clicks, closed shaker ticks.
import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/7122b9f6-ef9c-5a65-8b0a-af50e22d1cd8/scratchpad/clari5')
from au import *
D=32.2; B=60/112; N=int(SR*(D+2))
L=np.zeros(N); R=np.zeros(N); SL=np.zeros(N); SR_=np.zeros(N)
rng=np.random.default_rng(112)
def pluck(m,dur=0.5,bright=0.5):
    f=hz(m); p=int(SR/f); buf=rng.uniform(-1,1,p); buf=lp(buf,bright); out=np.zeros(int(SR*dur))
    for i in range(len(out)):
        out[i]=buf[i%p]; buf[i%p]=0.5*(buf[i%p]+buf[(i+1)%p])*0.996
    return out*env(dur,0.002,0.05)
cache={}
def pl(m,d=0.42):
    k=(m,d)
    if k not in cache: cache[k]=pluck(m,d,0.35)
    return cache[k]
def rim(seed):
    t=T(0.06); n=np.random.default_rng(seed).normal(0,1,len(t))
    tone=np.sin(2*np.pi*1650*t)*np.exp(-t*90)+0.6*np.sin(2*np.pi*870*t)*np.exp(-t*70)
    return (hp(n,0.6)*np.exp(-t*120)*0.5+tone)*0.32
def tick(seed): t=T(0.025); return hp(np.random.default_rng(seed).normal(0,1,len(t)),0.75)*np.exp(-t*260)*0.16
def kick():
    t=T(0.35); f=48+90*np.exp(-t*30); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*10)*0.8
roots=[38,38,41,41,36,36,43,41]   # D D F F C C G F, two beats each pattern
pat=[0,None,0,12,None,0,7,None]  # 8th notes per beat pair (offsets)
nb=int(D/B)+1
for b in range(nb):
    tb=b*B; bar=b//4; root=roots[(b//2)%8]
    if tb>D-0.3: break
    end=tb>29.4
    if not end:
        for k in range(2):
            o=pat[(b%2)*4+k*2] if (b%2)*4+k*2<8 else None
            if o is None: continue
            x=pl(root+o)
            add(L,x,tb+k*B/2,0.9); add(R,x,tb+k*B/2+0.004,0.9)
        if b%4 in (1,3): r=rim(b); add(L,r,tb,0.7); add(R,r,tb,0.9)
        if b%4==0 and b>=4: kk=kick(); add(L,kk,tb,0.6); add(R,kk,tb,0.6)
        for s in range(4):
            if b>=8 and s in (1,3): x=tick(b*4+s); add(L,x,tb+s*B/4,0.8); add(R,x,tb+s*B/4,1.0)
# end: held Dm9 pluck chord + low D
for i,m in enumerate([38,50,53,57,60,64]):
    x=pluck(m,2.6,0.5)*0.6; add(L,x,29.9+i*0.03); add(R,x,29.9+i*0.035)
L=L[:int(SR*D)]; R=R[:int(SR*D)]
# shape: quieter under voice is done in the mix; lift after the voice ends
g=np.ones(len(L)); tt=T(D); g=np.where(tt>29.2,1+2.2*np.minimum(1,(tt-29.2)/0.4),1)
g*=np.minimum(1,(D-tt)/1.2)
L=reverb(L,1.2,0.14,3)*g; R=reverb(R,1.2,0.14,4)*g
write('audio/bed.wav',stereo(L,R))
# SFX stem
def thump(f0=60): t=T(0.5); f=f0+140*np.exp(-t*25); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*8)
def swish(d,seed): n=noise(d,seed); t=T(d); return hp(n,0.3)*(np.sin(np.pi*t/d)**3)*0.4
for tm in (3.3,5.86,13.36,17.84): x=thump(); add(SL,x,tm+0.1); add(SR_,x,tm+0.1)
for tm in (5.7,13.2,22.36,29.2): x=swish(0.4,int(tm*10)); add(SL,x,tm-0.05,0.8); add(SR_,np.roll(x,200),tm-0.05,0.8)
x=swish(0.25,77)*1.2; add(SL,x,23.9); add(SR_,x,23.9)
for tm in (21.35,21.75): t=T(0.3); x=np.sin(2*np.pi*880*t)*np.exp(-t*18)*0.3; add(SL,x,tm); add(SR_,x,tm)
t=T(1.5); x=(np.sin(2*np.pi*hz(74)*t)+0.4*np.sin(2*np.pi*hz(81)*t))*np.exp(-t*2.5)*0.35; add(SL,x,30.0); add(SR_,x,30.0)
write('audio/sfx.wav',stereo(SL[:int(SR*D)],SR_[:int(SR*D)]))
