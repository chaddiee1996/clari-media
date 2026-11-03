"""Clari November stories, highlight frames and highlight covers.

python3 stories.py OUT
Writes:
  OUT/stories/<DD-MM-YY - time>.png   (+ .mp4 for animated ones, made separately)
  OUT/highlights/Start here 1.png ...
  OUT/covers/<name>.png
Every page goes through the same clipping and safe-zone checks as the feed posts.
"""
import json, pathlib, sys
from playwright.sync_api import sync_playwright
import nov
from nov import U, e, icon, page, SAFE, CHECK_JS

W, H = 1080, 1920
L, R = 96, 96
TOP = 260          # below the story progress bar and profile name
BOT = H - 360      # above the reply bar

CSS = """
.c{display:block}
.night{background:radial-gradient(80% 45% at 85% 5%,#3E2670 0%,rgba(62,38,112,0) 70%),linear-gradient(180deg,#0E0620 0%,#1C0C3B 50%,#33175F 100%);color:var(--moon)}
.lilac{background:radial-gradient(90% 50% at 100% 0%,#F1E8FD 0%,rgba(241,232,253,0) 65%),linear-gradient(170deg,#D9C6F4 0%,#E9D9F2 55%,#F5DCE5 100%);color:var(--plum)}
.butter{background:radial-gradient(80% 50% at 0% 0%,#FFF1B8 0%,rgba(255,241,184,0) 70%),#FFE27A;color:var(--plum)}
.blush{background:radial-gradient(80% 50% at 100% 100%,#F8D0DB 0%,rgba(248,208,219,0) 70%),#F2B4C5;color:var(--plum)}
.paper{background:radial-gradient(80% 50% at 100% 0%,#F6E6D6 0%,rgba(246,230,214,0) 70%),var(--cream);color:var(--plum)}
.dawn{background:linear-gradient(180deg,#2B1A5E 0%,#7B4E9E 45%,#E9A6A6 85%,#F6C9B0 100%);color:var(--moon)}
.bg{position:absolute;inset:0}
.t{position:absolute;left:96px;right:96px;font-size:120px;font-weight:430}
.t em{font-style:italic;font-weight:370}
.night .t em,.dawn .t em{color:#F7C6D3}
.lilac .t em,.paper .t em{color:var(--violet)}
.blush .t em,.butter .t em{color:#8A2F5A}
.b{position:absolute;left:96px;right:96px;font-size:46px;line-height:1.38;font-weight:480}
.night .b,.dawn .b{color:rgba(255,243,214,.88)}
.lilac .b,.paper .b,.blush .b,.butter .b{color:#4A2F63}
.hand{position:absolute;font-family:H;font-size:64px;line-height:1.05}
.small{position:absolute;font-size:28px;font-weight:600;opacity:.72}
.moon{position:absolute;width:150px;height:150px;border-radius:50%;box-shadow:inset -34px 10px 0 0 #FFEFC9;transform:rotate(-20deg);filter:drop-shadow(0 0 30px rgba(255,239,201,.35))}
.star{position:absolute;width:6px;height:6px;border-radius:50%;background:#FFF3D6}
.big{position:absolute;left:80px;right:80px;font-family:F;font-variation-settings:"opsz" 144,"SOFT" 50;font-weight:500;letter-spacing:-.04em;line-height:.86}
.frame{position:absolute;left:150px;right:150px;border:4px dashed rgba(36,16,63,.0);border-radius:40px}
.card{position:absolute;left:84px;right:84px;background:var(--paper);border-radius:44px;padding:70px 64px;box-shadow:0 60px 100px -50px rgba(60,30,110,.55);overflow:hidden}
.card::before{content:"";position:absolute;left:0;right:0;top:0;height:14px;background:linear-gradient(90deg,#6B3FA0,#C8628A)}
.ct{font-family:IS;font-size:84px;line-height:1;color:var(--plum)}
.ct em{font-style:italic;color:var(--violet)}
.rt{font-family:IN;font-size:44px;line-height:1.3;color:#2A1D40;font-weight:500}
"""

