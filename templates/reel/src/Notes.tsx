import React from 'react';
import { AbsoluteFill, Img, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { clamp, ease, easeIn } from './kit';

/* Series: Sourced in 30 seconds. "The symptoms that never make it into the notes."
   Voice: Eleanor (ElevenLabs). Source: Hswen et al., JAMA Network Open, reported by STAT, 27 Aug 2026.
   Look: a researcher's desk. Paper, ink, yellow highlighter, red pen. Text kept between y=230 and y=1400. */

const F = 30;
const s = (t: number) => Math.round(t * F);
const SERIF = 'NFrau, Georgia, serif';
const MONO = 'NMono, ui-monospace, monospace';
const HAND = 'NKalam, cursive';
const SANS = 'NFig, sans-serif';
const INK = '#16182C';
const PAPER = '#F3F1EA';
const HI = '#F6E05E';
const RED = '#D43A2C';

// cue times (seconds) measured from the voice take's pauses
const C = {
  start: 0, brain: 7.44, memory: 8.6, words: 9.96, four: 12.29, mood: 16.94, three: 18.13,
  real: 20.23, written: 21.99, so: 24.22, when: 25.73, much: 27.65, take: 28.82, clari: 30.29,
};
const VO_END = 31.84;
export const NOTES_FRAMES = s(VO_END + 3.2);

const fh = { done: false };
const Fonts: React.FC = () => {
  const [h] = React.useState(() => (fh.done ? null : delayRender('notesfonts')));
  React.useEffect(() => {
    const faces = [
      new FontFace('NFrau', `url(${staticFile('fraunces-full.woff2')})`, { weight: '100 900' }),
      new FontFace('NFrau', `url(${staticFile('fraunces-full-italic.woff2')})`, { weight: '100 900', style: 'italic' }),
      new FontFace('NMono', `url(${staticFile('dm-mono-500.woff2')})`, { weight: '500' }),
      new FontFace('NKalam', `url(${staticFile('kalam-700.woff2')})`, { weight: '700' }),
      new FontFace('NFig', `url(${staticFile('figtree.woff2')})`, { weight: '300 900' }),
    ];
    Promise.all(faces.map((x) => x.load().then((ff) => (document as any).fonts.add(ff)))).then(() => {
      fh.done = true;
      if (h !== null) continueRender(h);
    });
  }, [h]);
  return null;
};

const r = (f: number, a: number, b: number, e = ease) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: e });
const win = (f: number, a: number, b: number) => f >= s(a) && f < s(b);

/** reveals text word by word from a start time, each word sliding up out of a mask */
const Rise: React.FC<{ text: string; at: number; style?: React.CSSProperties; step?: number; hi?: string[] }> = ({ text, at, style, step = 2.2, hi = [] }) => {
  const f = useCurrentFrame();
  const words = text.split(' ');
  return (
    <span style={style}>
      {words.map((w, i) => {
        const p = r(f, s(at) + i * step, s(at) + i * step + 12);
        return (
          <span key={i} style={{ display: 'inline-block', overflow: 'hidden', verticalAlign: 'bottom', paddingBottom: '0.08em', marginBottom: '-0.08em' }}>
            <span style={{ display: 'inline-block', transform: `translateY(${(1 - p) * 105}%)`, fontStyle: hi.includes(w) ? 'italic' : undefined }}>
              {w}{i < words.length - 1 ? ' ' : ''}
            </span>
          </span>
        );
      })}
    </span>
  );
};

const Paper: React.FC = () => {
  const f = useCurrentFrame();
  const drift = Math.sin(f / 90) * 6;
  return (
    <AbsoluteFill style={{ background: PAPER }}>
      <svg width="1080" height="1920" style={{ position: 'absolute', inset: 0, transform: `translateY(${drift}px)` }}>
        {Array.from({ length: 40 }).map((_, i) => (
          <line key={i} x1="0" x2="1080" y1={120 + i * 46} y2={120 + i * 46} stroke="#C9CFDD" strokeWidth="1.4" opacity="0.55" />
        ))}
        <line x1="120" x2="120" y1="0" y2="1920" stroke="#E8A9A2" strokeWidth="2" opacity="0.7" />
      </svg>
      <AbsoluteFill style={{ background: 'radial-gradient(120% 70% at 50% 40%, rgba(0,0,0,0) 55%, rgba(60,50,30,.18) 100%)' }} />
    </AbsoluteFill>
  );
};

