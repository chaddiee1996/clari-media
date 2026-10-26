import React from 'react';
import { AbsoluteFill, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { BODY, C, DISPLAY, Fonts, Grain, Moon, Stars, Words, ramp, easeIn, s } from './kit';

/* Five myths, one per beat. Text stays between y=300 and y=1240 (Reels safe zone). */
export const MYTHS_FRAMES = s(19);

const MYTHS: { myth: string; fact: string; src: string }[] = [
  { myth: '"You\'re too young."', fact: 'Menopause usually happens|between 45 and 55, and|it can come earlier.', src: 'nhs.uk' },
  { myth: '"It\'s just|hot flushes."', fact: 'The NHS lists low mood,|anxiety, memory problems,|joint pain and more.', src: 'nhs.uk' },
  { myth: '"It\'s over in a year."', fact: 'Symptoms usually last|7 to 9 years, sometimes|longer.', src: 'nhs.uk' },
  { myth: '"You\'ll need|a blood test."', fact: 'There\'s no routine test.|Over 45, NICE says it can|be diagnosed without one.', src: 'nhs.uk, NICE NG23' },
];
const BEAT = 3.0;
const START = 2.2;

const Sky: React.FC = () => {
  const f = useCurrentFrame();
  const dawn = ramp(f, s(8), s(17));
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(180deg,#0E0620 0%,#1C0C3B 46%,#33175F 100%)' }} />
      <AbsoluteFill style={{ opacity: dawn, background: 'linear-gradient(180deg,#120726 0%,#2B1256 36%,#5B2A93 66%,#B86FA8 88%,#F2B7C5 100%)' }} />
      <Stars maxY={1100} count={60} opacity={1 - dawn * 0.4} />
    </AbsoluteFill>
  );
};

const Hook: React.FC = () => {
  const f = useCurrentFrame();
  if (f >= s(START)) return null;
  const out = ramp(f, s(START) - 8, s(START), easeIn);
  return (
    <div style={{ position: 'absolute', left: 96, right: 96, top: 560, opacity: 1 - out }}>
      <Words text="Things people|still get wrong|about|perimenopause" at={0} stagger={1.6} dur={9}
        style={{ fontFamily: DISPLAY, fontWeight: 450, fontSize: 112, lineHeight: 1.0, letterSpacing: -2.5, color: '#FFF3D6' }} />
    </div>
  );
};

const Beat: React.FC<{ i: number }> = ({ i }) => {
  const f = useCurrentFrame();
  const a = s(START + i * BEAT);
  const b = a + s(BEAT);
  if (f < a || f >= b) return null;
  const out = ramp(f, b - 7, b, easeIn);
  const m = MYTHS[i];
  return (
    <div style={{ position: 'absolute', left: 96, right: 96, top: 520, opacity: 1 - out, transform: `translateY(${-out * 18}px)` }}>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <Words text={m.myth} at={a} stagger={1.4} dur={8}
          style={{ fontFamily: DISPLAY, fontStyle: 'italic', fontWeight: 380, fontSize: 104, lineHeight: 1.02, letterSpacing: -2, color: '#FFF3D6' }} />
        <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none' }}>
          {m.myth.split('|').map((_, li, arr) => (
            <div key={li} style={{ position: 'absolute', left: -6, right: -6, top: `${((li + 0.56) / arr.length) * 100}%`, height: 6, borderRadius: 3, background: C.pink,
              transformOrigin: '0% 50%', transform: `scaleX(${ramp(f, a + s(0.9) + li * 5, a + s(1.25) + li * 5)})` }} />
          ))}
        </div>
      </div>
      <div style={{ marginTop: 44 }}>
        <Words text={m.fact} at={a + s(1.2)} stagger={1.2} dur={9}
          style={{ fontFamily: BODY, fontWeight: 500, fontSize: 52, lineHeight: 1.32, color: 'rgba(255,243,214,0.9)' }} />
      </div>
      <div style={{ marginTop: 36, fontFamily: BODY, fontWeight: 600, fontSize: 28, color: 'rgba(255,243,214,0.6)', opacity: ramp(f, a + s(1.6), a + s(2.0)) }}>
        Source: {m.src}
      </div>
    </div>
  );
};

const End: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = s(START + MYTHS.length * BEAT);
  if (f < t0) return null;
  const pop = spring({ frame: f - t0, fps, config: { damping: 14, stiffness: 60 } });
  const lift = (p: number): React.CSSProperties => ({ opacity: p, transform: `translateY(${(1 - p) * 26}px)` });
  return (
    <>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 360, display: 'flex', justifyContent: 'center' }}>
        <Moon size={160} glow={pop} style={{ transform: `scale(${pop})` }} />
      </div>
      <div style={{ position: 'absolute', left: 96, right: 96, top: 600, textAlign: 'center' }}>
        <div style={{ fontFamily: DISPLAY, fontWeight: 450, fontSize: 84, lineHeight: 1.05, letterSpacing: -1.5, color: '#FFF3D6', ...lift(ramp(f, t0 + 4, t0 + 20)) }}>
          Send this to someone<br/>who's been told it's nothing.
        </div>
        <div style={{ marginTop: 50, fontFamily: DISPLAY, fontWeight: 600, fontSize: 64, color: '#fff', ...lift(ramp(f, t0 + 16, t0 + 32)) }}>Clari</div>
        <div style={{ marginTop: 10, fontFamily: BODY, fontWeight: 600, fontSize: 34, color: 'rgba(255,243,214,0.8)', ...lift(ramp(f, t0 + 20, t0 + 36)) }}>
          The private perimenopause tracker
        </div>
        <div style={{ marginTop: 34, display: 'flex', justifyContent: 'center', gap: 20, ...lift(ramp(f, t0 + 26, t0 + 42)) }}>
          <Img src={staticFile('app-store-badge.svg')} style={{ height: 80 }} />
          <Img src={staticFile('google-play-badge.png')} style={{ height: 80 }} />
        </div>
      </div>
    </>
  );
};

export const Myths: React.FC = () => (
  <AbsoluteFill style={{ background: '#0E0620', overflow: 'hidden' }}>
    <Fonts />
    <Sky />
    <Hook />
    {MYTHS.map((_, i) => <Beat key={i} i={i} />)}
    <End />
    <Grain opacity={0.06} />
  </AbsoluteFill>
);
