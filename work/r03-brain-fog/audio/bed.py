# R3: bouncy marimba + claps + shaker, 120 bpm, F major, comic pops on every slam.
import sys, re; sys.path.insert(0,'/tmp/claude-0/-home-claude/7122b9f6-ef9c-5a65-8b0a-af50e22d1cd8/scratchpad/clari5')
from au import *
D=23.6; B=0.5; N=int(SR*(D+2)); L=np.zeros(N); R=np.zeros(N)
def mar(m,v=1.0):
    t=T(0.9); f=hz(m)
    s=np.sin(2*np.pi*f*t)*np.exp(-t*7)+0.35*np.sin(2*np.pi*f*3.93*t)*np.exp(-t*22)+0.12*np.sin(2*np.pi*f*9.2*t)*np.exp(-t*50)
    return v*s*np.minimum(1,t/0.001)*0.3
def clap(seed):
    t=T(0.2); n=np.random.default_rng(seed).normal(0,1,len(t)); e=np.zeros(len(t))
    for d in (0,0.009,0.018): e+=np.exp(-np.maximum(0,t-d)*140)*(t>=d)
    e+=0.5*np.exp(-t*22); x=hp(lp(n,0.5),0.15)*e; return x*0.35
def kick():
    t=T(0.3); f=52+110*np.exp(-t*35); return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*12)*0.7
def shk(seed): t=T(0.05); return hp(np.random.default_rng(seed).normal(0,1,len(t)),0.7)*np.exp(-t*90)*0.12
def bass(m,d=0.4):
    t=T(d); f=hz(m); return (np.sin(2*np.pi*f*t)+0.3*np.sin(4*np.pi*f*t))*np.exp(-t*5)*env(d,0.004,0.05)*0.5
prog=[(41,[65,69,72,77]),(46,[65,70,74,77]),(48,[67,72,76,79]),(41,[65,69,72,81])]  # F Bb C F
riff=[0,2,1,3,2,1,3,None]  # 8ths per bar index into chord tones
for bi in range(int(D/2)+1):
    root,ch=prog[bi%4]; tb=bi*2.0
    for k in range(8):
        tt=tb+k*B/2
        if tt>D-1.7: break
        sw=0.03 if k%2 else 0
        idx=riff[k] if bi%2==0 else [3,1,2,0,None,2,1,3][k]
        if idx is not None: x=mar(ch[idx]+(12 if (bi%4==3 and k>5) else 0),0.9 if k%2==0 else 0.6); p=0.3+0.4*(idx/3); add(L,x,tt+sw,1-p+0.3); add(R,x,tt+sw,p+0.3)
        add(L,shk(bi*8+k),tt+sw,0.7); add(R,shk(bi*8+k+99),tt+sw,1)
    for q in range(4):
        tt=tb+q*B
        if tt>D-1.7: break
        if q in (0,2): add(L,kick(),tt,0.8); add(R,kick(),tt,0.8); add(L,bass(root-12 if q==0 else root-5),tt,1); add(R,bass(root-12 if q==0 else root-5),tt,1)
        if q in (1,3) and tt>1.9: c=clap(bi*4+q); add(L,c,tt,1); add(R,np.roll(c,90),tt,1)
# end: marimba roll on F chord
for i,m in enumerate([65,69,72,77,81,84]):
    for r in range(6): add(L,mar(m,0.5),21.8+i*0.06+r*0.12,0.5); add(R,mar(m,0.5),21.83+i*0.06+r*0.12,0.5)
x=bass(29,1.6); add(L,x,21.8); add(R,x,21.8)
# comic pops on each slam (times read from the page)
html=open('proj/index.html').read()
tins=sorted(set(float(v) for v in re.findall(r'data-in="([0-9.]+)"',html)))
def pop(i):
    t=T(0.14); f=900-500*t/0.14+ (i%3)*120; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*30)*0.45
def boing():
    t=T(0.6); f=180+60*np.sin(2*np.pi*9*t)*np.exp(-t*4)+t*120; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*5)*0.4
def zip_(d=0.45):
    t=T(d); f=300+2200*(t/d)**2; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.sin(np.pi*t/d)*0.18
for i,tm in enumerate(tins):
    add(L,pop(i),tm+0.17,0.8); add(R,pop(i),tm+0.17,0.8)
for tm in (8.5,): 
    for k in range(8): add(L,mar(72+k*2,0.8),tm+k*0.05); add(R,mar(72+k*2,0.8),tm+k*0.05)   # stairs climb
add(L,zip_(),13.6,1); add(R,zip_(),13.62,1)  # the train leaves
add(L,boing(),9.45,1); add(R,boing(),9.45,1)
L=L[:int(SR*D)]; R=R[:int(SR*D)]
f=np.minimum(1,T(D)/0.05)*np.minimum(1,(D-T(D))/0.9)
L=reverb(L,1.0,0.12,5)*f; R=reverb(R,1.0,0.12,6)*f
write('audio/bed.wav',stereo(L,R))
