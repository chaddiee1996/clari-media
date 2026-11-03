POSTS = {
    "2026-11-08-new": feature,
    "2026-11-11-told": thread,
    "2026-11-14-age": ruler,
    "2026-11-17-notes": notes,
    "2026-11-23-checklist": checklist,
    "2026-11-26-which-one": grid,
    "2026-11-20-reel-cover": cover_day,
    "2026-11-29-reel-cover": cover_page,
}

CHECK_JS = r"""
() => {
  const W = innerWidth, H = innerHeight, kind = document.body.dataset.kind;
  const S = JSON.parse(document.body.dataset.safe);
  const bad = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    if (!n.textContent.trim()) continue;
    const el = n.parentElement;
    if (el.closest('.deco')) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') continue;
    const r = document.createRange(); r.selectNodeContents(n);
    for (const b of r.getClientRects()) {
      if (b.width < 1) continue;
      const rlim = (kind === 'tt' && b.bottom < 700) ? 60 : S[2];
      if (b.left < S[0] - 2 || b.top < S[1] - 2 || b.right > W - rlim + 2 || b.bottom > H - S[3] + 2)
        bad.push(`unsafe: "${n.textContent.trim().slice(0, 40)}" at ${Math.round(b.left)},${Math.round(b.top)},${Math.round(b.right)},${Math.round(b.bottom)}`);
    }
    // clipped by any ancestor with overflow hidden
    let a = el;
    while (a && a !== document.body) {
      const s = getComputedStyle(a);
      if ((s.overflow !== 'visible') && a.classList && !a.classList.contains('c')) {
        if (a.scrollHeight > a.clientHeight + 1 || a.scrollWidth > a.clientWidth + 1) bad.push(`clipped in ${a.className}: "${n.textContent.trim().slice(0, 40)}"`);
      }
      a = a.parentElement;
    }
  }
  // text boxes that overlap each other (direct text holders only)
  const holders = [...document.querySelectorAll('body *')].filter(x => [...x.childNodes].some(c => c.nodeType === 3 && c.textContent.trim()));
  const rects = holders.map(x => { const r = document.createRange(); r.selectNodeContents(x); return [x, [...r.getClientRects()]]; });
  for (let i = 0; i < rects.length; i++) for (let j = i + 1; j < rects.length; j++) {
    const [x, A] = rects[i], [y, B] = rects[j];
    if (x.contains(y) || y.contains(x)) continue;
    for (const a of A) for (const b of B) {
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 4 && oy > 4) bad.push(`overlap: "${x.textContent.trim().slice(0, 30)}" / "${y.textContent.trim().slice(0, 30)}"`);
    }
  }
  const imgs = [...document.querySelectorAll('img, .note, .phone')].filter(i => !i.closest('.brand') && !i.closest('.deco') && !i.classList.contains('deco') && !i.closest('.note,.card,.in,.out') || i.classList.contains('note'));
  for (const [x, A] of rects) for (const im of imgs) {
    if (im.contains(x) || x.closest('.deco')) continue;
    const b = im.getBoundingClientRect();
    for (const a of A) {
      const ox = Math.min(a.right, b.right) - Math.max(a.left, b.left), oy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ox > 4 && oy > 4) bad.push(`text on image: "${x.textContent.trim().slice(0, 30)}"`);
    }
  }
  return [...new Set(bad)];
}
"""

def main():
    out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    names = sys.argv[2:] or list(POSTS)
    kinds = ["ig", "tt"]
    tmp = HERE / "_p.html"
    problems = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name in names:
            fn = POSTS[name]
            for kind in getattr(fn, 'kinds', kinds):
                w, h = SIZES[kind]
                css, slides = fn(kind)
                pg = b.new_page(viewport={"width": w, "height": h})
                for i, body in enumerate(slides):
                    doc = page(w, h, css, body, kind).replace("<body ", f"<body data-safe='{json.dumps(SAFE[kind])}' ", 1)
                    tmp.write_text(doc)
                    pg.goto(tmp.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
                    for m in pg.evaluate(CHECK_JS):
                        problems.append(f"{name} {kind} {i + 1}: {m}")
                    suffix = f"-{i + 1:02d}" if len(slides) > 1 else ""
                    pg.screenshot(path=str(out / f"{name}-{kind}{suffix}.jpg"), type="jpeg", quality=94)
                pg.close()
        b.close()
    tmp.unlink(missing_ok=True)
    print("\n".join(problems) or "all clear")
    sys.exit(1 if problems else 0)

if __name__ == "__main__":
    main()
