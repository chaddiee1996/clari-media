import React from 'react';
import { AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { BODY, C, DISPLAY, Fonts, Grain, Moon, Out, Show, Stars, Words, ramp, easeIn, s } from './kit';

export const JOINTS_FRAMES = s(22);

const centre: React.CSSProperties = { position: 'absolute', left: 100, right: 100, textAlign: 'center' };
const big: React.CSSProperties = {
  fontFamily: DISPLAY, fontWeight: 500, fontSize: 104, lineHeight: 1.05, letterSpacing: -2, color: C.ink, textWrap: 'balance' as any,
};
const mid: React.CSSProperties = { ...big, fontSize: 76, lineHeight: 1.1, letterSpacing: -1 };
const eyebrow: React.CSSProperties = {
  fontFamily: BODY, fontWeight: 800, fontSize: 28, letterSpacing: 6, textTransform: 'uppercase', color: C.pink,
};
const pinkItalic = { fontStyle: 'italic', color: C.pink, fontWeight: 400 } as const;

/* Sky: night that warms slowly towards dawn across the piece */
const Sky: React.FC = () => {
  const f = useCurrentFrame();
  const dawn = ramp(f, s(9), s(19));
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(180deg,#0A0418 0%,#170A33 38%,#2A1252 72%,#3E1C6E 100%)' }} />
      <AbsoluteFill style={{ opacity: dawn, background: 'linear-gradient(180deg,#120726 0%,#2B1256 36%,#5B2A93 66%,#B86FA8 88%,#F2B7C5 100%)' }} />
      <AbsoluteFill style={{ transform: `scale(${interpolate(f, [0, JOINTS_FRAMES], [1.1, 1])})` }}>
        <Stars maxY={1400} opacity={1 - dawn * 0.4} count={90} />
      </AbsoluteFill>
      <AbsoluteFill style={{ background: 'radial-gradient(120% 80% at 50% 45%, rgba(0,0,0,0) 55%, rgba(5,2,12,0.55) 100%)' }} />
    </AbsoluteFill>
  );
};

/* Ache: soft rose rings that pulse outwards, like a throb */
const Ache: React.FC<{ from: number; to: number; y: number }> = ({ from, to, y }) => {
  const f = useCurrentFrame();
  if (f < from || f > to) return null;
  const fadeAll = ramp(f, from, from + 10) * (1 - ramp(f, to - 12, to));
  const period = 34;
  return (
    <AbsoluteFill style={{ opacity: fadeAll }}>
      <svg width="1080" height="1920">
        {[0, 1, 2].map((k) => {
          const t = (((f - from + k * (period / 3)) % period) + period) % period / period;
          const r = 60 + t * 520;
          return <circle key={k} cx={540} cy={y} r={r} fill="none" stroke={C.rose} strokeWidth={3 + (1 - t) * 5} opacity={(1 - t) * 0.55} />;
        })}
        <circle cx={540} cy={y} r={38} fill={C.rose} opacity={0.18 + 0.12 * Math.sin((f / period) * Math.PI * 2)} />
      </svg>
    </AbsoluteFill>
  );
};

/* Scene 1: hook, readable from frame 0 */
const Hook: React.FC = () => (
  <Show from={0} to={s(3.4)}>
    <Out at={s(3.0)}>
      <div style={{ ...centre, top: 620 }}>
        <div style={eyebrow}>World Menopause Day</div>
        <div style={{ marginTop: 34 }}>
          <Words text="Aching joints|at 47?" at={0} stagger={1.5} dur={9} style={{ ...big, fontSize: 132 }}
            wordStyle={(w, i) => (i >= 2 ? pinkItalic : undefined)} />
        </div>
        <div style={{ marginTop: 40 }}>
          <Words text="It could be perimenopause." at={s(1.1)} stagger={2.2} style={{ ...mid, fontSize: 58, fontWeight: 400, color: C.soft }} />
        </div>
      </div>
    </Out>
  </Show>
);

/* Scene 2: the theme */
const Theme: React.FC = () => (
  <Show from={s(3.3)} to={s(6.9)}>
    <Out at={s(6.5)}>
      <div style={{ ...centre, top: 640 }}>
        <Words text="18 October 2026" at={s(3.35)} style={eyebrow} />
        <div style={{ marginTop: 36 }}>
          <Words text="This year's theme|is chronic pain|in midlife." at={s(3.6)} stagger={2.6} style={mid}
            wordStyle={(w) => (['chronic', 'pain'].includes(w) ? pinkItalic : undefined)} />
        </div>
        <Words text="International Menopause Society" at={s(5.0)} style={{ ...eyebrow, display: 'block', marginTop: 48, fontSize: 22, letterSpacing: 4, color: C.soft }} />
      </div>
    </Out>
  </Show>
);

/* Scene 3: NHS fact */
const Fact: React.FC = () => (
  <Show from={s(6.8)} to={s(10.6)}>
    <Out at={s(10.2)}>
      <div style={{ ...centre, top: 560 }}>
        <Words text="Muscle aches|and joint pains" at={s(6.9)} stagger={2.4} style={{ ...big, fontSize: 112 }}
          wordStyle={(w) => (['joint', 'pains'].includes(w) ? pinkItalic : undefined)} />
        <div style={{ marginTop: 40 }}>
          <Words text="are on the NHS list|of perimenopause symptoms." at={s(7.9)} stagger={2.2} style={{ ...mid, fontSize: 60, fontWeight: 400, color: C.soft }} />
        </div>
        <Words text="Source: nhs.uk" at={s(8.8)} style={{ display: 'block', marginTop: 46, fontFamily: BODY, fontWeight: 600, fontSize: 28, color: C.soft }} />
      </div>
    </Out>
  </Show>
);

/* Scene 4: after menopause */
const After: React.FC = () => (
  <Show from={s(10.5)} to={s(13.0)}>
    <Out at={s(12.6)}>
      <div style={{ ...centre, top: 720 }}>
        <Words text="And they can carry on|after menopause." at={s(10.55)} stagger={2.4} style={mid}
          wordStyle={(w) => (w.startsWith('after') || w.startsWith('menopause') ? pinkItalic : undefined)} />
      </div>
    </Out>
  </Show>
);

/* Scene 5: phone with the real log recording */
const PHONE_W = 560;
const BEZEL = 12;
const SCREEN_W = PHONE_W - BEZEL * 2;
const SCREEN_H = Math.round((SCREEN_W * 1864) / 860);

const Phone: React.FC<{ src: string; trim: number }> = ({ src, trim }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inAt = s(12.8);
  const outAt = s(17.0);
  const rise = spring({ frame: f - inAt, fps, config: { damping: 18, stiffness: 80 } });
  const out = ramp(f, outAt - 14, outAt, easeIn);
  if (f < inAt || f > outAt) return null;
  return (
    <div style={{ position: 'absolute', left: (1080 - PHONE_W) / 2, top: 560, width: PHONE_W,
      transform: `translateY(${(1 - rise) * 1100 + out * 900}px) rotate(${Math.sin(f / 70) * 1.2}deg)`, opacity: 1 - out }}>
      <div style={{ padding: BEZEL, borderRadius: 74, background: 'linear-gradient(145deg,#2A2238,#0B0712 40%,#1B1526)',
        boxShadow: '0 0 0 2px rgba(255,255,255,0.08), 0 60px 120px -30px rgba(5,0,15,0.85), 0 30px 60px -30px rgba(91,42,147,0.6)' }}>
        <div style={{ position: 'relative', width: SCREEN_W, height: SCREEN_H, borderRadius: 62, overflow: 'hidden', background: '#F6F1FC' }}>
          <Sequence from={inAt} durationInFrames={outAt - inAt} layout="none">
            <OffthreadVideo src={staticFile(src)} trimBefore={trim} muted style={{ width: SCREEN_W, height: SCREEN_H, display: 'block' }} />
            <div style={{ position: 'absolute', left: (288 / 860) * SCREEN_W - 18, top: (59 / 1864) * SCREEN_H - 18, width: 36, height: 36, borderRadius: 18, background: '#000' }} />
          </Sequence>
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(115deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0) 35%)' }} />
        </div>
      </div>
    </div>
  );
};

