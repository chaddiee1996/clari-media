import React from 'react';
import { AbsoluteFill, Img, OffthreadVideo, Sequence, continueRender, delayRender, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { BODY, Grain, Moon, Words, clamp, ease, easeIn, ramp, s } from './kit';

/* "Three months, one page." Real screen recordings of Clari in a phone frame.
   Light lilac world, so it sits apart from the night-sky reels. Captions y 230 to 460. */

const SERIF = 'FrauncesFull, Fraunces, Georgia, serif';
const fontHandle = { done: false };
const PageFonts: React.FC = () => {
  const [h] = React.useState(() => (fontHandle.done ? null : delayRender('pagefonts')));
  React.useEffect(() => {
    const faces = [
      new FontFace('FrauncesFull', `url(${staticFile('fraunces-full.woff2')})`, { weight: '100 900', style: 'normal' }),
      new FontFace('FrauncesFull', `url(${staticFile('fraunces-full-italic.woff2')})`, { weight: '100 900', style: 'italic' }),
      new FontFace('Figtree', `url(${staticFile('figtree.woff2')})`, { weight: '300 900', style: 'normal' }),
    ];
    Promise.all(faces.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => {
      fontHandle.done = true;
      if (h !== null) continueRender(h);
    });
  }, [h]);
  return null;
};

const HOOK = 3.0;
const CLIPS = [
  { src: 'log.mp4', from: 0, dur: 6.4, title: 'Tap how you feel.', sub: 'Tap again as it gets stronger. About a minute a day.' },
  { src: 'cal.mp4', from: 0.4, dur: 6.0, title: 'Watch the month take shape.', sub: 'Each day shows how strong things were.' },
  { src: 'sum.mp4', from: 0, dur: 5.0, title: 'Then share one clear summary.', sub: 'Made for your GP appointment.' },
];
const starts = CLIPS.reduce<number[]>((acc, c, i) => [...acc, i === 0 ? HOOK : acc[i - 1] + CLIPS[i - 1].dur], []);
const PDF_AT = starts[2] + CLIPS[2].dur;
const END_AT = PDF_AT + 3.4;
export const PAGE_FRAMES = s(END_AT + 5.0);

const BG: React.FC = () => {
  const f = useCurrentFrame();
  const t = ramp(f, s(END_AT + 0.3), s(END_AT + 1.2));
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: 'radial-gradient(90% 55% at 100% 0%, #EFE5FC 0%, rgba(239,229,252,0) 65%), radial-gradient(80% 50% at 0% 100%, #F7DCE6 0%, rgba(247,220,230,0) 70%), linear-gradient(180deg,#E6DAF8 0%, #F1E8F7 50%, #F6E3EA 100%)' }} />
      <AbsoluteFill style={{ opacity: t, background: 'linear-gradient(180deg,#0E0620 0%,#1C0C3B 46%,#33175F 100%)' }} />
    </AbsoluteFill>
  );
};

const Hook: React.FC = () => {
  const f = useCurrentFrame();
  if (f >= s(HOOK)) return null;
  const out = ramp(f, s(HOOK) - 9, s(HOOK), easeIn);
  return (
    <div style={{ position: 'absolute', left: 96, right: 96, top: 560, opacity: 1 - out, transform: `translateY(${-out * 24}px)` }}>
      <Words text="Three months|of symptoms.|One appointment." at={3} stagger={2.4} dur={12}
        style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 50', fontWeight: 430, fontSize: 128, lineHeight: 1.0, letterSpacing: -3.4, color: '#24103F' }}
        wordStyle={(w) => (w.startsWith('One') || w.startsWith('appointment') ? { fontStyle: 'italic', color: '#6B3FA0', fontWeight: 380 } : undefined)} />
      <div style={{ marginTop: 44, fontFamily: BODY, fontWeight: 550, fontSize: 44, color: '#4F3C6B', opacity: ramp(f, 34, 50) }}>Here's how to bring it all with you.</div>
    </div>
  );
};

const PW = 560;
const PH = Math.round(PW * (1864 - 120) / 860);

const Phone: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = s(HOOK - 0.3);
  if (f < a || f > s(PDF_AT + 1.2)) return null;
  const up = spring({ frame: f - a, fps, config: { damping: 18, stiffness: 70 } });
  const away = ramp(f, s(PDF_AT), s(PDF_AT + 0.8), easeIn);
  const tilt = interpolate(f, [a, s(PDF_AT)], [-2.5, 2.5], clamp);
  return (
    <div style={{ position: 'absolute', left: (1080 - PW) / 2 - 14, top: 560 + (1 - up) * 900 + away * 260, width: PW + 28, padding: 14, borderRadius: 82,
      background: 'linear-gradient(145deg,#3a3050,#0b0712 45%,#221a33)', boxShadow: '0 0 0 2px rgba(255,255,255,.06), 0 80px 120px -50px rgba(36,16,63,.7)',
      transform: `rotate(${tilt}deg) scale(${1 - away * 0.12})`, opacity: 1 - away }}>
      <div style={{ width: PW, height: PH, borderRadius: 68, overflow: 'hidden', position: 'relative', background: '#F3EEFA' }}>
        {CLIPS.map((c, i) => (
          <Sequence key={i} from={s(starts[i])} durationInFrames={s(c.dur) + (i === CLIPS.length - 1 ? s(1.2) : 0)} layout="none">
            <OffthreadVideo src={staticFile(c.src)} startFrom={s(c.from)} muted
              style={{ position: 'absolute', left: 0, top: -Math.round(120 * PW / 860), width: PW, height: Math.round(1864 * PW / 860) }} />
          </Sequence>
        ))}
      </div>
    </div>
  );
};

