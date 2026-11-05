"""music.py: a unique numpy bed (plus SFX hits) for each of reels 06 to 10.
usage: python3 music.py <reel> <out.wav> <seconds>     reel in r06 r07 r08 r09 r10
48 kHz stereo 16-bit. Every sound is synthesised here; nothing is sampled."""
import numpy as np, wave, sys

SR = 48000
reel, out, total = sys.argv[1], sys.argv[2], float(sys.argv[3])
rng = np.random.default_rng({'r06': 61, 'r07': 71, 'r08': 81, 'r09': 91, 'r10': 101}[reel])
N = int(SR * (total + 4))
L = np.zeros(N); R = np.zeros(N)

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def tt(d): return np.arange(int(SR * d)) / SR
def put(sig, at, pan=0.0, gain=1.0):
    s = int(at * SR)
    if s >= N or s < 0: return
    n = min(len(sig), N - s)
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[s:s + n] += sig[:n] * gain * l * 1.414; R[s:s + n] += sig[:n] * gain * r * 1.414
def lp(x, fc):   # one-pole low-pass, run twice for 12 dB/oct
    a = np.exp(-2 * np.pi * fc / SR); y = np.empty_like(x); z = 0.0
    for _ in range(2):
        for i in range(len(x)): z = (1 - a) * x[i] + a * z; y[i] = z
        x = y.copy()
    return y
def lp_fast(x, fc):   # FFT brick-ish low-pass with soft knee (fast for long signals)
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= 1 / (1 + (f / fc) ** 4); return np.fft.irfft(X, len(x))
def bp_fast(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X *= (1 / (1 + (lo / np.maximum(f, 1)) ** 4)) * (1 / (1 + (f / hi) ** 4)); return np.fft.irfft(X, len(x))
def env(n, a, d, s=0.0, r=0.0, hold=None):
    t = np.arange(n) / SR
    e = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    if hold is not None:
        e = e * np.where(t > hold, np.exp(-(t - hold) / max(r, 1e-3)), 1.0)
    return e
def reverb(x, secs, mix, damp=3.0, seed=3):
    r2 = np.random.default_rng(seed); n = int(SR * secs)
    ir = r2.normal(0, 1, n) * np.exp(-np.arange(n) / SR * damp); ir[:int(SR * 0.015)] = 0
    ir = lp_fast(ir, 5000); ir /= np.sqrt(np.sum(ir ** 2))
    m = len(x) + n; y = np.fft.irfft(np.fft.rfft(x, m) * np.fft.rfft(ir, m), m)[:len(x)]
    return (1 - mix) * x + mix * y

# ---------- instruments
def strings(freqs, d):          # bowed, string-like pad: detuned saws (additive), slow swell, vibrato
    t = tt(d); s = np.zeros_like(t)
    vib = 1 + 0.0035 * np.sin(2 * np.pi * 5.2 * t) * np.minimum(1, t / 1.5)
    for f in freqs:
        for det in (-0.07, 0.0, 0.08):
            ph = 2 * np.pi * np.cumsum(f * 2 ** (det / 12) * vib) / SR
            for k in range(1, 9): s += np.sin(k * ph + rng.uniform(0, 6)) / k * 0.9 ** k
    e = np.minimum(1, t / 1.6) * np.minimum(1, (d - t) / 1.4)
    return lp_fast(s * e, 2200) / (len(freqs) * 6)
def tick(pitch=2600, d=0.09, bright=1.0):   # clock tick: a tiny wooden click
    t = tt(d); n = rng.normal(0, 1, len(t))
    s = bp_fast(n, pitch * 0.7, pitch * 1.6) * np.exp(-t * 90) * bright + np.sin(2 * np.pi * pitch * 0.5 * t) * np.exp(-t * 70) * 0.6
    return s * 0.5
def whoosh(d=1.0, lo=300, hi=4000, up=True):
    t = tt(d); n = rng.normal(0, 1, len(t)); s = np.zeros_like(t); seg = 2048
    for i in range(0, len(t), seg):
        u = i / len(t); fc = lo * (hi / lo) ** (u if up else 1 - u)
        s[i:i + seg] = bp_fast(n[i:i + seg], fc * 0.6, fc * 1.4)
    return s * np.sin(np.pi * t / d) ** 2 * 0.5
def chime(f, d=3.0):
    t = tt(d); s = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (1.2 + 1.5 * k)) for k, a in [(1, 1), (2.76, 0.4), (5.4, 0.15)])
    return s * np.minimum(1, t / 0.003) * 0.4
