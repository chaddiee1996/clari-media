# Clari reel templates (Remotion)

Compositions: `Launch` (launch reel), `Joints` (World Menopause Day, 18 Oct 2026).

Render (1080x1920, 30fps, silent; audio is mixed afterwards with ffmpeg):

    npm install
    COMP=Joints node render.mjs          # -> out/Joints-silent.mp4
    COMP=Joints node stills.mjs 0.5 5 12 # preview stills

Browser: Chromium headless shell at /opt/pw-browsers/chromium_headless_shell-1194, gl 'swangle', concurrency 2.
Style rules: no em dashes, no "neon", British English, ASA-safe words (track, log, notice patterns; never treat, diagnose, detect).
Audio: mix music under, loudnorm to -14 LUFS, 48 kHz AAC (Instagram limit).
