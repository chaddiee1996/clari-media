"""Small offline sound-design helpers (numpy + scipy). 48 kHz stereo float arrays."""
import numpy as np, subprocess
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
SR = 48000

def silence(sec): return np.zeros((int(sec * SR), 2), np.float32)
def rng(seed): return np.random.default_rng(seed)
def bp(x, lo, hi, order=4):
    sos = butter(order, [lo, hi], btype='band', fs=SR, output='sos'); return sosfilt(sos, x, axis=0)
def lp(x, f, order=4):
    sos = butter(order, f, btype='low', fs=SR, output='sos'); return sosfilt(sos, x, axis=0)
def hp(x, f, order=4):
    sos = butter(order, f, btype='high', fs=SR, output='sos'); return sosfilt(sos, x, axis=0)
def env(n, a=0.005, r=0.05):
    e = np.ones(n); na, nr = max(1, int(a * SR)), max(1, int(r * SR))
    e[:na] = np.linspace(0, 1, na); e[-nr:] *= np.linspace(1, 0, nr); return e
def stereo(m, pan=0.0):
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    return np.stack([m * l * 1.414, m * r * 1.414], 1).astype(np.float32)
def norm(x, peak=0.9):
    m = np.max(np.abs(x)) or 1; return x * peak / m

def printer(sec, seed=1):
    """thermal printer: stepper buzz (pulsed band noise) + faint motor tone"""
    n = int(sec * SR); t = np.arange(n) / SR; g = rng(seed)
    noise = bp(g.standard_normal(n), 2200, 7000)
    puls = (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 52 * t))) * (0.7 + 0.3 * np.sin(2 * np.pi * 9 * t))
    motor = 0.25 * np.sin(2 * np.pi * 820 * t) * (0.6 + 0.4 * np.sin(2 * np.pi * 52 * t))
    m = (noise * puls * 0.8 + motor * 0.15) * env(n, 0.01, 0.06)
    return stereo(norm(m, 0.5), 0.0)
def tear(sec=0.55, seed=3):
    n = int(sec * SR); g = rng(seed); t = np.arange(n) / SR
    crackle = (g.random(n) > 0.9).astype(float) * g.standard_normal(n)
    noise = bp(g.standard_normal(n) * 0.5 + crackle * 2.5, 900, 6500)
    e = np.clip(t / (sec * 0.75), 0, 1) ** 1.5 * env(n, 0.002, 0.05)
    e *= (0.6 + 0.4 * np.abs(np.sin(2 * np.pi * 23 * t)))
    return stereo(norm(noise * e, 0.8), 0.1)
def clunk(seed=4, f=95):
    n = int(0.35 * SR); t = np.arange(n) / SR; g = rng(seed)
    body = np.sin(2 * np.pi * f * t) * np.exp(-t * 22)
    click = hp(g.standard_normal(n), 2000) * np.exp(-t * 180) * 0.5
    return stereo(norm(body + click, 0.6), 0.0)
def whoosh(sec=0.8, seed=5, lo=300, hi=2400, peak_at=0.55):
    n = int(sec * SR); g = rng(seed); t = np.arange(n) / SR
    x = g.standard_normal(n)
    # sweeping band: crossfade a low and a high band
    a = bp(x, lo, lo * 3); b = bp(x, hi / 2, hi)
    sw = np.clip(t / sec, 0, 1)
    m = a * (1 - sw) + b * sw
    e = np.where(t < sec * peak_at, (t / (sec * peak_at)) ** 2, np.exp(-(t - sec * peak_at) * 7))
    return stereo(norm(m * e, 0.6), 0.0)
def blip(f=880, sec=0.12, drop=0.6):
    """bubble pop: a short sine chirp that rises"""
    n = int(sec * SR); t = np.arange(n) / SR
    fr = f * (1 + drop * t / sec); ph = 2 * np.pi * np.cumsum(fr) / SR
    m = np.sin(ph) * np.exp(-t * 38) * env(n, 0.001, 0.02)
    return stereo(norm(m, 0.6), 0.0)
def water(sec, seed=6, level=0.3):
    n = int(sec * SR); g = rng(seed); t = np.arange(n) / SR
    x = lp(g.standard_normal(n), 900) * (0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t))
    bub = np.zeros(n)
    for i in range(int(sec * 9)):
        p = int(g.random() * (n - 4000)); f = 400 + g.random() * 900; k = np.arange(3000) / SR
        bub[p:p + 3000] += np.sin(2 * np.pi * f * (1 + 2 * k) * k) * np.exp(-k * 60) * 0.3
    m = x + bub
    return np.stack([norm(m, level), norm(np.roll(m, 300), level)], 1).astype(np.float32)
def tick(seed=7, f=3200):
    n = int(0.05 * SR); t = np.arange(n) / SR; g = rng(seed)
    m = bp(g.standard_normal(n), f * 0.7, f * 1.4) * np.exp(-t * 260) + 0.3 * np.sin(2 * np.pi * f * t) * np.exp(-t * 200)
    return stereo(norm(m, 0.5), 0.0)
def slide(sec=0.35, seed=8):
    """card / paper slide: soft band noise swell"""
    n = int(sec * SR); g = rng(seed); t = np.arange(n) / SR
    m = bp(g.standard_normal(n), 500, 4000) * np.sin(np.pi * t / sec) ** 2
    return stereo(norm(m, 0.45), 0.0)

def place(track, clip, at, gain=1.0):
    i = int(at * SR); j = min(len(track), i + len(clip))
    if i < len(track) and j > i: track[i:j] += clip[:j - i] * gain
def read(path):
    sr, x = wavfile.read(path); x = x.astype(np.float32)
    if x.dtype != np.float32 or np.max(np.abs(x)) > 2: x = x / 32768.0
    if x.ndim == 1: x = np.stack([x, x], 1)
    assert sr == SR, sr; return x
def write(path, x):
    wavfile.write(path, SR, np.clip(x, -1, 1).astype(np.float32))
