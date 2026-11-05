# R1: sleepy music box over a warm low pad, 70 bpm, E major. Plus soft SFX on key moments.
import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/7122b9f6-ef9c-5a65-8b0a-af50e22d1cd8/scratchpad/clari5')
from au import *
D=21.0; B=60/70; L=np.zeros(int(SR*(D+3))); Rr=np.zeros_like(L)
def mbox(m,dur=2.6,v=1.0):  # comb tine: inharmonic partials, quick decay, tiny click
    t=T(dur); f=hz(m)
    s=np.sin(2*np.pi*f*t)*np.exp(-t*2.2)+0.42*np.sin(2*np.pi*f*2.76*t)*np.exp(-t*6)+0.16*np.sin(2*np.pi*f*5.4*t)*np.exp(-t*11)
    s+=0.08*np.sin(2*np.pi*f*8.9*t)*np.exp(-t*30)
    return v*s*np.minimum(1,t/0.0015)*0.32
def pad(ms,dur):
    t=T(dur); s=np.zeros_like(t)
    for m in ms:
        f=hz(m)
        for dt in (-0.09,0,0.08):
            ff=f*2**(dt/12); s+=np.sin(2*np.pi*ff*t+dt*40)+0.3*np.sin(2*np.pi*2*ff*t)+0.1*np.sin(2*np.pi*3*ff*t)
    s*=0.82+0.18*np.sin(2*np.pi*0.23*t)
    return lp(s,0.06)*env(dur,1.4,1.6)/len(ms)/3
chords=[[40,52,56,59,63],[37,49,52,56,59],[33,45,49,52,56],[35,47,51,54,57]]   # Emaj7 C#m7 Amaj7 B(add)
mel=[[76,71,68,71,75,71],[73,68,64,68,71,68],[73,69,64,69,76,73],[75,71,66,71,78,75]]
bar=4*B; t0=0.25
for i in range(7):
    ch=chords[i%4]; tb=t0+i*bar
    p=pad(ch,bar+2.2); add(L,p,tb,0.55); add(Rr,np.roll(p,300),tb,0.55)
    for k,m in enumerate(mel[i%4]):
        if i==0 and k<1: continue
        nt=tb+k*bar/6*1.0+ (0.025 if k%2 else 0)
        if nt>D-1.5: continue
        x=mbox(m,2.8,0.9 if k==0 else 0.62)
        pan=0.5+0.3*np.sin(k*1.7+i)
        add(L,x,nt,1.2*(1-pan)+0.4); add(Rr,x,nt,1.2*pan+0.4)
# soft low heartbeat-ish pulse on beats 1 and 3 from bar 2 (felt kick)
def felt(d=0.5):
    t=T(d); f=55*np.exp(-t*8)+42
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*9)*0.5
for i in range(2,24,2):
    tt=t0+i*B
    if tt<D-1.8: add(L,felt(),tt,0.5); add(Rr,felt(),tt,0.5)
# SFX
def whoosh(d=1.0,seed=3):
    n=noise(d,seed); t=T(d); e=np.sin(np.pi*np.minimum(1,t/d))**2
    return (0.5*lp(n,0.03)+0.5*lp(n,0.09)*np.sin(np.pi*t/d))*e*0.9
def tick(seed=5):
    return hp(noise(0.03,seed),0.5)*env(0.03,0.0005,dec=180)*0.5
def chime(m,v=1):
    t=T(3); f=hz(m); return v*(np.sin(2*np.pi*f*t)*np.exp(-t*1.4)+0.3*np.sin(2*np.pi*f*3.01*t)*np.exp(-t*3)+0.2*np.sin(2*np.pi*f*4.2*t)*np.exp(-t*5))*0.22
def plink(m,seed):
    t=T(0.4); f=hz(m)*(1+0.6*np.exp(-t*40)); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*14)*0.22
for tm in (3.4,7.8,16.6,18.6): add(L,whoosh(1.1,int(tm*10)),tm-0.35,0.5); add(Rr,whoosh(1.1,int(tm*10)+1),tm-0.35,0.5)
for tm in (1.3,1.95,2.6): add(L,tick(int(tm*100)),tm+0.2,1); add(Rr,tick(int(tm*100)),tm+0.2,1)
sw=T(1.4); swell=np.sin(2*np.pi*hz(64)*sw)*np.sin(np.pi*sw/1.4)**2*0.18; add(L,swell,2.7); add(Rr,swell,2.72)
for k,tm in enumerate([5.75,6.05,6.4,6.8,7.1]): add(L if k%2 else Rr,plink(88+k%3*2,k),tm,1); 
for k,tm in enumerate([8.35,10.05,11.75,13.45,15.15]): x=chime([83,80,78,76,75][k]); add(L,x,tm,0.8); add(Rr,x,tm+0.01,0.8)
x=chime(76,1.3)+chime(83,0.8); add(L,x,19.1); add(Rr,x,19.11)
L=L[:int(SR*D)]; Rr=Rr[:int(SR*D)]
L=reverb(L,3.0,0.34,1); Rr=reverb(Rr,3.0,0.34,2)
f=np.minimum(1,T(D)/0.4)*np.minimum(1,(D-T(D))/1.6)
write('audio/bed.wav',stereo(L*f,Rr*f))
