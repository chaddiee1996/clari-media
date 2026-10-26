import React from 'react';
import { AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { BODY, C, DISPLAY, Fonts, Grain, Moon, Stars, Words, ramp, easeIn, s } from './kit';

/* Meta Reels ad, 1080x1920. Text lives between y=300 and y=1240 (Reels safe zone:
   top 270px and bottom 672px are covered by UI). */
export const AD_FRAMES = s(23);

const T = {
  bed: [0, 2.7], water: [2.6, 4.9], tea: [4.8, 7.1], notes: [7.0, 9.3],
  cal: [9.2, 12.3], log: [12.2, 15.3], sum: [15.2, 17.7], dawn: [17.6, 20.3], end: [20.2, 23],
} as const;

const textBox: React.CSSProperties = { position: 'absolute', left: 90, right: 90, top: 330, textAlign: 'left' };
const head: React.CSSProperties = {
  fontFamily: DISPLAY, fontWeight: 500, fontSize: 104, lineHeight: 1.04, letterSpacing: -2, color: '#fff',
  textShadow: '0 4px 30px rgba(10,4,24,0.55)', textWrap: 'balance' as any,
};
const sub: React.CSSProperties = { ...head, fontSize: 60, fontWeight: 400, lineHeight: 1.15, letterSpacing: -0.5, color: 'rgba(255,255,255,0.92)' };
const pink = { fontStyle: 'italic', color: C.pink, fontWeight: 400 } as const;

/* Full-bleed real footage, graded towards Clari's plum night palette */
const Footage: React.FC<{ src: string; at: readonly [number, number]; warm?: boolean }> = ({ src, at, warm }) => {
  const f = useCurrentFrame();
  const a = s(at[0]);
  const b = s(at[1]);
  if (f < a || f >= b) return null;
  const inP = ramp(f, a, a + 6);
  const zoom = interpolate(f, [a, b], [1.0, 1.07]);
  return (
    <AbsoluteFill style={{ opacity: inP }}>
      <Sequence from={a} durationInFrames={b - a} layout="none">
        <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
          <OffthreadVideo src={staticFile(src)} muted style={{ width: 1080, height: 1920, objectFit: 'cover',
            filter: warm ? 'saturate(1.0) contrast(1.06)' : 'saturate(0.92) contrast(1.08) brightness(0.95)' }} />
        </AbsoluteFill>
      </Sequence>
      {/* plum grade + top shade for legible text */}
      <AbsoluteFill style={{ background: 'linear-gradient(180deg, rgba(23,10,51,0.72) 0%, rgba(23,10,51,0.38) 30%, rgba(23,10,51,0) 50%, rgba(10,4,24,0) 80%, rgba(10,4,24,0.3) 100%)' }} />
    </AbsoluteFill>
  );
};

const Line: React.FC<{ at: number; to: number; a: string; b?: string; bAt?: number; aStyle?: React.CSSProperties }> = ({ at, to, a, b, bAt, aStyle }) => {
  const f = useCurrentFrame();
  if (f < s(at) || f >= s(to)) return null;
  const out = ramp(f, s(to) - 7, s(to), easeIn);
  return (
    <div style={{ ...textBox, opacity: 1 - out, transform: `translateY(${-out * 20}px)` }}>
      <Words text={a} at={s(at) + 2} stagger={2.2} dur={12} style={{ ...head, ...aStyle }}
        wordStyle={(w) => (w.endsWith('*') ? pink : undefined)} render={(w) => w.replace('*', '')} />
      {b ? (
        <div style={{ marginTop: 26 }}>
          <Words text={b} at={s(bAt ?? at + 0.6)} stagger={2.2} dur={12} style={sub}
            wordStyle={(w) => (w.endsWith('*') ? pink : undefined)} render={(w) => w.replace('*', '')} />
        </div>
      ) : null}
    </div>
  );
};

/* Night-sky brand background for the app and end scenes */
const Sky: React.FC<{ from: number }> = ({ from }) => {
  const f = useCurrentFrame();
  if (f < s(from)) return null;
  const dawn = ramp(f, s(15), s(21));
  return (
    <AbsoluteFill style={{ opacity: ramp(f, s(from), s(from) + 6) }}>
      <AbsoluteFill style={{ background: 'linear-gradient(180deg,#0A0418 0%,#170A33 38%,#2A1252 72%,#3E1C6E 100%)' }} />
      <AbsoluteFill style={{ opacity: dawn, background: 'linear-gradient(180deg,#120726 0%,#2B1256 36%,#5B2A93 66%,#B86FA8 88%,#F2B7C5 100%)' }} />
      <Stars maxY={1300} count={80} opacity={1 - dawn * 0.4} />
    </AbsoluteFill>
  );
};

/* The calendar clip is landscape, so it sits in a card instead of being cropped */
const CalCard: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = s(T.cal[0]);
  const b = s(T.cal[1]);
  if (f < a || f >= b) return null;
  const pop = spring({ frame: f - a, fps, config: { damping: 18, stiffness: 90 } });
  const out = ramp(f, b - 8, b, easeIn);
  return (
    <div style={{ position: 'absolute', left: 60, width: 960, top: 760, transform: `translateY(${(1 - pop) * 80 - out * 40}px) rotate(${-1.5 + pop * 1.5}deg)`, opacity: Math.min(1, pop * 1.5) * (1 - out) }}>
      <div style={{ borderRadius: 36, overflow: 'hidden', boxShadow: '0 50px 100px -30px rgba(0,0,0,0.75), 0 0 0 2px rgba(255,255,255,0.08)' }}>
        <Sequence from={a} durationInFrames={b - a} layout="none">
          <OffthreadVideo src={staticFile('ad/cal.mp4')} muted style={{ width: 960, height: 540, objectFit: 'cover', display: 'block' }} />
        </Sequence>
      </div>
    </div>
  );
};

