import React from 'react';
import { AbsoluteFill, Img, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { BODY, Grain, Moon, Stars, Words, clamp, ease, easeIn, ramp, rnd, s } from './kit';

/* "Perimenopause doesn't keep office hours."
   One day, hour by hour. The sky moves with the clock; the sun or moon rides an arc.
   Every line is a symptom on the NHS list. Text kept between y=300 and y=1300. */

const SERIF = 'FrauncesFull, Fraunces, Georgia, serif';
const MONO = 'DMMono, ui-monospace, monospace';

const fontHandle = { done: false };
const DayFonts: React.FC = () => {
  const [h] = React.useState(() => (fontHandle.done ? null : delayRender('dayfonts')));
  React.useEffect(() => {
    const faces = [
      new FontFace('FrauncesFull', `url(${staticFile('fraunces-full.woff2')})`, { weight: '100 900', style: 'normal' }),
      new FontFace('FrauncesFull', `url(${staticFile('fraunces-full-italic.woff2')})`, { weight: '100 900', style: 'italic' }),
      new FontFace('Figtree', `url(${staticFile('figtree.woff2')})`, { weight: '300 900', style: 'normal' }),
      new FontFace('DMMono', `url(${staticFile('dm-mono-500.woff2')})`, { weight: '500', style: 'normal' }),
    ];
    Promise.all(faces.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => {
      fontHandle.done = true;
      if (h !== null) continueRender(h);
    });
  }, [h]);
  return null;
};

type Beat = { t: string; mins: number; line: string; tag: string; sky: [string, string, string]; dark: boolean };
export const BEATS: Beat[] = [
  { t: '03:12', mins: 192, line: 'Awake. Soaked.|Again.', tag: 'Night sweats', sky: ['#0B051A', '#1A0B38', '#311660'], dark: true },
  { t: '07:40', mins: 460, line: 'Stiff before you’ve|even stood up.', tag: 'Joint pain', sky: ['#3A2470', '#9A62A8', '#F4B8A6'], dark: true },
  { t: '10:55', mins: 655, line: 'The word is right|there. Then gone.', tag: 'Brain fog', sky: ['#C7D4F6', '#E9E0F8', '#FBE9E6'], dark: false },
  { t: '14:20', mins: 860, line: 'Heart racing,|out of nowhere.', tag: 'Palpitations', sky: ['#F6E7CF', '#F7D2C4', '#EDB9C8'], dark: false },
  { t: '18:05', mins: 1085, line: 'Snapped at someone.|Felt awful after.', tag: 'Mood swings', sky: ['#5B347F', '#BC6A97', '#F2A88C'], dark: true },
  { t: '23:40', mins: 1420, line: 'Exhausted.|Still can’t sleep.', tag: 'Trouble sleeping', sky: ['#0E0620', '#22103F', '#3A1C63'], dark: true },
];
const HOOK = 2.6;
const BEAT = 2.7;
const END_AT = HOOK + BEATS.length * BEAT;
export const DAY_FRAMES = s(END_AT + 6.2);

const mix = (a: string, b: string, t: number) => {
  const p = (h: string) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16));
  const A = p(a), B = p(b);
  return '#' + A.map((v, i) => Math.round(v + (B[i] - v) * t).toString(16).padStart(2, '0')).join('');
};

/** which beat (fractional) are we in, with eased transition at each beat start */
const useBeat = () => {
  const f = useCurrentFrame();
  const sec = f / 30;
  if (sec < HOOK) return { i: -1, k: 0, local: sec };
  const raw = (sec - HOOK) / BEAT;
  const i = Math.min(BEATS.length - 1, Math.floor(raw));
  const local = sec - HOOK - i * BEAT;
  return { i, k: Math.min(1, local / 0.7), local };
};

const skyAt = (f: number) => {
  const sec = f / 30;
  const night: [string, string, string] = ['#0B051A', '#1A0B38', '#311660'];
  if (sec < HOOK) return night;
  const raw = (sec - HOOK) / BEAT;
  const i = Math.min(BEATS.length - 1, Math.floor(raw));
  const prev = i === 0 ? night : BEATS[i - 1].sky;
  const t = ease(Math.min(1, (raw - i) * BEAT / 0.9));
  let sky = BEATS[i].sky.map((c, j) => mix(prev[j], c, t)) as [string, string, string];
  if (sec > END_AT) {
    const e2 = ease(Math.min(1, (sec - END_AT) / 1.2));
    sky = sky.map((c, j) => mix(c, ['#0E0620', '#1C0C3B', '#33175F'][j], e2)) as [string, string, string];
  }
  return sky;
};