const PhoneCaption: React.FC = () => (
  <Show from={s(12.9)} to={s(17.0)}>
    <Out at={s(16.6)}>
      <div style={{ ...centre, top: 250 }}>
        <Words text="Log it|when it flares." at={s(13.0)} stagger={2.4} style={{ ...big, fontSize: 84 }}
          wordStyle={(w) => (w.startsWith('flares') || w === 'when' || w === 'it' ? undefined : undefined)} />
      </div>
    </Out>
  </Show>
);

/* Scene 6: pattern, a week of moons filling */
const Pattern: React.FC = () => {
  const f = useCurrentFrame();
  const levels = [0.25, 0.5, 0.35, 0.8, 0.6, 0.9, 0.45];
  const days = ['M', 'T', 'W', 'T', 'F', 'S', 'S'];
  const from = s(17.0);
  return (
    <Show from={from} to={s(19.4)}>
      <Out at={s(19.0)}>
        <div style={{ ...centre, top: 600 }}>
          <Words text="See the pattern." at={from + 2} stagger={2.4} style={{ ...big, fontSize: 96 }} />
          <div style={{ display: 'flex', justifyContent: 'center', gap: 30, marginTop: 60 }}>
            {levels.map((lv, i) => {
              const p = ramp(f, from + 8 + i * 3, from + 20 + i * 3);
              return (
                <div key={i} style={{ textAlign: 'center', opacity: Math.min(1, p * 2) }}>
                  <svg width="92" height="92" viewBox="0 0 100 100">
                    <circle cx="50" cy="50" r="44" fill="rgba(255,243,214,.12)" stroke="rgba(255,243,214,.45)" strokeWidth="3" />
                    <clipPath id={`cp${i}`}><rect x="0" y="0" width={lv * 100 * p} height="100" /></clipPath>
                    <circle cx="50" cy="50" r="44" fill="#FFEFC9" clipPath={`url(#cp${i})`} />
                  </svg>
                  <div style={{ fontFamily: BODY, fontWeight: 700, fontSize: 26, color: C.soft, marginTop: 10 }}>{days[i]}</div>
                </div>
              );
            })}
          </div>
          <Words text="Show your GP." at={from + 30} stagger={2.4} style={{ ...big, fontSize: 96, display: 'block', marginTop: 60, ...pinkItalic }} />
        </div>
      </Out>
    </Show>
  );
};