def stars(n=26, maxy=900):
    return "".join(f'<div class="star" style="left:{(i * 263 + 40) % W}px;top:{60 + (i * 97) % maxy}px;opacity:{.25 + (i % 4) * .15:.2f};transform:scale({.6 + (i % 3) * .4:.1f})"></div>' for i in range(n))

def brand_at(y, dark):
    return nov.brand(L, y, dark)

def handle(dark):  # small brand line at the bottom of the safe area
    return brand_at(BOT - 50, dark)

def blossom(x, y, w, flip=False, rot=0, op=1):
    return nov.blossom(x, y, w, flip, rot, op)

def phone(src, w, style):
    return nov.phone(src, w, style)

# Each story: (filename, theme, body html, sticker instructions, highlight)
STORIES = []
def story(name, theme, body, sticker, highlight=None, caption=None):
    STORIES.append(dict(name=name, theme=theme, body=body, sticker=sticker, highlight=highlight))

# 1. Poll: sleep
story("04-11-26 - 7pm", "night", f"""{stars()}
<div class="moon" style="right:120px;top:{TOP + 20}px"></div>
<div class="t F" style="top:{TOP + 260}px">Be honest.<br><em>How did you sleep last night?</em></div>
<div class="hand" style="left:96px;top:{BOT - 210}px;color:#F7C6D3">Tap your answer</div>
{handle(True)}""",
 "POLL sticker in the empty space under the question. Options: \"Badly\" and \"Not bad\".", "Symptoms")

# 2. Quiz: how long
story("06-11-26 - 8pm", "lilac", f"""
{blossom(W - 600, TOP - 40, 640, rot=4, op=.95)}
<div class="t F" style="top:{TOP + 300}px;font-size:110px">Quick quiz. <em>How long do perimenopause symptoms usually last?</em></div>
{handle(False)}""",
 "QUIZ sticker under the question. Options: \"About a year\", \"2 to 3 years\", \"7 to 9 years\". Mark \"7 to 9 years\" as correct.", "Symptoms")

# 3. Answer
story("07-11-26 - 7pm", "blush", f"""
<div class="small" style="left:96px;top:{TOP + 20}px;font-size:36px;opacity:.85">Yesterday's answer</div>
<div class="big" style="top:{TOP + 170}px;font-size:400px">7&#8209;9</div>
<div class="t F" style="top:{TOP + 600}px;font-size:120px"><em>years.</em></div>
<div class="b" style="top:{TOP + 800}px">That's how long symptoms usually last. Sometimes longer, and they can change along the way. A long time to rely on memory.</div>
<div class="small" style="left:96px;top:{BOT - 130}px">Source: nhs.uk</div>
{handle(False)}""",
 "No sticker needed. Optional: a SLIDER sticker under the text with the question \"Did that surprise you?\"", "Symptoms")

# 4. New feature (needs new screenshot app-calendar-log.png, falls back to app-calendar.png)
story("08-11-26 - 6pm", "night", f"""{stars(14, 300)}
<div class="t F" style="top:{TOP}px;font-size:112px">Missed a day? <em>Now you can fill it in.</em></div>
<div class="b" style="top:{TOP + 390}px">Tap any past day in your calendar. Update Clari to 1.5.4.</div>
{phone('FEATURE_SHOT', 470, f"left:{(W - 470) // 2}px;top:{TOP + 640}px;transform:rotate(-3deg)")}
{handle(True)}""",
 "LINK sticker over the top of the phone, with the link clariapp.co (it works for iPhone and Android). Sticker text: \"Update Clari\".", "New in Clari")

# 5. This or that
story("10-11-26 - 8pm", "butter", f"""
<div class="t F" style="top:{TOP + 120}px">Right now, <em>are you…</em></div>
<div style="position:absolute;left:96px;right:96px;top:{TOP + 520}px;display:flex;gap:24px">
  <div style="flex:1;height:360px;border-radius:40px;background:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;box-shadow:0 30px 60px -36px rgba(36,16,63,.45)">{icon('thermometer-hot', 130, '#C8628A')}<div style="font-size:52px;font-weight:700">Too hot</div></div>
  <div style="flex:1;height:360px;border-radius:40px;background:var(--plum);color:var(--moon);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:24px;box-shadow:0 30px 60px -36px rgba(36,16,63,.6)">{icon('snowflake', 130, '#CBB7F2')}<div style="font-size:52px;font-weight:700">Too cold</div></div>
</div>
<div class="hand" style="left:96px;top:{TOP + 960}px;color:#8A2F5A">or both, in the same hour?</div>
{handle(False)}""",
 "POLL sticker below \"or both, in the same hour?\". Options: \"Too hot\" and \"Too cold\".", "Symptoms")