def pluck_ks(f, d=2.5, bright=0.5):     # Karplus-Strong plucked string (nylon guitar-ish)
    n = int(SR * d); p = int(SR / f); buf = rng.uniform(-1, 1, p); buf = lp(buf, 1500 + 5000 * bright)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]; buf[i % p] = 0.5 * (buf[i % p] + buf[(i + 1) % p]) * 0.996
    return out * 0.6
def kalimba(f, d=2.2):
    t = tt(d); s = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.6) + 0.35 * np.sin(2 * np.pi * f * 5.95 * t) * np.exp(-t * 14) + 0.2 * np.sin(2 * np.pi * f * 3 * t) * np.exp(-t * 6)
    return s * np.minimum(1, t / 0.002) * 0.45
def arp_synth(f, d=0.5):          # soft pulse pluck, filtered
    t = tt(d); ph = 2 * np.pi * f * t
    s = sum(np.sin(k * ph) / k * (1 if k % 2 else 0.35) for k in range(1, 12))
    s = s * np.exp(-t * 7) * np.minimum(1, t / 0.004)
    return lp_fast(s, 2400) * 0.28
def rhodes(f, d=2.6, vel=1.0):     # FM-ish electric piano tine
    t = tt(d); idx = 1.6 * np.exp(-t * 3.5) * vel
    s = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * f * t)) * np.exp(-t * 1.1)
    s += 0.25 * np.sin(2 * np.pi * f * 7.0 * t) * np.exp(-t * 18) * vel
    return s * np.minimum(1, t / 0.003) * 0.3 * vel
def wurli(f, d=0.9, vel=1.0):       # muted electric piano: odd harmonics, short, damped
    t = tt(d); s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * 3 * f * t) * np.exp(-t * 9) + 0.15 * np.sin(2 * np.pi * 5 * f * t) * np.exp(-t * 14)
    s = np.tanh(1.6 * s) * np.exp(-t * 3.2) * np.minimum(1, t / 0.004) * np.minimum(1, (d - t) / 0.06)
    return lp_fast(s, 2600) * 0.26 * vel
def kick(d=0.35, g=1.0):
    t = tt(d); f = 48 + 90 * np.exp(-t * 28); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    return s * g * 0.9
def shaker(d=0.09, g=1.0):
    t = tt(d); n = rng.normal(0, 1, len(t)); return bp_fast(n, 5000, 11000) * np.minimum(1, t / 0.012) * np.exp(-t * 45) * 0.35 * g
def scratch(d=0.6, g=1.0):        # pencil on paper: band-passed grain with stroke wobble
    t = tt(d); n = rng.normal(0, 1, len(t)); s = bp_fast(n, 1800, 7000)
    am = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * (7 + 3 * rng.random()) * t)) ; am *= (0.6 + 0.4 * (rng.random(len(t)) > 0.3))
    return s * am * np.sin(np.pi * t / d) ** 0.6 * 0.22 * g
def rustle(d=0.45, g=1.0):        # paper: crackle + soft swish
    t = tt(d); n = rng.normal(0, 1, len(t)); sw = bp_fast(n, 600, 5000) * np.sin(np.pi * t / d) ** 2 * 0.25
    cr = np.zeros_like(t); idx = rng.integers(0, len(t), 90); cr[idx] = rng.normal(0, 1, 90); cr = bp_fast(cr, 1500, 9000) * 2.5
    return (sw + cr * np.sin(np.pi * t / d)) * g
def click(g=1.0):
    t = tt(0.05); return (np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 300) + bp_fast(rng.normal(0, 1, len(t)), 2000, 8000) * np.exp(-t * 400) * 0.5) * 0.4 * g
def sub(f, d):
    t = tt(d); return np.sin(2 * np.pi * f * t) * np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.4) * 0.22