const Source: React.FC = () => {
  const f = useCurrentFrame();
  const o = r(f, 6, 20) * (1 - r(f, s(C.take), s(C.take) + 10));
  return (
    <div style={{ position: 'absolute', left: 150, right: 90, top: 1460, fontFamily: MONO, fontSize: 26, lineHeight: 1.4, color: '#5D6175', opacity: o }}>
      Source: Hswen et al., JAMA Network Open.<br />Reported by STAT, 27 August 2026.
    </div>
  );
};

/* 1. hook, then the comparison */
const Scene1: React.FC = () => {
  const f = useCurrentFrame();
  if (!win(f, 0, C.brain)) return null;
  const out = r(f, s(C.brain) - 8, s(C.brain), easeIn);
  const hookOut = r(f, s(3.0), s(3.3), easeIn);
  const count = Math.round(interpolate(f, [s(3.5), s(6.0)], [0, 2000000], { ...clamp, easing: ease }));
  const hi = r(f, s(1.3), s(1.8));
  return (
    <>
      <div style={{ position: 'absolute', left: 150, right: 90, top: 460, opacity: 1 - hookOut, transform: `translateY(${-hookOut * 30}px)` }}>
        <div style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 30', fontWeight: 460, fontSize: 132, lineHeight: 1.0, letterSpacing: -3.5, color: INK }}>
          <Rise text="The symptoms that never make it into" at={0.05} step={1.6} />{' '}
          <span style={{ position: 'relative', display: 'inline-block' }}>
            <span style={{ position: 'absolute', left: -10, right: -10, top: '30%', bottom: '4%', background: HI, transformOrigin: '0 50%', transform: `scaleX(${hi}) rotate(-1deg)`, borderRadius: 6 }} />
            <span style={{ position: 'relative' }}><Rise text="your notes." at={0.9} step={2} /></span>
          </span>
        </div>
      </div>
      {f >= s(3.0) && (
        <div style={{ position: 'absolute', left: 150, right: 90, top: 360, opacity: (1 - out) * r(f, s(3.1), s(3.4)) }}>
          <div style={{ fontFamily: MONO, fontSize: 34, color: '#5D6175', letterSpacing: 1 }}>A STUDY COMPARED</div>
          <div style={{ marginTop: 24, fontFamily: SERIF, fontWeight: 440, fontSize: 92, lineHeight: 1.02, letterSpacing: -2.2, color: INK }}>One huge online menopause community</div>
          <div style={{ marginTop: 70, fontFamily: MONO, fontSize: 34, color: RED, letterSpacing: 1 }}>WITH</div>
          <div style={{ marginTop: 10, fontFamily: MONO, fontWeight: 500, fontSize: 150, letterSpacing: -5, color: INK, fontVariantNumeric: 'tabular-nums' }}>
            {count.toLocaleString('en-GB')}+
          </div>
          <div style={{ fontFamily: SERIF, fontWeight: 420, fontSize: 92, letterSpacing: -2, color: INK, opacity: r(f, s(4.8), s(5.2)) }}>medical notes.</div>
        </div>
      )}
    </>
  );
};

/* 2. three symptoms, one per beat; the last one loses its last word */
const Scene2: React.FC = () => {
  const f = useCurrentFrame();
  if (!win(f, C.brain, C.four)) return null;
  const out = r(f, s(C.four) - 8, s(C.four), easeIn);
  const line = (txt: string, at: number) => {
    const p = r(f, s(at), s(at) + 9);
    return (
      <div style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 30', fontWeight: 470, fontSize: 150, lineHeight: 1.0, letterSpacing: -4, color: INK, opacity: p, transform: `translateY(${(1 - p) * 40}px)` }}>{txt}</div>
    );
  };
  // typed "Losing words mid-sen..." then the word goes missing
  const typedFull = 'mid-sentence.';
  const t0 = s(C.words) + 12;
  const n = Math.max(0, Math.min(typedFull.length, Math.floor((f - t0) / 2.2)));
  const lost = f > t0 + 2.2 * 7 + 10;
  const shown = lost ? typedFull.slice(0, 7) : typedFull.slice(0, n);
  const caret = Math.floor(f / 12) % 2 === 0;
  const pw = r(f, s(C.words), s(C.words) + 9);
  return (
    <div style={{ position: 'absolute', left: 150, right: 90, top: 430, opacity: 1 - out, display: 'flex', flexDirection: 'column', gap: 44 }}>
      {line('Brain fog.', C.brain)}
      {line('Memory slips.', C.memory)}
      <div style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 30', fontWeight: 470, fontSize: 150, lineHeight: 1.0, letterSpacing: -4, color: INK, opacity: pw, transform: `translateY(${(1 - pw) * 40}px)` }}>
        Losing words<br />
        <span style={{ fontStyle: 'italic', fontWeight: 380 }}>{shown}</span>
        <span style={{ display: 'inline-block', width: 8, height: 130, background: RED, marginLeft: 8, verticalAlign: '-12px', opacity: caret ? 1 : 0 }} />
      </div>
    </div>
  );
};

