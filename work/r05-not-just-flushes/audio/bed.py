# R5: lo-fi drum loop + warm tape-saturated chords, 86 bpm, G minor. Print thud on every word, roller swish on wipes.
import sys; sys.path.insert(0,'/tmp/claude-0/-home-claude/7122b9f6-ef9c-5a65-8b0a-af50e22d1cd8/scratchpad/clari5')
from au import *
D=25.5; B=60/86; b=lambda n:0.35+n*B; N=int(SR*(D+3)); L=np.zeros(N); R=np.zeros(N)
rng=np.random.default_rng(86)
def keys(ms,dur):   # Rhodes-ish: sine + bell partial, tremolo, tape wow, saturation
    t=T(dur); s=np.zeros_like(t); wow=1+0.0035*np.sin(2*np.pi*0.55*t)+0.0015*np.sin(2*np.pi*3.1*t)
    ph=np.cumsum(wow)/SR
    for m in ms:
        f=hz(m); s+=np.sin(2*np.pi*f*ph)*np.exp(-t*0.7)+0.22*np.sin(2*np.pi*f*7.0*ph)*np.exp(-t*6)+0.12*np.sin(2*np.pi*2*f*ph)*np.exp(-t*1.5)
    s*=(1+0.12*np.sin(2*np.pi*4.3*t))
    s=np.tanh(1.6*s/len(ms))*env(dur,0.01,0.4)
    return lp(s,0.2)*0.5
def kick(): t=T(0.4); f=45+80*np.exp(-t*28); return np.tanh(2*np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*7))*0.75
def snare(seed):
    t=T(0.3); n=np.random.default_rng(seed).normal(0,1,len(t)); return (lp(hp(n,0.1),0.35)*np.exp(-t*16)*0.55+np.sin(2*np.pi*190*t)*np.exp(-t*25)*0.3)
def hat(seed,o=False): t=T(0.12 if o else 0.04); return hp(np.random.default_rng(seed).normal(0,1,len(t)),0.7)*np.exp(-t*(30 if o else 140))*0.12
def bass(m,d): t=T(d); f=hz(m); return np.tanh(1.5*np.sin(2*np.pi*f*t))*np.exp(-t*1.6)*env(d,0.006,0.1)*0.42
prog=[(43,[58,62,65,69]),(39,[58,62,63,67]),(36,[58,60,63,67]),(38,[57,60,62,66])]   # Gm9 Ebmaj7 Cm9 D7sus-ish
bar=4*B; t0=0.35
for bi in range(int(D/bar)+2):
    tb=t0+bi*bar; root,ch=prog[bi%4]
    if tb>D-0.5: break
    if tb<D-2.6:
        x=keys(ch,bar+0.4); add(L,x,tb-0.02,1); add(R,np.roll(x,240),tb-0.02,1)
        add(L,bass(root,B*1.8),tb,1); add(R,bass(root,B*1.8),tb,1); add(L,bass(root+7 if bi%2 else root,B*1.2),tb+2.5*B,0.8); add(R,bass(root+7 if bi%2 else root,B*1.2),tb+2.5*B,0.8)
    for q in range(4):
        tt=tb+q*B
        if tt>D-2.6: break
        if q==0 or (q==2 and bi%2==1): add(L,kick(),tt); add(R,kick(),tt)
        if q==2 and bi%2==0: add(L,kick(),tt+B*0.5,0.7); add(R,kick(),tt+B*0.5,0.7)
        if q in (1,3): s_=snare(bi*4+q); add(L,s_,tt+0.012,1); add(R,s_,tt+0.012,0.9)
        for e in range(2):
            sw=0.09*B if e else 0; add(L,hat(bi*8+q*2+e,o=(q==3 and e==1)),tt+e*B/2+sw,0.8); add(R,hat(bi*8+q*2+e+50),tt+e*B/2+sw,1)
# end: held Gm9 with tape stop feel
x=keys([43,55,58,62,65,69],3.2); add(L,x,b(32.6)); add(R,np.roll(x,240),b(32.6))
# vinyl crackle bed
cr=np.zeros(N); idx=rng.integers(0,N,int(D*35)); cr[idx]=rng.normal(0,1,len(idx))*0.25; cr=hp(cr,0.4)+hp(rng.normal(0,0.004,N),0.6)
L+=cr; R+=np.roll(cr,500)
# print thud on every word stamp, roller swish on wipes
def thud(seed): t=T(0.18); n=np.random.default_rng(seed).normal(0,1,len(t)); return (lp(n,0.12)*np.exp(-t*35)*0.9+np.sin(2*np.pi*95*t)*np.exp(-t*30)*0.6)*0.6
def roller(seed): d=1.0; t=T(d); n=np.random.default_rng(seed).normal(0,1,len(t)); g=np.sin(np.pi*t/d)**2; return (lp(n,0.05)*1.5+hp(lp(n,0.3),0.1)*0.3*(1+np.sin(2*np.pi*22*t)))*g*0.5
stamps=[b(0),b(1),b(2),b(3),b(5.3)]+[b(6+i) for i in range(12)]+[b(19.5),b(20.3),b(21.1),b(23.5),b(24.3),b(25.1),b(25.9),b(28.5),b(29.4),b(32.0),b(32.6)]
for i,tm in enumerate(stamps): x=thud(i); add(L,x,tm,0.9); add(R,x,tm+0.003,0.9)
for tm in (b(5),b(19),b(23),b(28),b(31.5)): x=roller(int(tm*10)); add(L,x,tm-0.5,1); add(R,np.roll(x,400),tm-0.5,1)
L=L[:int(SR*D)]; R=R[:int(SR*D)]
f=np.minimum(1,T(D)/0.08)*np.minimum(1,(D-T(D))/1.2)
L=np.tanh(1.2*reverb(L,1.4,0.16,9))*f; R=np.tanh(1.2*reverb(R,1.4,0.16,10))*f
write('audio/bed.wav',stereo(L,R))
