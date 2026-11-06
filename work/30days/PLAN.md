# Clari: 30 days of content, Mon 9 Nov to Tue 8 Dec 2026

Owner: Claude (art director + copywriter). Builders follow this file word for word. Copy is final: do not
rewrite it. If a line will not fit, tell the art director; never invent new claims.

## 0. The one idea that ties it together

Every piece lives in **the Clari world**: the app's own moonlit sky, the crescent-and-blossom logo,
Fraunces serif with one pink italic word, cream type, blossoms and petals. Women who see three posts
should know the fourth is Clari before the logo appears. Inside that world every piece has its own
concept, scene, time of day, layout, motion, music and sound. The world is consistent; the ideas never repeat.

Recognition anchors (every piece, no exceptions):
1. Real logo only: `kit/logo/icon.png` (app icon tile), `kit/logo/mark.png` (crescent + blossoms, no tile),
   `kit/logo/lockup-light.png` / `lockup-dark.png` (tile + "Clari" wordmark). Never draw a different moon as "the logo".
2. Every reel ends with the identical 4 s sting `kit/sting/sting.mp4` (tile rises, petals, wordmark, sound logo),
   appended with `bash kit/append_sting.sh in.mp4 out.mp4`. The reel itself does NOT draw its own end card.
3. Type: Fraunces (headlines, 600 to 800, one word per headline may be italic 600 in pink #F7B6CD on dark
   or rose #B83A68 on light) + Figtree (labels, body, 600 to 800). Caveat only for handwriting in the paper world.
4. Colour family: night #22103F, plum #4A2070, violet #7A45B5, lilac #C3A8EA, cream #FFF8EC, pink #F7B6CD,
   blossom #E8628F, rose #B83A68, moon gold #FFEFC9. Paper world: #FBF6EE paper, ink #241A33.
5. Source line on screen whenever a fact is shown: Figtree 700, at least 44 px, e.g. "Source: NHS".

Sub-worlds (pick the one each brief names): **Sky** (night, evening, dawn, day, from kit/art SKIES),
**Paper** (cream stationery, the GP summary page, pencil and handwriting), **App** (real app screens in a phone,
from kit/screens, all real screenshots of the live app).

## 1. Hard rules (break one and the piece is rejected)

- No em dashes or en dashes anywhere (on screen, captions, alt text). No " - " either.
- Banned words: neon, unlock, empower, journey, game changer, elevate, delve, navigate, embrace, "let's dive in",
  "you've got this", "ladies", diagnose, detect, treat, cure, manage, "you have". No emoji in on-screen text.
- Treatment neutral. Never say what anyone should take. Never imply the viewer has a condition.
- No red/amber/green, no scores, no "risk" visuals.
- Facts only from section 6, worded as there. Source on screen.
- Phone-first type: nothing under 48 px on a 1080 x 1920 frame (44 px allowed for the source line only).
  Headlines 110 to 170 px. Statics 1080 x 1440: nothing under 40 px, headlines 90 to 140 px.
- Safe areas on 9:16: keep text out of the top 230 px, bottom 400 px, right 150 px (IG/TikTok buttons).
- High contrast. Text over busy art sits on a plate or a clear area.
- No people drawn (faceless brand). Objects, rooms, sky, paper, the app. Hands are allowed only as simple flat silhouettes.
- Alignment: follow each brief. Not everything centred, never default left.
- At most about 8 words on screen at once (except list slides on carousels).
- Never reuse anything from templates/nov, templates/v2, notes-v3/v4, or work/r01..r15 (the rejected batch).

## 2. Production rules

- Reels: 1080 x 1920, 30 fps, built with the claude-video-studio skill (HyperFrames + GSAP, one clock),
  canvas art from `kit/art/clari-art.js`. Stills scored 8+ by a harsh eye before rendering. Pacing check must pass.
- Voiced reels: VO is `work/30days/vo/<id>.mp3`, word timings in `work/30days/vo/<id>.words.json` (Whisper transcription; words may be misspelt, e.g. "Clary" = Clari, timings are right). On-screen
  words appear exactly when spoken (most people watch muted).
- Music: real sampled instruments via `kit/music/musiclib.py` (FluidR3 GM, MIT licence). Each reel its own key,
  tempo, instruments and melody (brief gives the direction). Sound effects can be built from the soundfont
  (woodblock, drums kit notes, glockenspiel, fx programs) or simple filtered noise.
- Mix: voiced: VO loudnorm I=-16, music about 12 dB under the voice (check with loudness()), duck in gaps is fine.
  Text-only: whole mix about I=-14. Then append the sting. AAC 192k 48 kHz.
- Output: `/home/claude/clari/30 days/<date> <Type> - <Title>.mp4` (reels), carousels as numbered JPGs in a folder.

## 3. The calendar (UK time, Europe/London)

IG: Mon carousel 18:00 · Tue reel 10:00 · Thu reel 18:00 · Sat carousel 10:00 · Sun reel 19:00 · story every day.
TikTok: Tue reel goes Wed 18:00 · Thu reel goes Thu 10:00 · Sun reel goes Mon 18:00 · Fri photo post 18:00.

| Date | Instagram | TikTok | Story |
|---|---|---|---|
| Mon 9 Nov | C1 It's not just hot flushes (carousel) | (R0 none) | S09 |
| Tue 10 Nov | R1 3:07am | | S10 |
| Wed 11 Nov | | R1 3:07am | S11 |
| Thu 12 Nov | R2 Too young? (VO) | R2 | S12 |
| Fri 13 Nov | | C1 as photo post | S13 |
| Sat 14 Nov | C2 Before your GP appointment | | S14 |
| Sun 15 Nov | R3 Why did I come upstairs? | | S15 |
| Mon 16 Nov | C3 Self Care Week: 7 small things | R3 | S16 |
| Tue 17 Nov | R4 The notes nobody writes (VO) | | S17 |
| Wed 18 Nov | | R4 | S18 |
| Thu 19 Nov | R5 The receipt | R5 | S19 |
| Fri 20 Nov | | C3 as photo post | S20 |
| Sat 21 Nov | C4 Brain fog, translated | | S21 |
| Sun 22 Nov | R6 Not a bubble bath | | S22 |
| Mon 23 Nov | C5 Peri, meno, post: the words | R6 | S23 |
| Tue 24 Nov | R7 Make your GP appointment count (VO) | | S24 |
| Wed 25 Nov | | R7 | S25 |
| Thu 26 Nov | R8 Private, by design (VO) | R8 | S26 |
| Fri 27 Nov | | C5 as photo post | S27 |
| Sat 28 Nov | C6 Menopause at work: what's changing | | S28 |
| Sun 29 Nov | R9 Heating on, duvet out | | S29 |
| Mon 30 Nov | C7 When the NHS says to contact your GP | R9 | S30 |
| Tue 1 Dec | R10 How long does it last? (VO) | | S01 |
| Wed 2 Dec | | R10 | S02 |
| Thu 3 Dec | R11 One more glass? | R11 | S03 |
| Fri 4 Dec | | C7 as photo post | S04 |
| Sat 5 Dec | C8 What to say to a friend | | S05 |
| Sun 6 Dec | R12 £19.80 (VO) | | S06 |
| Mon 7 Dec | C9 What Clari keeps, and where | R12 | S07 |
| Tue 8 Dec | R13 A new question at your Health Check (VO) | | S08 |

Totals: 13 reels, 9 carousels (4 also as TikTok photo posts), 30 stories. 7 reels voiced (AI label), 6 text and music.

## 4. Reels: full briefs

### R1 "3:07am"  (Tue 10 Nov) · no voice · Sky: night, a bedroom · alignment: centred under a giant clock, then text drops to lower third
Hook: the bedside clock fills the frame and flips 3:06 to 3:07. The whole piece is the rhythm of one bad night.
On screen, in order (one beat each, 1.2 to 1.6 s, comic rhythm that speeds up):
1. "3:07am."  (clock flips; room is dark violet, moon through the window)
2. "Duvet off."  (duvet slides off the bed edge)
3. "Duvet on."
4. "Duvet off."  (faster)
5. "Pillow flipped to the *cold* side."
6. "Window open. In November."  (window swings open, cold air streaks, a leaf blows in)
7. "By breakfast, you'll have *forgotten* it happened."  (clock spins forward to 7:15, sky turns dawn)
8. "Night sweats are on the NHS list of perimenopause symptoms."  Source: NHS
9. Phone slides up showing the real Log screen (kit/screens/log.png). Text: "Log it *before* you forget."
Then sting. Length 19 to 22 s before sting.
Music: felt piano lullaby in E flat major, 66 bpm, music box doubling the top line, warm pad; it slowly warms up
as dawn arrives. SFX: soft clock tick, duvet whoosh (filtered noise), window creak (low woodblock + noise), a single glockenspiel note on "forgotten".
Caption:
"3am, again? Night sweats are on the NHS list of perimenopause symptoms, and they're easy to forget by morning.
Note them when they happen, so you can show your GP the real picture.
Send this to the friend who's up at 3am too.
#perimenopause #perimenopauseUK #nightsweats"

### R2 "Too young?"  (Thu 12 Nov) · VOICE vo/R2 · Paper world: NICE guideline pages on a desk · alignment: giant numerals right-aligned, words right-aligned to the same edge
Hook: "41." in huge Fraunces ink numerals on cream paper, a pencil underlines it; "Told you're too young?" in pink italic.
Words on screen follow the voice. Structure: three paper index cards slide in one after another, like dividers:
card "Over 45": "Symptoms are enough. No blood test needed." · card "40 to 45": "A blood test can be considered." ·
card "Under 40": "Two blood tests, 4 to 6 weeks apart." Then "Too young isn't the *end* of the conversation."
then "Write down what's changed. Take it with you." (handwritten list being written in Caveat).
Source: NICE guideline NG23 (always visible while the ages are on screen).
Music: calm, confident; nylon guitar fingerpicking in A minor, 84 bpm, soft cello, very sparse under voice.
SFX: paper slides, pencil scratch on the underline.
Caption:
"Perimenopause at 41 and told you're too young?
NICE guideline NG23 says that over 45, perimenopause can be recognised from symptoms like hot flushes and irregular periods, with no blood test needed. Between 40 and 45 a blood test can be considered. Under 40, it's two blood tests, 4 to 6 weeks apart.
Save this for your next appointment.
#perimenopause #perimenopauseUK #NICEguidelines"

### R3 "Why did I come upstairs?"  (Sun 15 Nov) · no voice · Sky: day, a sunny staircase · alignment: diagonal, each line sits on its own stair, climbing left-low to right-high
Hook: "Why did I come upstairs?" at the top of a staircase seen side-on; the camera climbs one stair per beat.
Each stair holds one lost thing (small flat object + line):
1. "The word for colander."  (a colander)
2. "My glasses. They were on my head."  (glasses)
3. "Her name. We've been friends for twenty years."  (two mugs)
4. "What I was saying. Mid-sentence."  (a speech bubble that trails off "...")
5. Top stair, empty: "Why I came upstairs."
Turn: the sky behind the window goes soft pink. "Problems with memory and concentration are on the NHS list. It's called *brain fog*." Source: NHS
Close: "Send this to the friend who finishes your sentences."
Music: playful pizzicato strings + marimba in F major, 112 bpm, a bassoon "huh?" note at each stair. SFX: a soft footstep (low tom) per stair, a woodblock "tok" when each object lands.
Caption:
"Why did I come upstairs?
Problems with memory and concentration are on the NHS list of perimenopause symptoms. It even has a name: brain fog.
If it's happening a lot, write it down when it happens. Patterns are easier to talk about than \"I keep forgetting things\".
#perimenopause #brainfog #perimenopauseUK"

### R4 "The notes nobody writes"  (Tue 17 Nov, Self Care Week) · VOICE vo/R4 · Sky: dawn + Paper · alignment: two columns facing each other, left page and right page of an open notebook
Concept: an open notebook. Left page "What women post" fills with handwritten symptoms (brain fog, can't think straight,
low mood, I don't feel like me); right page "What gets written down" stays almost empty, one line: "Hot flushes."
The stat lands as two simple, honest dot grids (no colour coding): 20 dots of 100 filled on the left ("about 1 in 5 posts"),
5 of 100 on the right ("about 1 in 20 clinic visits"). Then the right page starts filling in as the voice says "write them down".
On screen (synced to voice): "It's Self Care Week." · "The symptoms that get *left out*." · "Memory and thinking problems" ·
"About 1 in 5 posts" · "About 1 in 20 clinic visits" · "Mood, too." · "They're real. They just don't make it into the room." ·
"Write them down. Take them with you."
Source: Mehta et al, JAMA Network Open, 2026
Music: warm Rhodes chords in D major, 76 bpm, brushed snare very low, a single harp gliss at the turn. SFX: pen on paper.
Caption:
"The perimenopause symptoms that don't make it into the room.
A 2026 study compared Reddit posts about menopause with clinical notes. Memory and thinking problems came up in about 1 in 5 posts, but only about 1 in 20 clinic visits. Mood and emotional wellbeing were missing too.
It's Self Care Week. Start by writing down how you really feel.
Source: Mehta et al, JAMA Network Open, 2026.
#perimenopause #selfcareweek #perimenopauseUK"

### R5 "The receipt"  (Thu 19 Nov, Self Care Week) · no voice · Sky: evening, a supermarket at closing · alignment: centred receipt, text printed onto it line by line
Concept: a till receipt prints from the top of the frame, long and curling, itemising her day like shopping.
Header in monospace style (use Figtree 800 caps, not a mono font): "TODAY". Items print one per beat:
1. "Unexpected item in bagging area. Fourth time."
2. "A rage I didn't recognise."
3. "Cried at an advert. About gravy."
4. "Snapped. Said sorry. Snapped again."
5. "Lay awake. Worried about everything."
Rule line, then "TOTAL" in big Fraunces: "Mood swings, low mood, anxiety." then "All on the NHS list." Source: NHS
Close (receipt tears off, flutters down): "You're not *imagining* it." then "Keep the receipt. Write it down."
Music: lo-fi, gentle: muted Rhodes + finger bass + brushed kit in B flat, 82 bpm, a little tape wobble is fine. SFX: thermal printer bursts (filtered noise pulses), till beep (glockenspiel), a paper tear.
Caption:
"Mood swings, low mood and anxiety are all on the NHS list of perimenopause symptoms.
If your days have started to feel like this, you're not imagining it. Write down what happened and how you felt. It helps when you talk to your GP.
Self Care Week is about mind and body. This is the mind part.
#perimenopause #selfcareweek #moodswings"

### R6 "Not a bubble bath"  (Sun 22 Nov, last day of Self Care Week) · no voice · Sky: evening into night, a bathroom window · alignment: words float inside bubbles all over the frame, each bubble somewhere new
Hook: "Self care isn't always a bubble bath." A bath fills with bubbles; one by one they rise and each holds a small real thing:
"Bed at 9:30. No guilt." · "A cold drink by the bed." · "A walk while it's still light." · "Saying no to one thing." ·
"Telling one person how you actually feel." · "Writing down today, so tomorrow has the facts."
Then the bubbles pop into petals and the line: "Small things *count*." Source line: "Ideas from NHS advice on rest, exercise and talking to others."
Music: harp and slow strings in G major, 70 bpm, a celesta on each bubble. SFX: soft water, bubble pops (short sine blips or glockenspiel ticks).
Caption:
"Self care isn't always a bubble bath.
The NHS suggests rest and a regular sleep routine, regular exercise, and talking to people going through the same thing. Small, real things.
Last day of Self Care Week. Which one are you doing tonight?
#selfcareweek #perimenopause #perimenopauseUK"

### R7 "Make your GP appointment count"  (Tue 24 Nov) · VOICE vo/R7 · App + Paper: an appointment card and a stopwatch · alignment: centred stack, steps sit on numbered tabs that stack like a pile of cards
Hook: a stopwatch races; "GP appointments go *fast*."
Step tabs (each slides in on its number, words synced to voice):
"1  When you book" · "Ask which GP is best to see about menopause." · "Ask for a longer slot, if you can." ·
"2  Bring a record" · "Each symptom. How often. How strong." (show the real Summary screen, kit/screens/summary.png) ·
"3  Say it plainly" · "“I think this could be perimenopause. What are my options?”" (pink quote marks, big) ·
"Save this for the day you book."
Music: steady, reassuring; soft piano ostinato in C major, 96 bpm, light shaker, strings enter on step 3. SFX: stopwatch tick at the start, card slides.
Caption:
"How to make a short GP appointment count, if you think it's perimenopause.
1. When you book, ask which GP is best to see about menopause, and if a longer appointment is possible.
2. Bring a record: what you've noticed, how often, and how bad.
3. Say it plainly: \"I think this could be perimenopause. What are my options?\"
Save this for the day you book.
#perimenopause #perimenopauseUK #GPappointment"

### R8 "Private, by design"  (Thu 26 Nov) · VOICE vo/R8 · App + Sky: night · alignment: right-aligned headlines on the right, phone on the left, they share a horizon line
Concept: a phone floats in the night sky; symptom words (Hot flushes, Brain fog, Low mood, Night sweats) drift towards it
as petals and settle INSIDE the screen; the crescent closes around the phone like a lock. Use real screens: home.png then summary.png.
On screen synced: "Your symptoms are nobody's business but *yours*." · "Your symptom data stays on your phone." · "No account needed to start." ·
"You decide what to share, and when." · "A summary for your GP, from your own notes." · "Private, by design."
Music: hushed, intimate: warm pad + celesta in A flat, 72 bpm, a low heartbeat-soft kick. SFX: soft whoosh as petals enter.
Caption:
"Your symptoms are nobody's business but yours.
Clari keeps your symptom data on your phone. No account needed to start. You choose what to share and when, like a summary for your GP made from your own notes.
Private, by design.
#perimenopause #perimenopauseUK #privacy"

### R9 "Heating on, duvet out"  (Sun 29 Nov) · no voice · Sky: winter night, frost on a window, a radiator · alignment: text wraps around a big round thermostat dial, centred, each tip appears as the dial turns down a notch
Hook: "The heating's on. The duvet's out." then "And you're *on fire*." (warm glow floods the cold blue room)
The dial clicks down a notch per tip (NHS list, in this order):
"Light clothes to bed." · "Keep the bedroom cool at night." · "A cool shower, a fan, or a cold drink." ·
"Go easy on the triggers: spicy food, caffeine, hot drinks, alcohol." Source: NHS
Close: frost grows back on the window, calm: "Save this for *tonight*."
Music: winter lullaby: celesta + soft strings + harp in D minor turning to F major, 72 bpm. SFX: dial clicks (woodblock hi), radiator tick, soft wind.
Caption:
"Heating on, duvet out, and you're on fire?
NHS tips for hot flushes and night sweats: lightweight clothing, a cool bedroom at night, a cool shower, a fan or a cold drink, and cutting down on triggers like spicy food, caffeine, hot drinks and alcohol.
Save this for tonight.
#nightsweats #hotflushes #perimenopause"

### R10 "How long does it last?"  (Tue 1 Dec) · VOICE vo/R10 · Sky: the moon's phases passing over years · alignment: a horizontal row of moon phases sweeps across mid-frame; words sit above it centred, the year count sits below it right-aligned
Concept: moon phases tick past like months, faster and faster; a counter beneath counts years 1 to 9.
Synced on screen: "How long does it last?" · "Usually *7 to 9* years." · "Sometimes longer." · "And it can change." ·
"Hot flushes ease." · "Low mood or anxiety take their place." · "That's a lot to remember." · "Keep a record. Let the pattern *speak*."
At "change": the symptom label under the moons crossfades from "Hot flushes" to "Low mood" to "Anxiety".
Source: NHS
Music: reflective, moving forward: piano arpeggios in B flat major, 92 bpm, strings swell slowly, clock-like woodblock pulse under the years.
Caption:
"How long do menopause symptoms last?
The NHS says symptoms usually last 7 to 9 years, sometimes longer, and they can change. Hot flushes may ease and be replaced by low mood or anxiety.
That's a lot to keep in your head. A record of your symptoms shows the pattern for you.
#perimenopause #menopausesymptoms #perimenopauseUK"

### R11 "One more glass?"  (Thu 3 Dec) · no voice · Sky: evening party, fairy lights, a window full of stars · alignment: text sits inside the outline of a big wine glass, centred, rising with the liquid level
Hook: "Christmas party." · "Second glass." · "Here it *comes*." (warmth rises up the frame like the glass filling, fairy lights brighten, a hot glow)
Then: "Alcohol is on the NHS list of possible hot flush triggers." Source: NHS · "Not a lecture. Just worth *noticing*."
Phone shows real Log screen with triggers (kit/screens/triggers.png): "Log what you drank, and how you felt." · "Then see your own pattern."
Music: festive but soft: brushed jazz trio in G, 104 bpm swing (jazz guitar comping, upright bass, brushes), vibraphone melody. SFX: two glasses clink, party murmur kept very low (filtered noise).
Caption:
"Christmas party, second glass, and here comes the hot flush?
Alcohol is on the NHS list of possible hot flush triggers, along with spicy food, caffeine and hot drinks. Not a lecture. Just worth noticing.
Log what you had and how you felt, and see your own pattern.
#hotflushes #perimenopause #partyseason"

### R12 "£19.80"  (Sun 6 Dec) · VOICE vo/R12 · Paper + Sky: day · alignment: "£19.80" huge and centred, a 12-month calendar grid below it lights month by month, words right-aligned above
Concept: twelve small month tiles (Jan to Dec) light up one by one, all covered by one certificate that slides over them.
Synced on screen: "If you pay for HRT prescriptions in England" · "this one's worth knowing." · "HRT prescription prepayment certificate" ·
"£19.80" · "Covers certain HRT medicines for 12 months." · "The price of two single prescriptions." · "Buy online, or at some pharmacies." ·
"Ask your pharmacist if yours is covered." Source: NHSBSA
Music: light and bright: marimba + pizzicato in E flat, 100 bpm, a glockenspiel sparkle as each month lights. SFX: a soft stamp when the certificate lands.
Caption:
"Pay for HRT prescriptions in England? This is worth knowing.
The HRT prescription prepayment certificate costs £19.80, the cost of two single items, and covers an unlimited number of certain HRT medicines for 12 months. NHSBSA says it could save you money if you pay for HRT 3 or more times a year.
Buy it online or at some pharmacies, and check your HRT is covered first.
Source: NHSBSA.
#HRT #perimenopauseUK #menopauseUK"

### R13 "A new question at your Health Check"  (Tue 8 Dec) · VOICE vo/R13 · Sky: dawn + Paper: a letter through a letterbox · alignment: left of centre letter, text right-aligned on the right half
Concept: dawn hallway; an envelope drops through the letterbox and opens to an invitation; a new line writes itself on it: "Menopause and perimenopause".
Synced: "Something new is coming to the NHS Health Check." · "In England." · "Women aged 40 to 55" · "will be asked about menopause and perimenopause." ·
"Part of the government's plan for women's health." · "When your invitation lands, go in *ready*." · "Your symptoms. How long. How often." ·
"It's your chance to be asked. Make it count."
Small fact line: "NHS Health Checks: every 5 years, ages 40 to 74, England." Source: UK Government, Oct 2025
Music: hopeful morning: acoustic steel guitar + flute in G major, 98 bpm. SFX: letterbox clack, envelope tear.
Caption:
"The NHS Health Check is adding a question about menopause.
In October 2025 the government asked councils in England to add a menopause element to NHS Health Checks in 2026, so eligible women aged 40 to 55 can get advice about menopause and perimenopause more easily.
When your invitation comes, go in with your symptoms written down.
Source: UK Government written statement, 23 Oct 2025.
#NHSHealthCheck #perimenopauseUK #menopause"

## 5. Carousels (IG 1080 x 1440; the four TikTok ones also 1080 x 1920) and stories

### C1 "It's not just hot flushes"  (Mon 9 Nov, TT Fri 13) · Sky: night, symptoms drawn as constellations · 9 slides
1. "Hot flushes get all the *attention*." (one bright star)  small: "Swipe for the rest of the NHS list"
2. "Here's what else is on the NHS list."
3. Constellation MIND: "Mood swings · Low mood · Anxiety · Memory and concentration (brain fog)"
4. Constellation SLEEP: "Getting to sleep · Staying asleep · Night sweats"
5. Constellation BODY: "Joint aches · Muscle pains · Headaches and migraines worse than usual · Palpitations"
6. Constellation SKIN AND HAIR: "Dry, itchy skin · Hair thinning"
7. "The ones people don't say out loud." "Vaginal dryness · More UTIs · Lower sex drive · Sensitive teeth or sore gums"
8. "One of the first signs is usually a *change* to your periods."
9. lockup + "Save this. Send it to her."
Every slide: small "Source: NHS". Caption:
"Perimenopause symptoms: it's not just hot flushes.
The NHS list includes mood swings, anxiety, brain fog, sleep problems, joint aches, headaches, palpitations, dry skin, hair thinning, vaginal dryness, UTIs, lower sex drive and even sore gums. And one of the first signs is usually a change to your periods.
Save this, and send it to someone who'd want to know.
#perimenopause #perimenopauseUK #menopausesymptoms"

### C2 "Before your GP appointment"  (Sat 14 Nov) · Paper: a lined notepad, handwriting · 8 slides
1. "Before your GP appointment, *write these down*."
2. "What's changed, and when it started."  (example in Caveat: "Waking at 3am since August")
3. "How often, and how bad."  ("Most nights. Bad enough to change the sheets.")
4. "Your periods: more often, less often, heavier, lighter."
5. "What seems to set it off."  ("Wine. Hot rooms. Stress at work.")
6. "How it's affecting work, sleep and the people around you."
7. "What you want to ask." big pink quote: "I think this could be perimenopause. What are my options?"
8. lockup + "Or let Clari keep the notes, and make a one-page summary for your GP." small: "Save this for the day you book."
Source line on slide 6: "NHS: symptoms can affect relationships, social life, family life and work." Caption:
"What to write down before a GP appointment about perimenopause.
What's changed and when, how often and how bad, your periods, what sets it off, how it's affecting your life, and the one question to ask.
Save this for the day you book.
#perimenopause #GPappointment #perimenopauseUK"

### C3 "Self Care Week: 7 small things"  (Mon 16 Nov, TT Fri 20) · Sky: each slide a different time of day, Monday dawn to Sunday night · 9 slides
1. "Self Care Week. 16 to 22 November." "7 days. 7 *small* things."
2. MON "Go to bed at the same time as last night."
3. TUE "Put a cold drink by the bed."
4. WED "Take a walk while it's still light."
5. THU "Tell one person how you're really doing."
6. FRI "Ten quiet minutes. Yoga, tai chi, or meditation."
7. SAT "Something with calcium. Milk, yoghurt, kale."
8. SUN "Write down how this week really felt."
9. lockup + "Save this for the week." small: "Ideas from NHS advice on menopause and perimenopause"
Caption:
"Self Care Week, 16 to 22 November. Seven small things, one a day.
All based on NHS advice for perimenopause and menopause: a regular sleep routine, a cold drink, regular exercise, talking to people, relaxing things like yoga or tai chi, calcium-rich food, and noticing how you feel.
Save this for the week.
#selfcareweek #perimenopause #perimenopauseUK"

### C4 "Brain fog, translated"  (Sat 21 Nov) · Sky: day, a pastel dictionary · 8 slides, each a dictionary entry
1. "Brain fog, *translated*."
2. "Colander" → "the spaghetti bowl with holes"
3. "Remote control" → "the telly button thing"
4. "Fridge" → "the cold cupboard"
5. "Her name (20 years of friendship)" → "Hello, *you*!"
6. "Why I came in here" → "..."
7. "Problems with memory and concentration are on the NHS list of perimenopause symptoms." Source: NHS
8. lockup + "Send this to the one who knows exactly what you mean."
Caption:
"Brain fog, translated. Which one is you?
Problems with memory and concentration are on the NHS list of perimenopause symptoms. Laugh about it, and write it down when it happens.
Send this to the one who knows exactly what you mean.
#brainfog #perimenopause #perimenopauseUK"

### C5 "Peri, meno, post: the words"  (Mon 23 Nov, TT Fri 27) · Sky: moon phases as the three stages · 8 slides
1. "Perimenopause. Menopause. Postmenopause." "What's the *difference*?"
2. PERIMENOPAUSE (waxing crescent): "When your periods become irregular."
3. MENOPAUSE (full moon): "When you haven't had a period for 12 months." small: "and you're not using hormonal contraception"
4. POSTMENOPAUSE (waning crescent): "The time after. Some symptoms can carry on, like joint pain and vaginal dryness."
5. "It usually happens between *45 and 55*."
6. "Early menopause: before 45. Premature menopause: before 40."
7. "There's no routine test for it." then "A doctor will usually go by your *age and symptoms*."
8. lockup + "Save this. Send it to her."
Source on each: NHS. Caption:
"Perimenopause, menopause, postmenopause: what's the difference?
NHS: perimenopause is when your periods become irregular. Menopause is when you haven't had a period for 12 months. After that, it's postmenopause. It usually happens between 45 and 55, but can happen earlier.
Save this for the next time someone asks.
#perimenopause #menopause #perimenopauseUK"

### C6 "Menopause at work: what's changing"  (Sat 28 Nov) · Sky: day, an office window, a 2026 to 2027 calendar · 7 slides
1. "Menopause at work." "Here's what's *changing*."
2. "Employers with 250 or more staff can now publish a menopause action plan."
3. "Right now it's *voluntary*."
4. "Subject to legislation, it becomes mandatory from spring 2027."
5. "The plans show the steps employers are taking to support employees experiencing menopause."
6. "Worth asking at work: do we have a menopause action plan?"
7. lockup + "Send this to a colleague."
Source on each: GOV.UK, Office for Equality and Opportunity, 2026. Caption:
"Menopause at work: what's changing.
Employers with 250 or more staff can now publish an action plan showing how they support employees experiencing menopause. It's voluntary for now, and subject to legislation it becomes mandatory from spring 2027.
Send this to a colleague.
Source: GOV.UK, Creating an action plan: guidance for employers.
#menopauseatwork #perimenopauseUK #menopause"

### C7 "When the NHS says to contact your GP"  (Mon 30 Nov, TT Fri 4 Dec) · Paper: the GP summary page style · 7 slides
1. "When the NHS says to *contact your GP*."
2. "You think you have symptoms of perimenopause or menopause and want to know your options."
3. "You have symptoms like a fast heartbeat (palpitations)."
4. "You still have periods, but you're bleeding more, not less, than before."
5. "You haven't had a period for 12 months or more, and you have any vaginal bleeding."
6. "Early advice can help reduce the effects on your health, relationships and work."
7. lockup + "Save this."
Source on each: NHS. Caption:
"When to contact your GP about perimenopause or menopause, according to the NHS.
If you want to know your options, if you have palpitations, if your bleeding is heavier than before, or if you have any bleeding 12 months or more after your last period.
Save this.
#perimenopause #perimenopauseUK #menopausesymptoms"

### C8 "What to say to a friend"  (Sat 5 Dec) · Sky: evening, two mugs on a windowsill, postcards · 8 slides, each a postcard "Instead of / Try"
1. "What to say to a friend who's struggling with *perimenopause*."
2. Instead of "You look fine!" try "How are you really sleeping?"
3. Instead of "It's just your age." try "That sounds hard. What's it like?"
4. Instead of "Have you tried yoga?" try "Do you want ideas, or just a moan?"
5. Instead of "I'm sure it's nothing." try "Have you told your GP? I'll come with you."
6. Instead of "Cheer up." try "You're not imagining it."
7. "The NHS suggests talking to people going through the same thing." Source: NHS
8. lockup + "Send this to her."
Caption:
"What to say to a friend who's struggling with perimenopause.
Swap \"you look fine\" for \"how are you really sleeping?\" The NHS suggests talking to other people going through the same thing. Sometimes that's you.
Send this to her.
#perimenopause #perimenopauseUK #friendship"

### C9 "What Clari keeps, and where"  (Mon 7 Dec) · App + Sky: night, real screens · 7 slides
1. "Your symptoms are nobody's business but *yours*."
2. "Stored on your phone." (real home.png)
3. "No account needed to start."
4. "You choose what to share, and when."
5. "A one-page summary for your GP, from your own notes." (real summary.png)
6. "Track symptoms, triggers and your cycle in under a minute a day." (real log.png)
7. lockup + "Free on the App Store and Google Play."
Caption:
"Where does your symptom data go? With Clari, it stays on your phone.
No account needed to start, you choose what to share and when, and you can turn your notes into a one-page summary for your GP.
Free on the App Store and Google Play.
#perimenopause #perimenopauseUK #privacy"

### Stories (1080 x 1920, one per day). Recurring templates so they feel like a series:
- **N** "On the NHS list" (Sky, a single constellation star, symptom name big, Source: NHS)
- **K** "Check-in" (Paper, a handwritten question on a sticky note)
- **W** "Self Care Week" (dawn sky, day number, one small thing)
- **A** "From the app" (real screen in a phone, one line)
- **T** "Today on our feed" (teaser frame from that day's post, title, "New post")
Every story: small mark.png top-left at 230 px from top, nothing in the bottom 400 px.
S09 Mon 9 Nov 08:15 K: "New week. First question: how did you sleep last night?"
S10 Tue 10 Nov 08:15 T: "3:07am. Duvet off. Duvet on. New on our feed."
S11 Wed 11 Nov 08:15 N: "Night sweats" / "Hot flushes that happen at night."
S12 Thu 12 Nov 18:15 T: "Told you're too young for perimenopause? What NICE says, by age. New on our feed."
S13 Fri 13 Nov 08:15 A: "Tap a symptom, then how strong it was. That's the whole check-in." (log.png)
S14 Sat 14 Nov 10:30 N: "Joint aches and muscle pains"
S15 Sun 15 Nov 10:30 K: "Sunday check-in: what was the hardest bit of this week? Write it down."
S16 Mon 16 Nov 08:15 W: "Self Care Week starts today. 16 to 22 November."
S17 Tue 17 Nov 08:15 W: "Day 2. Go to bed at the same time as last night."
S18 Wed 18 Nov 08:15 W: "Day 3. A walk while it's still light."
S19 Thu 19 Nov 08:15 W: "Day 4. Tell one person how you're really doing."
S20 Fri 20 Nov 08:15 W: "Day 5. Ten quiet minutes. Yoga, tai chi, or meditation."
S21 Sat 21 Nov 10:30 W: "Day 6. Something with calcium. Milk, yoghurt, kale."
S22 Sun 22 Nov 10:30 W: "Day 7. Write down how this week really felt."
S23 Mon 23 Nov 08:15 N: "Headaches and migraines" / "worse than usual"
S24 Tue 24 Nov 08:15 A: "Your week, as moons. One for every day you log." (home.png)
S25 Wed 25 Nov 08:15 N: "Sensitive teeth and sore gums" / "Yes, really."
S26 Thu 26 Nov 08:15 A: "Your data stays on your phone. No account needed to start." (homelogged.png)
S27 Fri 27 Nov 08:15 N: "Dry, itchy skin"
S28 Sat 28 Nov 10:30 K: "Heating on? NHS tip: keep your bedroom cool at night."
S29 Sun 29 Nov 10:30 K: "Sunday check-in: anything new this week? A new symptom, a new pattern?"
S30 Mon 30 Nov 08:15 N: "A change to your periods" / "Usually one of the first signs."
S01 Tue 1 Dec 08:15 K: "December. Party season. Notice what sets your flushes off."
S02 Wed 2 Dec 08:15 N: "Palpitations" / "The NHS says contact your GP if you have them."
S03 Thu 3 Dec 08:15 A: "A one-page summary for your GP, made from your own notes." (summary.png)
S04 Fri 4 Dec 08:15 N: "Hair thinning"
S05 Sat 5 Dec 10:30 K: "Christmas list idea: a cold water bottle by the bed. Not festive. Very useful."
S06 Sun 6 Dec 10:30 K: "Sunday check-in: how has your sleep been this week?"
S07 Mon 7 Dec 08:15 N: "Menopause" / "12 months without a period. Before that, it's perimenopause."
S08 Tue 8 Dec 08:15 T: "A new question at your NHS Health Check. New on our feed."

## 6. Verified fact bank (checked 6 Nov 2026). Use these words only.

- NHS (nhs.uk, symptoms page, reviewed 19 May 2026): symptoms include changes to periods (often one of the first signs: more or less often, heavier or lighter), hot flushes and night sweats, sleep problems, mood swings, low mood or depression, problems with memory or concentration, brain fog, weight gain, vaginal dryness, more UTIs, palpitations, weakening bones, urinary incontinence, headaches and migraines worse than usual, muscle aches and joint pains, hair thinning or loss, dry and itchy skin, reduced sex drive, sensitive teeth, painful gums or other mouth problems. Symptoms can affect relationships, social life, family life and work. Symptoms usually last 7 to 9 years, sometimes longer, and can change (hot flushes and night sweats may improve and be replaced by low mood and anxiety). Menopause is when you have not had a period for 12 months; after this it's postmenopause. Contact your GP if: you think you have symptoms and want to know your options; you have symptoms like palpitations; you still have periods but are bleeding more, not less; you have not had a period for 12 months or more and have any vaginal bleeding. "Early advice can help reduce the effects of menopause and perimenopause on your health, relationships and work."
- NHS "What are menopause and perimenopause?": perimenopause happens when your periods become irregular; menopause is when periods stop altogether; usually between 45 and 55 but can happen earlier; menopause is defined as not having a period for 12 months when not using hormonal contraception; "There's no routine test for perimenopause and menopause. A doctor may diagnose it based on your age and symptoms." Early menopause: before 45; premature: before 40 (NHS early menopause page).
- NHS things you can do: rest and regular sleep routines; balanced diet; calcium-rich food like milk, yoghurt and kale; regular exercise, weight-bearing; relaxing things such as yoga, tai chi or meditation; talk to other people going through the same thing; don't smoke; try not to drink more than the recommended alcohol limit. Hot flushes and night sweats: lightweight clothing; keep your bedroom cool at night; a cool shower, a fan or a cold drink; reduce stress; avoid or reduce potential triggers such as spicy food, caffeine, hot drinks, smoking and alcohol; exercise regularly; healthy weight. CBT can help low mood, anxiety, sleep and hot flushes.
- NICE NG23: over 45 with vasomotor symptoms and irregular periods, perimenopause can be diagnosed without lab tests; 40 to 45 with symptoms including a change in cycle, consider an FSH test; under 40 if menopause suspected (POI), diagnosis uses two FSH tests 4 to 6 weeks apart.
- NHSBSA HRT PPC: one-off £19.80 (the cost of two single items; each NHS prescription item usually £9.90); covers an unlimited number of certain HRT medicines for 12 months; could save money if you pay for NHS HRT 3 or more times in 12 months; not all HRT medicines covered; buy online or in person at some pharmacies.
- UK Government written statement, 23 Oct 2025 (Baroness Merron): local authorities asked to introduce a new menopause element to NHS Health Checks in 2026, so eligible women aged 40 to 55 can access advice about menopause and perimenopause more easily. NHS Health Checks: every 5 years, ages 40 to 74 without pre-existing heart conditions.
- GOV.UK "Creating an action plan: guidance for employers" (Office for Equality and Opportunity, first published 4 March 2026): employers with 250+ employees have the option to publish a voluntary action plan; subject to legislation these become mandatory from spring 2027; plans show steps to support employees experiencing menopause (and close the gender pay gap).
- Mehta et al, JAMA Network Open, 2026 (University of Maryland, Hswen): compared clinical notes (UCSF, from 2M+ records) with top r/menopause Reddit posts; cognitive impairment in about 20% of Reddit posts vs about 5% of clinic visits (almost 4-fold); emotional wellbeing also far more common online.
- Self Care Week 2026: 16 to 22 November.
- Clari: symptom data stored on the phone; no account needed to start; you choose what to share; one-page GP Appointment Summary (Pro feature: say "a summary for your GP", never "free summary"); check-in takes under a minute; tracks symptoms with severity, triggers (alcohol, caffeine, stress etc.), cycle, mood, energy, medications. Free on the App Store and Google Play (free to start).
