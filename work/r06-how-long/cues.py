"""cues.py: split each measured speech segment into caption chunks, snapping
chunk boundaries to the quietest point near the proportional estimate.
usage: python3 cues.py vo.mp3 spec.json out.json
spec: [{"s":2.39,"e":6.36,"chunks":["Symptoms can start","months,"]}, ...]
"""
import json, subprocess, sys, re
import numpy as np

vo, spec, out = sys.argv[1:4]
SR = 16000
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', vo, '-ac', '1', '-ar', str(SR), '-f', 's16le', '-'],
                     capture_output=True).stdout
x = np.frombuffer(raw, '<i2').astype(np.float32) / 32768
hop = int(SR * 0.01)
env = np.sqrt(np.convolve(x ** 2, np.ones(hop * 3) / (hop * 3), 'same')[::hop])

def weight(s):
    # rough syllable-ish weight: vowel groups, plus a little for punctuation pauses
    w = len(re.findall(r'[aeiouy]+', s.lower())) + 0.15 * len(s.split())
    w += 0.8 * s.count(',') + 1.0 * s.count('...')
    return max(w, 1)

res = []
for si, seg in enumerate(json.load(open(spec))):
    s, e, ch = seg['s'], seg['e'], seg['chunks']
    ws = np.array([weight(c) for c in ch]); cum = np.concatenate([[0], np.cumsum(ws)]) / ws.sum()
    bounds = [s]
    for k in range(1, len(ch)):
        est = s + (e - s) * cum[k]
        i0, i1 = int((est - 0.22) * 100), int((est + 0.22) * 100)
        i = i0 + int(np.argmin(env[i0:i1]))
        bounds.append(round(max(bounds[-1] + 0.3, i / 100), 2))
    bounds.append(e)
    for k, c in enumerate(ch):
        res.append({'text': c, 't0': round(bounds[k], 2), 't1': round(bounds[k + 1], 2), **{kk: v for kk, v in seg.items() if kk not in ('s', 'e', 'chunks')}, 'seg': si, 'k': k, 'n': len(ch)})
json.dump(res, open(out, 'w'), indent=1)
for r in res: print(f"{r['t0']:6.2f} {r['t1']:6.2f}  {r['text']}")
