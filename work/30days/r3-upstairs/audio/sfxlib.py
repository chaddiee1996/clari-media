"""Small offline SFX kit: filtered noise shapes placed on a timeline. Deterministic (seeded)."""
import numpy as np, wave
from scipy.signal import butter, sosfilt

SR = 48000
_rng = np.random.default_rng(7)

def _env(n, a, r, shape=2.0):
    t = np.linspace(0, 1, n)
    att = max(1, int(n * a)); rel = max(1, int(n * r))
    e = np.ones(n)
    e[:att] = np.linspace(0, 1, att) ** shape
    e[-rel:] *= np.linspace(1, 0, rel) ** shape
    return e

def band(x, lo, hi):
    sos = butter(2, [lo, hi], btype='band', fs=SR, output='sos'); return sosfilt(sos, x)

def lowpass(x, f):
    sos = butter(2, f, btype='low', fs=SR, output='sos'); return sosfilt(sos, x)

def sweep_noise(dur, f0, f1, width=0.6, a=0.35, r=0.6):
    """noise through a band that glides from f0 to f1 (a whoosh)"""
    n = int(dur * SR); x = _rng.standard_normal(n)
    out = np.zeros(n); seg = 1024
    for i in range(0, n, seg):
        p = i / n; f = f0 * (f1 / f0) ** p
        lo, hi = max(40, f * (1 - width / 2)), min(20000, f * (1 + width / 2))
        out[i:i + seg] = band(x[max(0, i - 4096):i + seg], lo, hi)[-len(x[i:i + seg]):]
    return out / (np.abs(out).max() + 1e-9) * _env(n, a, r)

def creak(dur=0.6, f=180):
    """a wooden creak: a rough pulse train with pitch wobble, band limited"""
    n = int(dur * SR); t = np.arange(n) / SR
    fr = f * (1 + 0.25 * np.sin(2 * np.pi * 3.2 * t) + 0.4 * t / dur)
    ph = np.cumsum(fr) / SR
    x = (np.mod(ph, 1) < 0.12).astype(float) + 0.3 * _rng.standard_normal(n)
    x = band(x, 300, 2400)
    return x / (np.abs(x).max() + 1e-9) * _env(n, 0.15, 0.4, 1.5)

def wind(dur, lo=200, hi=1400):
    n = int(dur * SR); x = band(_rng.standard_normal(n), lo, hi)
    t = np.arange(n) / SR; m = 0.7 + 0.3 * np.sin(2 * np.pi * 0.9 * t) * np.sin(2 * np.pi * 0.37 * t + 1)
    return x / (np.abs(x).max() + 1e-9) * m * _env(n, 0.2, 0.45, 1.5)

def scratch(dur, rate=14):
    """pencil / pen on paper: short noise grains"""
    n = int(dur * SR); x = band(_rng.standard_normal(n), 1800, 7000)
    t = np.arange(n) / SR; g = (0.5 + 0.5 * np.sin(2 * np.pi * rate * t + _rng.random() * 6)) ** 2
    g *= 0.6 + 0.4 * _rng.random(n).cumsum() % 1 * 0  # steady
    return x / (np.abs(x).max() + 1e-9) * g * _env(n, 0.08, 0.2, 1.5)

def thud(dur=0.25, f=90):
    n = int(dur * SR); t = np.arange(n) / SR
    x = np.sin(2 * np.pi * f * t * (1 - 0.3 * t / dur)) * np.exp(-t * 18) + 0.3 * lowpass(_rng.standard_normal(n), 600) * np.exp(-t * 40)
    return x / (np.abs(x).max() + 1e-9)

class Track:
    def __init__(self, seconds):
        self.buf = np.zeros((int(seconds * SR) + SR, 2))
    def add(self, t, x, gain=0.5, pan=0.0):
        i = int(t * SR); x = np.asarray(x, float)
        if x.ndim == 1:
            l, r = np.sqrt(0.5 * (1 - pan)), np.sqrt(0.5 * (1 + pan)); x = np.stack([x * l * 1.414, x * r * 1.414], 1)
        j = min(len(self.buf), i + len(x)); self.buf[i:j] += x[:j - i] * gain
    def add_wav(self, t, path, gain=1.0):
        with wave.open(path) as w:
            d = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, w.getnchannels()) / 32768.0
        if d.shape[1] == 1: d = np.repeat(d, 2, 1)
        self.add(t, d, gain)
    def write(self, path, seconds=None):
        b = self.buf if seconds is None else self.buf[:int(seconds * SR)]
        pk = np.abs(b).max()
        if pk > 0.98: b = b / pk * 0.98
        with wave.open(path, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((b * 32767).astype(np.int16).tobytes())
        return path