const Caption: React.FC<{ i: number }> = ({ i }) => {
  const f = useCurrentFrame();
  const a = s(starts[i]);
  const b = a + s(CLIPS[i].dur);
  if (f < a || f >= b) return null;
  const out = ramp(f, b - 8, b, easeIn);
  const c = CLIPS[i];
  return (
    <div style={{ position: 'absolute', left: 96, right: 96, top: 240, opacity: 1 - out, transform: `translateY(${-out * 16}px)` }}>
      <Words text={c.title} at={a + 4} stagger={2} dur={11}
        style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 50', fontWeight: 440, fontSize: 84, lineHeight: 1.04, letterSpacing: -2, color: '#24103F' }} />
      <div style={{ marginTop: 18, fontFamily: BODY, fontWeight: 550, fontSize: 38, color: '#4F3C6B', opacity: ramp(f, a + 16, a + 30) }}>{c.sub}</div>
    </div>
  );
};

const Pdf: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = s(PDF_AT + 0.2);
  if (f < a) return null;
  const p = spring({ frame: f - a, fps, config: { damping: 16, stiffness: 60 } });
  const out = ramp(f, s(END_AT), s(END_AT + 0.8), easeIn);
  const W = 700;
  return (
    <>
      <div style={{ position: 'absolute', left: 96, right: 96, top: 240, opacity: 1 - out }}>
        <Words text="30, 60 or 90 days.|One page." at={a + 2} stagger={2.2} dur={11}
          style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 50', fontWeight: 440, fontSize: 92, lineHeight: 1.02, letterSpacing: -2.2, color: '#24103F' }}
          wordStyle={(w) => (w.startsWith('One') || w.startsWith('page') ? { fontStyle: 'italic', color: '#6B3FA0', fontWeight: 380 } : undefined)} />
      </div>
      <div style={{ position: 'absolute', left: (1080 - W) / 2, top: 560 + (1 - p) * 700, width: W, borderRadius: 18, overflow: 'hidden', background: '#fff',
        boxShadow: '0 4px 0 rgba(36,16,63,.04), 0 90px 120px -50px rgba(36,16,63,.6)', transform: `rotate(${(1 - p) * 8 - 2}deg)`, opacity: 1 - out }}>
        <Img src={staticFile('pdf.webp')} style={{ display: 'block', width: W }} />
      </div>
    </>
  );
};

const End: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = s(END_AT + 0.5);
  if (f < t0) return null;
  const pop = spring({ frame: f - t0, fps, config: { damping: 14, stiffness: 60 } });
  const lift = (p: number): React.CSSProperties => ({ opacity: p, transform: `translateY(${(1 - p) * 26}px)` });
  return (
    <div style={{ position: 'absolute', left: 96, right: 96, top: 520 }}>
      <Moon size={150} glow={pop} style={{ transform: `scale(${pop})`, marginBottom: 60 }} />
      <Words text="Walk in with|the whole picture." at={t0 + 6} stagger={2} dur={12}
        style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 144, "SOFT" 50', fontWeight: 420, fontSize: 108, lineHeight: 1.02, letterSpacing: -2.8, color: '#FFF3D6' }}
        wordStyle={(w) => (w.startsWith('whole') || w.startsWith('picture') ? { fontStyle: 'italic', color: '#F7C6D3', fontWeight: 380 } : undefined)} />
      <div style={{ marginTop: 50, display: 'flex', alignItems: 'baseline', gap: 18, ...lift(ramp(f, t0 + 30, t0 + 46)) }}>
        <span style={{ fontFamily: SERIF, fontVariationSettings: '"opsz" 72, "SOFT" 50', fontWeight: 560, fontSize: 68, color: '#fff' }}>Clari</span>
        <span style={{ fontFamily: BODY, fontWeight: 550, fontSize: 36, color: 'rgba(255,243,214,.8)' }}>The private perimenopause tracker</span>
      </div>
      <div style={{ marginTop: 36, display: 'flex', gap: 20, ...lift(ramp(f, t0 + 40, t0 + 56)) }}>
        <Img src={staticFile('app-store-badge.svg')} style={{ height: 84 }} />
        <Img src={staticFile('google-play-badge.png')} style={{ height: 84 }} />
      </div>
    </div>
  );
};

export const Page: React.FC = () => (
  <AbsoluteFill style={{ overflow: 'hidden' }}>
    <PageFonts />
    <BG />
    <Hook />
    <Phone />
    {CLIPS.map((_, i) => <Caption key={i} i={i} />)}
    <Pdf />
    <End />
    <Grain opacity={0.05} />
  </AbsoluteFill>
);
