# R4: warm, steady felt piano + soft brushes, 92 bpm, A-flat major.
import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/7122b9f6-ef9c-5a65-8b0a-af50e22d1cd8/scratchpad/clari5')
from au import *
D=29.0; B=60/92; N=int(SR*(D+3)); L=np.zeros(N); R=np.zeros(N); SL=np.zeros(N); SRR=np.zeros(N)
rng=np.random.default_rng(92)
def felt(m,v=1.0,dur=2.4):
    t=T(dur); f=hz(m); s=np.zeros_like(t)
    for k,a in [(1,1),(2,0.38),(3,0.12),(4,0.05)]:
        s+=a*np.sin(2*np.pi*f*k*t*(1+0.0003*k*k))*np.exp(-t*(1.1+0.8*k))
    s=lp(s,0.25)
    thump=lp(rng.normal(0,1,len(t)),0.05)*np.exp(-t*60)*0.25
    return v*(s+thump)*np.minimum(1,t/0.008)*0.32
def brush_swish(d):
    n=rng.normal(0,1,int(SR*d)); t=T(d); e=np.sin(np.pi*t/d)**1.5
    return hp(lp(n,0.25),0.05)*e*0.05
def brush_tap():
    t=T(0.08); n=rng.normal(0,1,len(t)); return hp(lp(n,0.4),0.1)*np.exp(-t*60)*0.09
def bass(m,d):
    t=T(d); f=hz(m); return np.sin(2*np.pi*f*t)*(1-np.exp(-t*60))*np.exp(-t*0.9)*env(d,0.01,0.2)*0.3
# Abmaj9 - Fm7 - Dbmaj7 - Eb6
prog=[(44,[56,60,63,67,70]),(41,[56,60,63,65,68]),(37,[56,60,61,65,68]),(39,[55,58,63,67,70])]
mel=[[75,72,70],[72,68,67],[68,65,63],[70,67,70]]
bar=4*B
for bi in range(int(D/bar)+1):
    tb=bi*bar; root,ch=prog[bi%4]
    if tb>D-1: break
    add(L,bass(root,bar+0.3),tb,1); add(R,bass(root,bar+0.3),tb,1)
    # broken chord on 8ths, gentle
    for k in range(8):
        tt=tb+k*B/2
        if tt>D-2.5: break
        m=ch[[0,2,1,3,2,4,3,2][k]]; x=felt(m,0.55 if k%2 else 0.7)
        add(L,x,tt,0.9); add(R,x,tt+0.006,0.8)
    for k,m in enumerate(mel[bi%4]):
        tt=tb+[0,1.5,3][k]*B
        if tt<D-2.5 and bi>=1: x=felt(m+12,0.5,3); add(L,x,tt,0.6); add(R,x,tt,0.75)
    for q in range(4):
        tt=tb+q*B
        if tt>D-2.5: break
        if q in (1,3): add(L,brush_swish(B*0.9),tt-0.05,1); add(R,brush_swish(B*0.9),tt-0.03,1)
        for s in range(2): x=brush_tap(); add(L,x,tt+s*B/2+(0.02 if s else 0),0.8); add(R,x,tt+s*B/2+(0.02 if s else 0),1)
# end chord
for i,m in enumerate([44,56,60,63,67,72]): x=felt(m,0.7,4); add(L,x,26.2+i*0.04); add(R,x,26.2+i*0.045)
L=L[:int(SR*D)]; R=R[:int(SR*D)]
tt=T(D); g=np.where(tt>26.0,1+1.6*np.minimum(1,(tt-26.0)/0.5),1)*np.minimum(1,(D-tt)/1.5)
L=reverb(L,2.2,0.25,7)*g; R=reverb(R,2.2,0.25,8)*g
write('audio/bed.wav',stereo(L,R))
# SFX
def ping(m,v=1): t=T(1.2); f=hz(m); return v*(np.sin(2*np.pi*f*t)+0.25*np.sin(2*np.pi*2*f*t))*np.exp(-t*4)*0.4
def woosh(d,seed): n=noise(d,seed); t=T(d); return lp(n,0.08)*np.sin(np.pi*t/d)**2*0.7
def key(seed): t=T(0.03); return hp(np.random.default_rng(seed).normal(0,1,len(t)),0.6)*np.exp(-t*200)*0.22
for tm,m in [(4.85,80),(12.45,82),(18.0,84),(24.3,87)]: x=ping(m); add(SL,x,tm); add(SRR,x,tm)
for tm in (4.1,11.75,17.3,23.5): x=woosh(0.9,int(tm*7)); add(SL,x,tm-0.1); add(SRR,np.roll(x,300),tm-0.1)
x=ping(91,0.6); add(SL,x,8.05); add(SRR,x,8.05)
for k,tm in enumerate(np.concatenate([np.arange(20.2,21.9,0.055),np.arange(22.3,23.3,0.055)])): add(SL if k%2 else SRR,key(k),tm,1)
for i,tm in enumerate([26.0,26.55,27.1]): x=ping(80+i*4,0.5); add(SL,x,tm); add(SRR,x,tm)
write('audio/sfx.wav',stereo(SL[:int(SR*D)],SRR[:int(SR*D)]))