# ---------- the pieces
if reel == 'r06':   # reflective: clock ticks + string pad, D minor, 76 bpm
    bpm = 76; b = 60 / bpm; bar = 4 * b
    prog = [[50, 57, 62, 65], [46, 53, 58, 62], [53, 57, 60, 65], [48, 55, 60, 64]]   # Dm Bb F C
    t0 = 0.0; i = 0
    while t0 < total:
        ch = prog[i % 4]; put(strings([mtof(m) for m in ch], bar + 1.6), t0, 0, 0.9); put(sub(mtof(ch[0] - 12), bar + 0.2), t0, 0, 0.8)
        t0 += bar; i += 1
    # ticks: racing through the opening (time flying), then the steady clock, resting on the end card
    tt0 = 0.0; k = 0
    while tt0 < 2.3: put(tick(2900 if k % 2 else 2300, bright=0.7), tt0, 0.3 if k % 2 else -0.3, 0.55); k += 1; tt0 += b / 4 * (1 + 1.6 * tt0 / 2.3)
    tt0 = 2.39; k = 0
    while tt0 < 21.2: put(tick(2900 if k % 2 else 2300), tt0, 0.25 if k % 2 else -0.25, 0.7); k += 1; tt0 += b
    # a high string line on the pattern
    for j, m in enumerate([74, 77, 76, 72, 74]): put(strings([mtof(m)], 1.8) * 0.8, 19.0 + j * b * 0.5, 0.2, 0.6)
    put(whoosh(1.1, 400, 5000), 1.6, 0, 0.6); put(whoosh(1.6, 300, 6000), 11.0, 0, 0.55); put(whoosh(0.9, 3000, 400, up=False), 13.6, 0, 0.4)
    put(chime(mtof(86), 3.5), 21.45, 0.15, 0.55); put(chime(mtof(81), 3.5), 21.75, -0.15, 0.4)
elif reel == 'r07':   # handmade: plucked guitar + kalimba, G major, 84 bpm, paper rustle
    bpm = 84; b = 60 / bpm; bar = 4 * b
    prog = [[43, 50, 55, 59, 62], [40, 47, 52, 55, 59], [36, 48, 52, 55, 60], [38, 50, 54, 57, 62]]  # G Em C D
    t0 = 0.0; i = 0
    pat = [0, 2, 3, 4, 1, 3, 2, 4]
    while t0 < total - 0.5:
        ch = prog[i % 4]
        for k, p in enumerate(pat):
            at = t0 + k * b / 2 + (0.012 if k % 2 else 0)
            if at > total - 1.0: break
            put(pluck_ks(mtof(ch[p]), 2.2, 0.35 + 0.2 * (k == 0)), at, -0.25 + 0.12 * p, 0.85 if k == 0 else 0.6)
        t0 += bar; i += 1
    mel = [74, 76, 79, 76, 74, 71, 74, 79, 81, 79, 76, 74, 71, 74, 76, 74]
    for j, m in enumerate(mel):
        at = 3.15 + j * b
        if at < total - 1.5: put(kalimba(mtof(m)), at, 0.35, 0.55)
    put(kalimba(mtof(79), 3), 16.5, 0.3, 0.7); put(kalimba(mtof(83), 3), 16.5 + b / 2, -0.3, 0.6); put(kalimba(mtof(86), 3.5), 16.5 + b, 0.1, 0.6)
    for at in [0.05, 3.15, 5.7, 8.25, 10.8, 13.35, 16.0]: put(rustle(0.5), at, 0.1, 0.9)
    for at in [2.65, 5.2, 7.75, 10.3, 12.85, 15.5]: put(rustle(0.35, 0.6), at, -0.2, 0.7)
    put(rustle(0.4, 0.8), 11.75, 0.5, 0.8)  # the card lifting away
    for k in range(6): put(scratch(0.22, 0.8), 14.15 + k * 0.23, 0.1, 0.8)   # the pencil
elif reel == 'r08':   # precise, hopeful: soft synth arpeggio, A major, 100 bpm, pencil scratch
    bpm = 100; b = 60 / bpm; bar = 4 * b
    prog = [[57, 61, 64, 69], [52, 59, 64, 68], [54, 61, 64, 69], [50, 57, 62, 66]]   # A E F#m D
    t0 = 0.0; i = 0
    while t0 < total - 0.4:
        ch = prog[i % 4]; seq = [0, 1, 2, 3, 2, 1, 2, 3]
        for k in range(8):
            at = t0 + k * b / 2
            if at > total - 1.2: break
            put(arp_synth(mtof(ch[seq[k]] + 12), 0.55), at, -0.3 + 0.2 * seq[k], 0.8 if k % 4 == 0 else 0.6)
        put(strings([mtof(m) for m in ch], bar + 1.0) * 0.6, t0, 0, 0.5); put(sub(mtof(ch[0] - 12), bar), t0, 0, 0.7)
        if i >= 1: put(kick(0.3, 0.5), t0, 0, 1); put(kick(0.3, 0.35), t0 + 2 * b, 0, 1)
        t0 += bar; i += 1
    for at, d in [(0.1, 0.5), (0.55, 0.8), (1.15, 0.6), (5.35, 0.5), (7.1, 0.7), (7.65, 0.5), (15.2, 0.8), (16.7, 0.4), (17.8, 0.4), (18.9, 0.4), (23.7, 0.7)]:
        put(scratch(d), at, 0.2, 1.0)
    put(whoosh(0.8, 3000, 500, up=False), 3.0, 0, 0.45); put(chime(mtof(88), 2.5), 8.3, 0.2, 0.35); put(chime(mtof(85), 3.0), 24.2, -0.1, 0.45)