# 6. Share frame for the 11 Nov post
story("11-11-26 - 7pm", "lilac", f"""
<div class="t F" style="top:{TOP}px;font-size:96px">New post: <em>things women still get told</em></div>
<img src="{U('img/feed/2026-11-11-told-ig-01.jpg')}" style="position:absolute;left:230px;top:{TOP + 330}px;width:620px;border-radius:28px;transform:rotate(-2.5deg);box-shadow:0 70px 110px -50px rgba(20,8,40,.75)">
<div class="hand" style="left:96px;top:{BOT - 140}px;color:var(--rose)">Tap to read the replies</div>
{handle(False)}""",
 "LINK sticker on top of the post picture. To get the link: open the post on Instagram, tap the three dots, Copy link. Sticker text: \"See the post\". Post this story about an hour after the post goes live.", "Myths")

# 7. Question box
story("13-11-26 - 8pm", "night", f"""{stars()}
<div class="t F" style="top:{TOP + 160}px">What's one symptom <em>nobody warned you about?</em></div>
<div class="hand" style="left:96px;top:{BOT - 210}px;color:#F7C6D3">We read every answer</div>
{handle(True)}""",
 "QUESTIONS sticker under the headline. Prompt text: \"Type it here\".", "Symptoms")

# 8. Self Care Week
story("16-11-26 - 7pm", "dawn", f"""{stars(12, 400)}
<div class="small" style="left:96px;top:{TOP + 20}px;font-size:36px;opacity:.9">It's Self Care Week, 16 to 22 November</div>
<div class="t F" style="top:{TOP + 140}px">How much time did you get <em>for you</em> today?</div>
{handle(True)}""",
 "EMOJI SLIDER sticker under the headline. Pick the moon or the heart emoji.", "Self care")

# 9. Share frame for the 17 Nov post
story("17-11-26 - 8pm", "night", f"""{stars(14, 260)}
<div class="t F" style="top:{TOP}px;font-size:96px">Night sweats? <em>Five notes for tonight.</em></div>
<img src="{U('img/feed/2026-11-17-notes-ig-01.jpg')}" style="position:absolute;left:230px;top:{TOP + 330}px;width:620px;border-radius:28px;transform:rotate(-2.5deg);box-shadow:0 70px 110px -50px rgba(20,8,40,.75)">
<div class="hand" style="left:96px;top:{BOT - 140}px;color:#F7C6D3">Save it for later</div>
{handle(True)}""",
 "LINK sticker on top of the post picture. To get the link: open the post on Instagram, tap the three dots, Copy link. Sticker text: \"See the post\". Post this story about an hour after the post goes live.", "Self care")

# 10. GP tip card
story("19-11-26 - 8pm", "lilac", f"""
<div class="card" style="top:{TOP + 60}px">
  <div class="ct">Booking a <em>GP appointment?</em></div>
  <div style="height:40px"></div>
  <div class="rt">Ask reception which GP is best to see about menopause.</div>
  <div style="height:28px;border-bottom:2px solid #EFE7F6"></div><div style="height:28px"></div>
  <div class="rt">If you can, ask for a longer appointment.</div>
  <div style="height:36px"></div>
  <div style="font-family:IN;font-size:28px;color:#7A6894;font-weight:500">Tip from Nuffield Health</div>
</div>
<div class="hand" style="left:96px;top:{TOP + 1000}px;color:var(--plum)">Send this to a friend who's booking</div>
{handle(False)}""",
 "No sticker needed. Leave it clean so people screenshot it.", "GP visits")