const minsAt = (f: number) => {
  const sec = f / 30;
  if (sec < HOOK) return 0;
  const raw = (sec - HOOK) / BEAT;
  const i = Math.min(BEATS.length - 1, Math.floor(raw));
  const prev = i === 0 ? 0 : BEATS[i - 1].mins;
  const t = ease(Math.min(1, (raw - i) * BEAT / 0.8));
  return prev + (BEATS[i].mins - prev) * t;
};

const Sky: React.FC = () => {
  const f = useCurrentFrame();
  const [a, b, c] = skyAt(f);
  const m = minsAt(f);
  // night amount: 1 at night, 0 by day
  const day = Math.max(0, Math.sin(((m - 360) / 1440) * Math.PI * 2 * 1)) ;
  const isDay = m > 380 && m < 1200;
  // arc position: sun from 06:00 to 20:00, moon otherwise
  const p = isDay ? (m - 360) / (1200 - 360) : ((m < 380 ? m + 1440 : m) - 1200) / (1440 + 380 - 1200);
  const ax = 120 + p * 840;
  const ay = 360 - Math.sin(p * Math.PI) * 220;
  const starsOp = interpolate(m, [300, 470, 1150, 1300], [1, 0, 0, 1], clamp);
  const sec = f / 30;
  const endFade = ramp(f, s(END_AT), s(END_AT + 1));
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `linear-gradient(180deg, ${a} 0%, ${b} 52%, ${c} 100%)` }} />
      <Stars maxY={1200} count={80} opacity={Math.max(starsOp, endFade)} />
      {sec < END_AT + 0.4 && (
        <div style={{ position: 'absolute', left: ax - 70, top: ay - 70, width: 140, height: 140, opacity: 1 - endFade }}>
          {isDay ? (
            <div style={{ width: 140, height: 140, borderRadius: '50%', background: 'radial-gradient(circle at 40% 38%, #FFFDF6 0%, #FFF1CF 55%, #FFD9A8 100%)',
              boxShadow: '0 0 120px 40px rgba(255,236,200,.55)' }} />
          ) : (
            <Moon size={140} glow={0.9} />
          )}
        </div>
      )}
      {/* horizon hills, like the app */}
      <svg width="1080" height="1920" style={{ position: 'absolute', inset: 0 }}>
        <path d="M0 1700 C 260 1650, 520 1690, 760 1660 S 1000 1640, 1080 1650 L1080 1920 L0 1920Z" fill={mix(c, '#24103F', 0.55)} opacity={0.55} />
        <path d="M0 1770 C 300 1730, 560 1780, 820 1745 S 1040 1735, 1080 1745 L1080 1920 L0 1920Z" fill={mix(c, '#24103F', 0.75)} opacity={0.7} />
      </svg>
    </AbsoluteFill>
  );
};

const Clock: React.FC = () => {
  const f = useCurrentFrame();
  const { i } = useBeat();
  const sec = f / 30;
  if (sec < HOOK - 0.2 || sec > END_AT + 0.5) return null;
  const m = Math.round(minsAt(f));
  const hh = String(Math.floor(m / 60) % 24).padStart(2, '0');
  const mm = String(m % 60).padStart(2, '0');
  const dark = i < 0 ? true : BEATS[i].dark;
  const inP = ramp(f, s(HOOK - 0.2), s(HOOK + 0.3));
  const out = ramp(f, s(END_AT), s(END_AT + 0.4), easeIn);
  const col = dark ? '#FFF3D6' : '#24103F';
  return (
    <div style={{ position: 'absolute', left: 96, top: 520, fontFamily: MONO, fontWeight: 500, fontSize: 190, letterSpacing: -6, color: col,
      opacity: inP * (1 - out), fontVariantNumeric: 'tabular-nums' }}>
      {hh}<span style={{ opacity: 0.5 + 0.5 * Math.abs(Math.cos(sec * Math.PI)) }}>:</span>{mm}
    </div>
  );
};

const Hook: React.FC = () => {
  const f = useCurrentFrame();
  if (f >= s(HOOK)) return null;
  const out = ramp(f, s(HOOK) - 9, s(HOOK), easeIn);
  return (
    <div style={{ position: 'absolute', left: 96, right: 96, top: 600, opacity: 1 - out, transform: `translateY(${-out * 24}px)` }}>
      <Words text="Perimenopause|doesn't keep|office hours." at={2} stagger={2.2} dur={12}
        style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 50', fontWeight: 420, fontSize: 132, lineHeight: 1.0, letterSpacing: -3.5, color: '#FFF3D6' }}
        wordStyle={(w) => (w.startsWith('office') || w.startsWith('hours') ? { fontStyle: 'italic', color: '#F7C6D3', fontWeight: 380 } : undefined)} />
    </div>
  );
};