/* End card */
const End: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = s(19.3);
  const pop = spring({ frame: f - t0, fps, config: { damping: 14, stiffness: 60 } });
  const lift = (p: number): React.CSSProperties => ({ opacity: p, transform: `translateY(${(1 - p) * 26}px)`, filter: `blur(${(1 - p) * 8}px)` });
  const name = ramp(f, t0 + 4, t0 + 22);
  const tag = ramp(f, t0 + 12, t0 + 30);
  const badges = ramp(f, t0 + 20, t0 + 38);
  const send = ramp(f, t0 + 30, t0 + 48);
  if (f < t0) return null;
  return (
    <>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 430, display: 'flex', justifyContent: 'center' }}>
        <Moon size={190} glow={pop} style={{ transform: `scale(${pop})` }} />
      </div>
      <div style={{ ...centre, top: 680 }}>
        <div style={{ fontFamily: DISPLAY, fontWeight: 600, fontSize: 170, letterSpacing: -4, color: C.ink, lineHeight: 1, ...lift(name) }}>Clari</div>
        <div style={{ marginTop: 24, fontFamily: BODY, fontWeight: 600, fontSize: 40, color: C.soft, ...lift(tag) }}>Private perimenopause &amp; menopause tracker</div>
        <div style={{ marginTop: 50, display: 'flex', justifyContent: 'center', gap: 22, ...lift(badges) }}>
          <Img src={staticFile('app-store-badge.svg')} style={{ height: 92 }} />
          <Img src={staticFile('google-play-badge.png')} style={{ height: 92 }} />
        </div>
        <div style={{ marginTop: 44, fontFamily: DISPLAY, fontStyle: 'italic', fontSize: 50, color: C.pink, ...lift(send) }}>
          Send this to a friend with aching joints.
        </div>
      </div>
    </>
  );
};

export const Joints: React.FC<{ clip?: string; clipTrim?: number }> = ({ clip = 'joint.mp4', clipTrim = 0 }) => (
  <AbsoluteFill style={{ background: '#0A0418', overflow: 'hidden' }}>
    <Fonts />
    <Sky />
    <Ache from={0} to={s(3.3)} y={620} />
    <Ache from={s(6.8)} to={s(10.4)} y={560} />
    <Hook />
    <Theme />
    <Fact />
    <After />
    <PhoneCaption />
    <Phone src={clip} trim={clipTrim} />
    <Pattern />
    <End />
    <Grain />
  </AbsoluteFill>
);