/* 3 and 4. bars: online vs notes */
const Bars: React.FC<{ from: number; to: number; title: string; ratio: number; label: string; hiAt: number }> = ({ from, to, title, ratio, label, hiAt }) => {
  const f = useCurrentFrame();
  if (!win(f, from, to)) return null;
  const out = r(f, s(to) - 8, s(to), easeIn);
  const grow = r(f, s(from) + 6, s(from) + 40);
  const unit = 205;
  const hi = r(f, s(hiAt), s(hiAt) + 14);
  const bar = (name: string, v: number, col: string, delay: number) => {
    const g = r(f, s(from) + 6 + delay, s(from) + 40 + delay);
    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
        <div style={{ fontFamily: MONO, fontSize: 32, color: '#5D6175', letterSpacing: 1 }}>{name}</div>
        <div style={{ height: 150, width: v * unit * g, background: col, borderRadius: 8 }} />
      </div>
    );
  };
  return (
    <div style={{ position: 'absolute', left: 150, right: 90, top: 280, opacity: 1 - out }}>
      <div style={{ fontFamily: SERIF, fontWeight: 460, fontSize: 84, lineHeight: 1.04, letterSpacing: -2, color: INK }}>
        <Rise text={title} at={from + 0.05} step={2} />
      </div>
      <div style={{ marginTop: 70, display: 'flex', flexDirection: 'column', gap: 44 }}>
        {bar('ONLINE', ratio, INK, 0)}
        {bar('IN MEDICAL NOTES', 1, '#A9AEC4', 6)}
      </div>
      <div style={{ position: 'relative', display: 'inline-block', marginTop: 60 }}>
        <div style={{ position: 'absolute', left: -14, right: -14, top: '22%', bottom: '8%', background: HI, transformOrigin: '0 50%', transform: `scaleX(${hi}) rotate(-1deg)`, borderRadius: 6 }} />
        <div style={{ position: 'relative', fontFamily: SERIF, fontWeight: 520, fontSize: 190, letterSpacing: -5, color: INK, opacity: grow }}>{label}<span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 150, marginLeft: 6 }}>x</span></div>
      </div>
    </div>
  );
};

/* 5. the point, with a red pen underline */
const Scene5: React.FC = () => {
  const f = useCurrentFrame();
  if (!win(f, C.real, C.so)) return null;
  const out = r(f, s(C.so) - 8, s(C.so), easeIn);
  const pen = r(f, s(C.written) + 26, s(C.written) + 44);
  return (
    <div style={{ position: 'absolute', left: 150, right: 90, top: 520, opacity: 1 - out }}>
      <div style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 30', fontWeight: 460, fontSize: 140, lineHeight: 1.02, letterSpacing: -3, color: INK }}>
        <Rise text="The symptoms are real." at={C.real} step={2.4} />
      </div>
      <div style={{ marginTop: 60, position: 'relative', fontFamily: SERIF, fontWeight: 380, fontStyle: 'italic', fontSize: 128, lineHeight: 1.04, letterSpacing: -2.5, color: INK }}>
        <Rise text="They just don't get written down." at={C.written} step={2.2} />
        <svg width="820" height="60" viewBox="0 0 760 60" style={{ position: 'absolute', left: 0, bottom: -44 }}>
          <path d="M6 34 C 160 18, 360 44, 520 26 S 720 20, 754 30" fill="none" stroke={RED} strokeWidth="9" strokeLinecap="round"
            strokeDasharray="900" strokeDashoffset={900 * (1 - pen)} />
        </svg>
      </div>
    </div>
  );
};