const BeatText: React.FC<{ i: number }> = ({ i }) => {
  const f = useCurrentFrame();
  const a = s(HOOK + i * BEAT);
  const b = a + s(BEAT);
  if (f < a || f >= b) return null;
  const B = BEATS[i];
  const col = B.dark ? '#FFF3D6' : '#24103F';
  const out = i === BEATS.length - 1 ? 0 : ramp(f, b - 8, b, easeIn);
  const tagP = ramp(f, a + s(0.9), a + s(1.25));
  return (
    <div style={{ position: 'absolute', left: 96, right: 96, top: 800, opacity: 1 - out, transform: `translateY(${-out * 20}px)` }}>
      <Words text={B.line} at={a + s(0.45)} stagger={1.8} dur={11}
        style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 50', fontWeight: 420, fontSize: 100, lineHeight: 1.04, letterSpacing: -2.4, color: col }} />
      <div style={{ marginTop: 48, display: 'inline-flex', alignItems: 'center', gap: 14, padding: '14px 28px 16px', borderRadius: 999,
        border: `3px solid ${B.dark ? 'rgba(255,243,214,.55)' : 'rgba(36,16,63,.45)'}`, fontFamily: BODY, fontWeight: 650, fontSize: 38, color: col,
        opacity: tagP, transform: `translateY(${(1 - tagP) * 14}px)` }}>
        <span style={{ width: 14, height: 14, borderRadius: 7, background: B.dark ? '#F7C6D3' : '#C8628A' }} />
        {B.tag}
      </div>
    </div>
  );
};

const Footnote: React.FC = () => {
  const f = useCurrentFrame();
  const { i } = useBeat();
  const sec = f / 30;
  if (sec < HOOK || sec > END_AT) return null;
  const dark = BEATS[Math.max(0, i)].dark;
  return (
    <div style={{ position: 'absolute', left: 96, top: 1300, fontFamily: BODY, fontWeight: 600, fontSize: 28, color: dark ? 'rgba(255,243,214,.65)' : 'rgba(36,16,63,.6)',
      opacity: ramp(f, s(HOOK + 0.6), s(HOOK + 1.2)) }}>
      All on the NHS list of perimenopause symptoms
    </div>
  );
};

const End: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = s(END_AT + 0.4);
  if (f < t0) return null;
  const pop = spring({ frame: f - t0, fps, config: { damping: 14, stiffness: 60 } });
  const lift = (p: number): React.CSSProperties => ({ opacity: p, transform: `translateY(${(1 - p) * 26}px)` });
  return (
    <>
      <div style={{ position: 'absolute', left: 96, right: 96, top: 520 }}>
        <Words text="Clari keeps the|record, so you|don't have to|remember it all." at={t0} stagger={1.7} dur={12}
          style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 50', fontWeight: 420, fontSize: 104, lineHeight: 1.02, letterSpacing: -2.6, color: '#FFF3D6' }}
          wordStyle={(w) => (w.startsWith('remember') || w.startsWith('it') || w.startsWith('all') ? { fontStyle: 'italic', color: '#F7C6D3', fontWeight: 380 } : undefined)} />
        <div style={{ marginTop: 50, fontFamily: BODY, fontWeight: 500, fontSize: 42, lineHeight: 1.35, color: 'rgba(255,243,214,.88)', ...lift(ramp(f, t0 + 30, t0 + 46)) }}>
          Tap how you feel. A minute a day.<br />Then share one clear summary with your GP.
        </div>
        <div style={{ marginTop: 56, display: 'flex', alignItems: 'center', gap: 18, ...lift(ramp(f, t0 + 40, t0 + 56)) }}>
          <Moon size={70} glow={0.6 * pop} />
          <span style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 72, "SOFT" 50', fontWeight: 560, fontSize: 66, color: '#fff' }}>Clari</span>
        </div>
        <div style={{ marginTop: 34, display: 'flex', gap: 20, ...lift(ramp(f, t0 + 48, t0 + 64)) }}>
          <Img src={staticFile('app-store-badge.svg')} style={{ height: 84 }} />
          <Img src={staticFile('google-play-badge.png')} style={{ height: 84 }} />
        </div>
      </div>
    </>
  );
};

export const Day: React.FC = () => (
  <AbsoluteFill style={{ background: '#0B051A', overflow: 'hidden' }}>
    <DayFonts />
    <Sky />
    <Hook />
    <Clock />
    {BEATS.map((_, i) => <BeatText key={i} i={i} />)}
    <Footnote />
    <End />
    <Grain opacity={0.07} />
  </AbsoluteFill>
);
