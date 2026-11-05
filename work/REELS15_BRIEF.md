# Clari: 15 reels brief (shared by all build agents)

## Who and what
Clari is a UK perimenopause symptom diary app (iOS + Android, free to start). Audience: women roughly 38 to 55 in the UK. Made by women-first thinking: warm, frank, never patronising, never clinical-cold, never "girlboss" cliché. No men, partners or husbands in any concept. Brand plum #5B2A86, cream #FFF1E5, ink #1A1A1A, but each reel may use its own palette from its look as long as the end card carries the Clari moon mark (crescent) and the word "Clari".

## The client's hard rules (break one and the reel is rejected)
- NO em dashes or en dashes anywhere in on-screen text. Use full stops, commas, "to".
- NO AI-sounding words: neon, unlock, empower, journey, game-changer, elevate, delve, navigate, embrace, "let's dive in", "you've got this", sparkle emoji vibes.
- NO templated layouts. Every reel must look like a different studio made it.
- Do NOT default to left-aligned text. Each reel has an assigned alignment (below). Follow it.
- Phone-first type: nothing smaller than 48px on a 1080x1920 frame. Labels 58 to 64px heavy. Headlines around 130 to 160px heavy. Solid ink or solid colour text, never grey, never hairline/thin serifs. High contrast always.
- Keep text inside safe area: top 220px and bottom 380px clear of key text (IG/TikTok UI), right 140px clear.
- Facts: ONLY the verified facts listed below, worded as given. Never invent stats. Never say diagnose, detect, treat, cure. Clari "tracks", "logs", "notes", "keeps a record". No red/amber/green scores.
- No "comment a word" CTAs. CTAs allowed: "Save this", "Send this to her", "Send it to the friend who...".
- Nothing from previous Clari templates (templates/nov, templates/v2, notes-v3, notes-v4 looks) may be reused. notes-v4 is a quality bar only.

## Verified facts (with source to show small on screen as "Source: ...")
- NICE NG23: over 45 with symptoms (e.g. hot flushes, irregular periods) perimenopause can be diagnosed without a blood test. 40 to 45: an FSH blood test can be considered. Under 40 (suspected early menopause / POI): diagnosed with two FSH blood tests 4 to 6 weeks apart, never one alone. Source: NICE guideline NG23.
- NHS symptom list (Cambridge University Hospitals NHS): hot flushes, night sweats, problems with memory or concentration (brain fog), mood changes, anxiety, palpitations, headaches, joint pain, skin changes, sleep problems, lower sex drive, vaginal dryness, recurrent UTIs, mouth problems. Symptoms usually start months or years before periods stop. Source: Cambridge University Hospitals NHS.
- NHS Wales: menopause usually happens 45 to 55; average age in the UK is 51; about 1 in 100 women go through it before 40; symptoms last around 4 years after the last period (some much longer). Source: NHS Wales.
- HRT prescription prepayment certificate (England): £19.80, covers certain HRT medicines for 12 months, buy online or at some pharmacies. Source: NHSBSA.
- NHS Health Check (England): from 2026 will include questions on menopause for women aged 40 to 55. Source: UK Government, Oct 2025.
- Workplace: government menopause action plan guidance published 2026; employers with 250+ staff encouraged to publish one, expected to become required in 2027. Source: UK Government.
- Self Care Week: 16 to 22 November 2026.
- Alcohol can trigger hot flushes for some women. Source: Alcohol Change UK / NHS.
- Night sweats self-help (NHS): keep bedroom cool, wear light cotton, layers you can remove, keep cold water by the bed, cut down on alcohol, caffeine and spicy food. Source: NHS.
- Clari facts: keeps symptom data on your phone, no account needed to start, you choose what to share, makes a summary for your GP from your own notes. Free on App Store and Google Play.

## Process for EVERY reel (claude-video-studio skill, at /home/claude/clari-media/.claude/skills/claude-video-studio)
1. Read SKILL.md once, then the assigned look's styles/<look>/STYLE.md and its index.html reference piece. Build FROM that look's motion language, not a generic layout.
2. Project folder: /home/claude/clari-media/work/<reel-id>/ (use scripts/new_project.sh if helpful). Write BRIEF.md + storyboard.
3. 1080x1920, 30fps, 18 to 30s. Voiced reels: length = VO length + about 3s end card. Use measured VO cues (silence gaps listed per reel) so each line of text lands on its spoken phrase. Voiced reels also show the spoken words as on-screen captions/headlines (most people watch muted).
4. Stills: render 3 stills (scripts/stills.sh), LOOK at them with Read, score honestly out of 10 for: readability at phone size, originality, polish. Fix until all at least 8. Then check a downscaled 360px-wide version still reads.
5. Render with HF_WORKERS=1 (machine has 2 CPUs; other agents render too). Run scripts/pacing_check.py (use --end-hold for the end card). Fix dead gaps over 1s with purposeful motion, not wiggle.
6. Music: compose a UNIQUE bed per reel in numpy (look at /tmp/claude-0/-home-claude/7122b9f6-ef9c-5a65-8b0a-af50e22d1cd8/scratchpad/audio/bed.py as an example only; do not reuse its sound). Different key, tempo, instrument character per reel (e.g. music-box, warm Rhodes chords, soft plucked bass groove, brushed percussion, synth pad + clock ticks, marimba, felt piano, lo-fi drum loop). Add a few tasteful SFX hits on key moments. 48kHz.
7. Mix: voiced reels: VO loudnorm I=-16, bed around volume 0.15 under voice (duck), amix normalize=0, alimiter 0.89. Text-only reels: music is the star, loudnorm the whole mix to about I=-14. Mux AAC 192k 48k into the MP4.
8. Final file: /home/claude/clari/Reels 15/<NN> - <Title>.mp4 (NN = 01 to 15). Create the folder if missing.
9. Write /home/claude/clari-media/work/<reel-id>/CAPTION.md: IG caption (warm, human, 2 to 4 short lines, no em dashes, 3 hashtags max e.g. #perimenopause #menopauseuk + one topical), and note "AI voice: yes/no".
10. Do not touch git, .replit, eas.json, Metricool, or ElevenLabs. Do not generate any audio with ElevenLabs. Do not commit.