elif reel == 'r09':   # warm, light: Rhodes chords + soft shaker, Eb major, 96 bpm
    bpm = 96; b = 60 / bpm; bar = 4 * b
    prog = [[51, 55, 58, 62], [48, 55, 58, 63], [44, 51, 55, 60], [46, 53, 56, 63]]   # Ebmaj7 Cm7 Abmaj7 Bb7sus
    t0 = 0.0; i = 0
    while t0 < total - 0.6:
        ch = prog[i % 4]
        for k, at in enumerate([0, 1.5 * b, 2.5 * b]):
            if t0 + at > total - 1.0: break
            for j, m in enumerate(ch): put(rhodes(mtof(m + 12), 2.4, 0.85 if k == 0 else 0.6), t0 + at + 0.008 * j, -0.2 + 0.13 * j, 0.55)
        put(rhodes(mtof(ch[0]), 2.6, 0.9), t0, 0, 0.6)
        if i >= 1:
            for k in range(8): put(shaker(0.09, 1.0 if k % 2 else 0.6), t0 + k * b / 2 + (0.03 if k % 2 else 0), 0.4, 0.8)
        t0 += bar; i += 1
    put(whoosh(0.6, 600, 6000), 2.95, -0.2, 0.4); put(whoosh(0.6, 600, 6000), 20.25, 0.2, 0.4)
    for k in range(10): put(click(0.5), 9.0 + 1.55 * (1 - (1 - k / 10) ** 2), 0.2, 0.6)   # the count ticking up
    put(chime(mtof(87), 3.0), 10.55, 0.1, 0.5); put(chime(mtof(82), 3.0), 23.4, -0.1, 0.45)
elif reel == 'r10':   # steady, confident: muted electric piano + soft kick, F major, 104 bpm
    bpm = 104; b = 60 / bpm; bar = 4 * b
    prog = [[53, 57, 60, 64], [50, 57, 60, 65], [46, 53, 57, 62], [48, 55, 58, 64]]   # Fmaj7 Dm7 Bbmaj7 C7
    t0 = 0.0; i = 0
    while t0 < total - 0.5:
        ch = prog[i % 4]
        for k in range(8):
            at = t0 + k * b / 2
            if at > total - 1.0: break
            if k in (0, 3, 4, 6):
                for j, m in enumerate(ch[1:]): put(wurli(mtof(m + 12), 0.5 if k else 0.9, 0.9 if k in (0, 4) else 0.6), at + 0.006 * j, -0.15 + 0.15 * j, 0.7)
        put(wurli(mtof(ch[0]), 1.6, 1.0), t0, 0, 0.6); put(sub(mtof(ch[0] - 12), bar), t0, 0, 0.6)
        for k in range(4): put(kick(0.32, 0.8 if k % 2 == 0 else 0.45), t0 + k * b, 0, 1)
        for k in range(4): put(shaker(0.06, 0.5), t0 + k * b + b / 2, 0.3, 0.6)
        t0 += bar; i += 1
    for at in [2.85, 7.45, 12.95, 17.15]: put(whoosh(0.5, 500, 4000), at - 0.1, 0, 0.35)
    put(click(1.0), 10.3, 0.2, 0.8); put(click(1.2), 20.75, 0.3, 1.0); put(chime(mtof(84), 2.5), 21.1, 0.2, 0.4); put(chime(mtof(89), 3), 22.95, 0, 0.45)

# ---------- finish: room, fades, level
n = int(SR * total)
L, R = L[:n], R[:n]
mixr = {'r06': 0.38, 'r07': 0.22, 'r08': 0.25, 'r09': 0.24, 'r10': 0.18}[reel]
L = reverb(L, 2.6, mixr, seed=1); R = reverb(R, 2.6, mixr, seed=2)
tt_ = np.arange(n) / SR; fade = np.minimum(1, tt_ / 0.6) * np.minimum(1, (total - tt_) / 2.0)
L *= fade; R *= fade
pk = max(np.max(np.abs(L)), np.max(np.abs(R))); L *= 0.7 / pk; R *= 0.7 / pk
st = np.stack([L, R], 1)
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
print('wrote', out, round(total, 2), 's')
