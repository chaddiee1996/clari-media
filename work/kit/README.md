# Clari brand kit (for every reel, carousel and story)

Read `/home/claude/clari-media/work/30days/PLAN.md` first: it has the brief and the final copy for your pieces.

## Logo (the only logo, never redraw it)
- `logo/icon.png`  2048 px app icon tile (crescent + blossoms on the plum sky). Draw it with rounded corners
  (radius = 23% of its width) like an app icon.
- `logo/mark.png`  crescent + blossoms, transparent, no tile (for corners of stories/slides, small "bug" marks).
- `logo/mark-white.png`, `logo/mark-plum.png`  one-colour versions (for tiny sizes or on photos/paper).
- `logo/lockup-light.png` (cream wordmark, for dark backgrounds) / `logo/lockup-dark.png` (plum wordmark, for paper).
  Tile + "Clari" in Fraunces 600. Use on carousel first/last slides and story corners.

## End of every reel
`sting/sting.mp4` is the 4 s brand ending (tile rises, petals, "Clari", "Your private perimenopause diary",
"Free on the App Store and Google Play", with the Clari sound logo). After your reel is rendered and mixed:
`bash /home/claude/clari-media/work/kit/append_sting.sh reel_mixed.mp4 final.mp4`
It cross-dissolves for 0.4 s. Do not build your own end card or draw the logo at the end of the reel itself.
Plan the reel's last 0.6 s as a calm hold (it dissolves away).

## Art (canvas): `art/clari-art.js`
Copy it into your project folder (projects cannot load files from outside their folder), load it after studio.js.
`CLARI.sky / stars / moon / blossom / petal / branch / hills / sparkle / phone / plate / rich / loadImg`.
See the header comment for signatures. Skies: 'night', 'evening', 'dawn', 'day', 'icon'.
`kit/demo/demo.html` shows them together (rendered: `kit/demo/demo.png`).
Build your own scene objects (clock, staircase, receipt, bath, thermostat, wine glass, letterbox, notebook...)
in the same flat-gradient style: soft vertical gradients, rounded shapes, no outlines heavier than 4 px,
gentle drop shadows (rgba(16,4,40,.35)), pink glow only around the moon.

## Real app screens: `screens/`
Real screenshots of the live app (1290 x 2796): home, homelogged, log, triggers, done, calendar, insights, summary.
Show them in `CLARI.phone(...)`. The sample user is "Sarah", which is fine. Never edit what the screens say.

## Fonts (Google Fonts link, same in every project)
`<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,500;0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,500;1,9..144,600;1,9..144,700&family=Figtree:wght@500;600;700;800&family=Caveat:wght@600;700&display=swap">`
On canvas wait for `document.fonts.ready` (studio.js redraws when fonts load) and use
`"600 140px 'Fraunces'"` etc. Fraunces looks best large; set `font-variation-settings` only in DOM text.

## Music: `music/musiclib.py`
Real sampled instruments (FluidR3_GM soundfont, MIT licence) rendered with FluidSynth. See the docstring.
`music/sonic_logo.py` is an example. Check loudness with `musiclib.loudness(path)` (you cannot listen).
Write a real piece: a melody with a shape, chord changes that move, an intro and a lift where the story turns.
Mix the music to the picture: hits on reveals, a lift at the turn, thin out under voice.

## Statics (carousels, stories): `statics/shot.js`
`node /home/claude/clari-media/work/kit/statics/shot.js slide.html out.png 1080 1440` (or 1080 1920).
Use HTML/CSS (DOM text is crisper than canvas) plus inline SVG or a canvas with clari-art.js for art.
Save final slides as high-quality JPG (quality 92) after checking the PNG.

## Skill
claude-video-studio: `/home/claude/clari-media/.claude/skills/claude-video-studio` (SKILL.md, scripts/).
Use its process (brief, storyboard, stills scored at 8+, render with HF_WORKERS=1, pacing_check.py).
You do NOT need the gallery or the five questions: the plan is your brief and the Clari world is your style.