# 11. Share frame for the 20 Nov reel
story("20-11-26 - 7pm", "dawn", f"""{stars(10, 300)}
<div class="t F" style="top:{TOP}px;font-size:96px">New reel: <em>one day, hour by hour</em></div>
<img src="{U('img/feed/2026-11-20-reel-cover.jpg')}" style="position:absolute;left:310px;top:{TOP + 320}px;width:460px;border-radius:28px;transform:rotate(-2.5deg);box-shadow:0 70px 110px -50px rgba(20,8,40,.75)">
<div class="hand" style="left:96px;top:{BOT - 140}px;color:#FFF3D6">Which hour is yours?</div>
{handle(True)}""",
 "LINK sticker on top of the post picture. To get the link: open the post on Instagram, tap the three dots, Copy link. Sticker text: \"See the post\". Post this story about an hour after the post goes live.", None)

# 12. Quiz: blood test
story("22-11-26 - 7pm", "paper", f"""
<div class="t F" style="top:{TOP + 160}px;font-size:110px">Over 45 with symptoms. <em>Do you need a blood test to be diagnosed?</em></div>
{handle(False)}""",
 "QUIZ sticker under the question. Options: \"Yes, always\" and \"Not usually\". Mark \"Not usually\" as correct.", "GP visits, Myths")

# 13. Answer: NICE
story("24-11-26 - 8pm", "lilac", f"""
<div class="small" style="left:96px;top:{TOP + 20}px;font-size:36px;opacity:.85">Sunday's answer</div>
<div class="t F" style="top:{TOP + 110}px;font-size:150px"><em>Not usually.</em></div>
<div class="b" style="top:{TOP + 420}px">For women over 45 with symptoms, NICE says perimenopause can be diagnosed without a blood test.</div>
<div class="b" style="top:{TOP + 720}px">Between 40 and 45, a blood test may be considered.</div>
<div class="small" style="left:96px;top:{BOT - 130}px">Source: NICE guideline NG23</div>
{handle(False)}""",
 "No sticker needed.", "GP visits, Myths")

# 14. Share frame for 26 Nov grid
story("26-11-26 - 7pm", "paper", f"""
<div class="t F" style="top:{TOP}px;font-size:96px">16 symptoms. <em>Which one caught you out?</em></div>
<img src="{U('img/feed/2026-11-26-which-one-ig.jpg')}" style="position:absolute;left:230px;top:{TOP + 330}px;width:620px;border-radius:28px;transform:rotate(-2.5deg);box-shadow:0 70px 110px -50px rgba(20,8,40,.75)">
<div class="hand" style="left:96px;top:{BOT - 140}px;color:var(--rose)">Comment the number on the post</div>
{handle(False)}""",
 "LINK sticker on top of the post picture. To get the link: open the post on Instagram, tap the three dots, Copy link. Sticker text: \"See the post\". Post this story about an hour after the post goes live.", "Symptoms")

# 15. How it works
story("28-11-26 - 8pm", "lilac", f"""
<div class="t F" style="top:{TOP}px;font-size:104px">A minute a day, <em>that's it.</em></div>
<div class="b" style="top:{TOP + 270}px">Tap how you feel. The moon fills as a symptom gets stronger.</div>
{phone('app-log.png', 470, f"left:{(W - 470) // 2}px;top:{TOP + 520}px;transform:rotate(3deg)")}
{handle(False)}""",
 "LINK sticker over the phone, with the link clariapp.co. Sticker text: \"Try Clari free\".", "Start here")

# 16. Month end
story("30-11-26 - 7pm", "night", f"""{stars()}
{blossom(-60, TOP - 60, 640, flip=True, rot=-4, op=.9)}
<div class="t F" style="top:{TOP + 380}px">November, done. <em>Thank you for being here.</em></div>
<div class="b" style="top:{TOP + 780}px">What should we cover in December?</div>
{handle(True)}""",
 "POLL sticker under the question. Options: \"Sleep\" and \"GP visits\". Or use a QUESTIONS sticker if you'd rather hear ideas.", None)