const PHONE_W = 560;
const BEZEL = 12;
const SCREEN_W = PHONE_W - BEZEL * 2;
const SCREEN_H = Math.round((SCREEN_W * 1864) / 860);

const Phone: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = s(T.log[0]);
  const b = s(T.sum[1]);
  if (f < a || f >= b) return null;
  const rise = spring({ frame: f - a, fps, config: { damping: 18, stiffness: 80 } });
  const out = ramp(f, b - 10, b, easeIn);
  const swap = s(T.sum[0]);
  return (
    <div style={{ position: 'absolute', left: (1080 - PHONE_W) / 2, top: 800, width: PHONE_W,
      transform: `translateY(${(1 - rise) * 1100 + out * 900}px) rotate(${Math.sin(f / 70) * 1.2}deg)`, opacity: 1 - out }}>
      <div style={{ padding: BEZEL, borderRadius: 74, background: 'linear-gradient(145deg,#2A2238,#0B0712 40%,#1B1526)',
        boxShadow: '0 0 0 2px rgba(255,255,255,0.08), 0 60px 120px -30px rgba(5,0,15,0.85), 0 30px 60px -30px rgba(91,42,147,0.6)' }}>
        <div style={{ position: 'relative', width: SCREEN_W, height: SCREEN_H, borderRadius: 62, overflow: 'hidden', background: '#F6F1FC' }}>
          <Sequence from={a} durationInFrames={swap - a + 4} layout="none">
            <OffthreadVideo src={staticFile('joint.mp4')} trimBefore={10} muted style={{ width: SCREEN_W, height: SCREEN_H, display: 'block' }} />
          </Sequence>
          <Sequence from={swap} durationInFrames={b - swap} layout="none">
            <div style={{ position: 'absolute', inset: 0, opacity: ramp(f, swap, swap + 6) }}>
              <OffthreadVideo src={staticFile('sum.mp4')} muted style={{ width: SCREEN_W, height: SCREEN_H, display: 'block' }} />
            </div>
          </Sequence>
          <div style={{ position: 'absolute', left: (288 / 860) * SCREEN_W - 18, top: (59 / 1864) * SCREEN_H - 18, width: 36, height: 36, borderRadius: 18, background: '#000' }} />
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(115deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0) 35%)' }} />
        </div>
      </div>
    </div>
  );
};