/* 6. write it down: a handwritten note fills as she says it */
const Scene6: React.FC = () => {
  const f = useCurrentFrame();
  if (!win(f, C.so, C.take)) return null;
  const out = r(f, s(C.take) - 8, s(C.take), easeIn);
  const card = spring({ frame: f - s(C.so) - 10, fps: F, config: { damping: 16, stiffness: 80 } });
  const write = (txt: string, at: number) => {
    const n = Math.max(0, Math.min(txt.length, Math.floor((f - s(at)) / 1.3)));
    return txt.slice(0, n);
  };
  const row = (lab: string, txt: string, at: number) => (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 6, borderBottom: '2px solid #D9D3C3', paddingBottom: 18 }}>
      <div style={{ fontFamily: MONO, fontSize: 30, color: '#7A7466', letterSpacing: 1 }}>{lab}</div>
      <div style={{ fontFamily: HAND, fontWeight: 700, fontSize: 74, color: '#1D2A72', minHeight: 86 }}>{write(txt, at)}</div>
    </div>
  );
  return (
    <div style={{ position: 'absolute', left: 150, right: 90, top: 340, opacity: 1 - out }}>
      <div style={{ fontFamily: SERIF, fontWeight: 470, fontSize: 130, lineHeight: 1.0, letterSpacing: -3.5, color: INK }}>
        <Rise text="So write them down." at={C.so} step={2.4} />
      </div>
      <div style={{ marginTop: 60, background: '#FFFDF7', borderRadius: 14, padding: '44px 48px', boxShadow: '0 40px 70px -40px rgba(20,20,40,.45), 0 2px 0 rgba(0,0,0,.05)',
        transform: `translateY(${(1 - card) * 120}px) rotate(${(1 - card) * 4 - 1.2}deg)`, opacity: card, display: 'flex', flexDirection: 'column', gap: 26 }}>
        {row('WHEN', 'Tuesday, 2.10pm', C.when)}
        {row('HOW OFTEN', 'Third time this week', C.when + 0.8)}
        {row('HOW MUCH', 'Lost a whole word', C.much)}
      </div>
    </div>
  );
};

/* 7. end card */
const End: React.FC = () => {
  const f = useCurrentFrame();
  if (f < s(C.take)) return null;
  const p = r(f, s(C.take), s(C.take) + 14);
  const m = spring({ frame: f - s(C.clari), fps: F, config: { damping: 14, stiffness: 70 } });
  return (
    <div style={{ position: 'absolute', left: 150, right: 90, top: 520, opacity: p }}>
      <div style={{ fontFamily: SERIF, fontWeight: 460, fontSize: 140, lineHeight: 1.02, letterSpacing: -3, color: INK }}>
        <Rise text="And take it with you." at={C.take} step={2.4} />
      </div>
      <div style={{ marginTop: 90, display: 'flex', alignItems: 'center', gap: 26, opacity: m, transform: `translateY(${(1 - m) * 30}px)` }}>
        <div style={{ width: 120, height: 120, borderRadius: 30, background: '#24103F', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Img src={staticFile('mark-moon.svg')} style={{ width: 84, height: 84 }} />
        </div>
        <div>
          <div style={{ fontFamily: SERIF, fontWeight: 560, fontSize: 84, letterSpacing: -2, color: INK }}>Clari</div>
          <div style={{ fontFamily: SANS, fontWeight: 600, fontSize: 34, color: '#4C5068' }}>The private perimenopause diary</div>
        </div>
      </div>
      <div style={{ marginTop: 56, fontFamily: SANS, fontWeight: 600, fontSize: 36, color: INK, opacity: r(f, s(C.clari) + 20, s(C.clari) + 34) }}>
        Free on the App Store and Google Play
      </div>
    </div>
  );
};

export const Notes: React.FC = () => (
  <AbsoluteFill style={{ background: PAPER, overflow: 'hidden' }}>
    <Fonts />
    <Paper />
    <Scene1 />
    <Scene2 />
    <Bars from={C.four} to={C.mood} title="Women talked about these online nearly four times as often." ratio={3.9} label="nearly 4" hiAt={C.four + 2.6} />
    <Bars from={C.mood} to={C.real} title="Mood changes." ratio={2.9} label="nearly 3" hiAt={C.three + 0.2} />
    <Scene5 />
    <Scene6 />
    <End />
    <Source />
  </AbsoluteFill>
);