# Evergreen highlight frames for "Start here"
HIGHLIGHT_FRAMES = [
    ("Start here 1", "night", f"""{stars()}
<div class="moon" style="right:120px;top:{TOP + 20}px"></div>
<div class="t F" style="top:{TOP + 300}px">Hello. <em>This is Clari.</em></div>
<div class="b" style="top:{TOP + 560}px">A private symptom diary for perimenopause. Tap how you feel, see your patterns, and walk into your GP appointment with the whole picture.</div>
{handle(True)}"""),
    ("Start here 2", "lilac", f"""
<div class="t F" style="top:{TOP}px;font-size:104px">Tap how you feel. <em>Watch the moon fill.</em></div>
<div class="b" style="top:{TOP + 270}px">One tap for mild, again as it gets stronger.</div>
{phone('app-log.png', 470, f"left:{(W - 470) // 2}px;top:{TOP + 470}px;transform:rotate(-3deg)")}
{handle(False)}"""),
    ("Start here 3", "paper", f"""
<div class="t F" style="top:{TOP}px;font-size:104px">One summary <em>for your GP.</em></div>
<div class="b" style="top:{TOP + 270}px">30, 60 or 90 days of notes on one page.</div>
{phone('app-summary.png', 470, f"left:{(W - 470) // 2}px;top:{TOP + 470}px;transform:rotate(3deg)")}
{handle(False)}"""),
    ("Start here 4", "night", f"""{stars()}
<div style="position:absolute;left:96px;top:{TOP + 160}px">{icon('lock-simple', 170, '#F7C6D3')}</div>
<div class="t F" style="top:{TOP + 420}px">Your symptom data <em>stays on your phone.</em></div>
<div class="b" style="top:{TOP + 830}px">No account needed. Free to download on the App Store and Google Play.</div>
{handle(True)}"""),
]
HIGHLIGHT_STICKERS = {"Start here 4": "LINK sticker under the text, with the link clariapp.co. Sticker text: \"Get Clari\"."}

COVERS = [
    ("Start here", "moon-stars"), ("Symptoms", "thermometer"), ("GP visits", "stethoscope"),
    ("Myths", "chat-circle-text"), ("Self care", "hand-heart"), ("New in Clari", "bell-ringing"),
]

def cover(icn):
    # Instagram shows the centre of a 1080x1920 image as a circle. Keep the icon inside the middle 600px.
    return f"""<div class="bg" style="background:radial-gradient(60% 34% at 50% 50%,#3E2670 0%,#24103F 70%)"></div>
<div style="position:absolute;left:50%;top:50%;width:560px;height:560px;margin:-280px 0 0 -280px;border-radius:50%;
  background:radial-gradient(circle at 38% 32%,#FFF8EA 0%,#F3E6F7 60%,#E3D2F4 100%);display:flex;align-items:center;justify-content:center;
  box-shadow:inset 0 -18px 40px rgba(107,63,160,.18)">{icon(icn, 300, '#3A1C63')}</div>"""

def main():
    out = pathlib.Path(sys.argv[1])
    feat = sys.argv[2] if len(sys.argv) > 2 else "app-calendar.png"
    for d in ("stories", "highlights", "covers"):
        (out / d).mkdir(parents=True, exist_ok=True)
    tmp = nov.HERE / "_s.html"
    problems = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        def shot(body, theme, path, check=True):
            body = body.replace("FEATURE_SHOT", feat)
            doc = page(W, H, CSS, f'<div class="bg {theme}"></div>{body}<div class="grain{" l" if theme in ("night","dawn") else ""}"></div>', "st")
            doc = doc.replace('<div class="c">', f'<div class="c {theme}">', 1).replace("<body ", f"<body data-safe='{json.dumps(SAFE['st'])}' ", 1)
            tmp.write_text(doc)
            pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            if check:
                for m in pg.evaluate(CHECK_JS):
                    problems.append(f"{path.name}: {m}")
            pg.screenshot(path=str(path), type="png")
        for st in STORIES:
            shot(st["body"], st["theme"], out / "stories" / f"{st['name']}.png")
        for name, theme, body in HIGHLIGHT_FRAMES:
            shot(body, theme, out / "highlights" / f"{name}.png")
        for name, icn in COVERS:
            shot(cover(icn), "night", out / "covers" / f"{name}.png", check=False)
        b.close()
    tmp.unlink(missing_ok=True)
    (out / "stories.json").write_text(json.dumps([{k: v for k, v in s.items() if k != "body"} for s in STORIES], indent=1))
    print("\n".join(problems) or "all clear")

if __name__ == "__main__":
    main()
