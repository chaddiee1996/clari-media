# R14 Private, by design
Look: midnight-grid (STYLE.md in proj/). 1080 x 1920, 30 fps, 20 s, does not loop. Text only + music (VOICED: VO 17.04 s + 3 s end card).
Alignment: right-aligned headlines on one right edge (x 940) shared with the phone.
Fonts: Space Grotesk 700 / 500 (Google Fonts). Every font linked in <head>.
Palette: ground #0B1220, dots #1E2A44, panel #111A2E, border #2A3A5E, text #EEF2FA, accent blue #3D8BFF.
Type: headlines 110 to 270 px heavy, labels 58 to 68 px heavy, sources 48 to 52 px. Nothing under 48 px. Safe area: key text between y 220 and 1540, right edge at most x 940.
Words (exact, no em or en dashes):
- Your symptoms are nobody's business but yours.
- That's why Clari keeps your symptom data on your phone.
- No account needed to start.
- You decide what to share, and when.
- like a summary for your GP, made from your own notes.
- Private, by design.
- Clari. Free on the App Store and Google Play
Music: C# minor, 80 bpm: deep detuned saw pad, heartbeat lub-dub kick, sub; ducked to 0.15 under VO, rises on the end card; SFX: lock click 6.48, switch flick 10.55, end chime 17.1. 48 kHz, composed in numpy (scratchpad a1115/r14.py).
Bans: no glow beyond the look's own, no linear easing on followed motion, nothing scaling from zero, one accent colour, no fake chrome, no grey text.