const End: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = s(T.end[0]);
  if (f < t0) return null;
  const pop = spring({ frame: f - t0, fps, config: { damping: 14, stiffness: 60 } });
  const lift = (p: number): React.CSSProperties => ({ opacity: p, transform: `translateY(${(1 - p) * 26}px)`, filter: `blur(${(1 - p) * 8}px)` });
  return (
    <>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 330, display: 'flex', justifyContent: 'center' }}>
        <Moon size={170} glow={pop} style={{ transform: `scale(${pop})` }} />
      </div>
      <div style={{ position: 'absolute', left: 90, right: 90, top: 560, textAlign: 'center' }}>
        <div style={{ fontFamily: DISPLAY, fontWeight: 600, fontSize: 168, letterSpacing: -4, color: '#fff', lineHeight: 1, ...lift(ramp(f, t0 + 4, t0 + 22)) }}>Clari</div>
        <div style={{ marginTop: 22, fontFamily: BODY, fontWeight: 600, fontSize: 40, color: C.soft, ...lift(ramp(f, t0 + 12, t0 + 30)) }}>
          The private perimenopause tracker
        </div>
        <div style={{ marginTop: 46, display: 'flex', justifyContent: 'center', gap: 22, ...lift(ramp(f, t0 + 20, t0 + 38)) }}>
          <Img src={staticFile('app-store-badge.svg')} style={{ height: 92 }} />
          <Img src={staticFile('google-play-badge.png')} style={{ height: 92 }} />
        </div>
        <div style={{ marginTop: 34, fontFamily: BODY, fontWeight: 700, fontSize: 30, letterSpacing: 5, textTransform: 'uppercase', color: C.pink, ...lift(ramp(f, t0 + 28, t0 + 46)) }}>
          Free to download
        </div>
      </div>
    </>
  );
};

export const Ad: React.FC = () => (
  <AbsoluteFill style={{ background: '#0A0418', overflow: 'hidden' }}>
    <Fonts />
    <Footage src="ad/bed.mp4" at={T.bed} />
    <Footage src="ad/water.mp4" at={T.water} />
    <Footage src="ad/tea.mp4" at={T.tea} warm />
    <Footage src="ad/notes.mp4" at={T.notes} warm />
    <Sky from={T.cal[0]} />
    <CalCard />
    <Footage src="ad/dawn.mp4" at={T.dawn} warm />
    <Phone />

    <Line at={0} to={T.bed[1]} a="3am.|Awake* again.*" />
    <Line at={T.water[0]} to={T.water[1]} a="Too hot.|Then too cold." />
    <Line at={T.tea[0]} to={T.tea[1]} a="The morning|feels like fog.*" />
    <Line at={T.notes[0]} to={T.notes[1]} a="Notes for|everything." b="Because words|keep disappearing.*" bAt={T.notes[0] + 0.9} />
    <Line at={T.cal[0]} to={T.cal[1]} a="Then the GP asks:" b="how long has this|been going on?*" bAt={T.cal[0] + 0.8} />
    <Line at={T.log[0]} to={T.log[1]} a="Clari is a private|symptom diary." b="Tap how you feel.|The moon* fills* as it gets stronger.*" bAt={T.log[0] + 1.0} aStyle={{ fontSize: 80 }} />
    <Line at={T.sum[0]} to={T.sum[1]} a="Weeks of notes," b="one clear summary*|for your GP.*" bAt={T.sum[0] + 0.5} aStyle={{ fontSize: 84 }} />
    <Line at={T.dawn[0]} to={T.dawn[1]} a="Walk in with|the whole* picture.*" />
    <Sky from={T.end[0]} />
    <End />
    <Grain opacity={0.07} />
  </AbsoluteFill>
);
