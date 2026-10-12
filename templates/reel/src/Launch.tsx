import React from 'react';
import { AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from 'remotion';
import { BODY, C, DISPLAY, Fonts, Grain, Moon, Out, Petals, Show, Stars, Words, clamp, ease, easeIn, ramp, rnd, s } from './kit';

export const LAUNCH_FRAMES = s(42.5);

// Voiceover line starts (VO placed at 0.40s)
const T = {
  l1a: 0.4, l1b: 1.98,
  l2a: 4.41, l2b: 6.54,
  l3: 7.8, l3b: 8.95,
  l4: 10.63, l4b: 11.55,
  l5: 13.71, l5q: 14.45,
  l6: 17.01,
  l7: 19.21,
  l8: 22.76,
  l9: 26.24,
  l10: 28.85,
  l11a: 32.51, l11b: 34.22,
  l12a: 35.83, l12b: 36.67,
};

const centre: React.CSSProperties = {
  position: 'absolute',
  left: 110,
  right: 110,
  textAlign: 'center',
};
const big: React.CSSProperties = {
  fontFamily: DISPLAY,
  fontWeight: 500,
  fontSize: 98,
  lineHeight: 1.06,
  letterSpacing: -2,
  color: C.ink,
  textWrap: 'balance' as any,
};
const eyebrow: React.CSSProperties = {
  fontFamily: BODY,
  fontWeight: 800,
  fontSize: 27,
  letterSpacing: 6,
  textTransform: 'uppercase',
  color: C.pink,
};

/* ---------- Background ---------- */
const Sky: React.FC = () => {
  const f = useCurrentFrame();
  const dawn = ramp(f, s(18.9), s(21.5));
  const zoom = interpolate(f, [0, LAUNCH_FRAMES], [1.12, 1.0]);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: 'linear-gradient(180deg,#0A0418 0%,#170A33 38%,#2A1252 72%,#3E1C6E 100%)' }} />
      <AbsoluteFill
        style={{
          opacity: dawn,
          background: 'linear-gradient(180deg,#120726 0%,#2B1256 36%,#5B2A93 66%,#B86FA8 88%,#F2B7C5 100%)',
        }}
      />
      <AbsoluteFill style={{ transform: `scale(${zoom})` }}>
        <Stars maxY={1550} opacity={1 - dawn * 0.35} />
      </AbsoluteFill>
      {/* soft drifting haze */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(60% 30% at ${50 + Math.sin(f / 90) * 12}% ${78 + Math.cos(f / 110) * 4}%, rgba(249,201,216,${0.1 + dawn * 0.18}) 0%, rgba(249,201,216,0) 70%)`,
        }}
      />
      <AbsoluteFill style={{ background: 'radial-gradient(120% 80% at 50% 45%, rgba(0,0,0,0) 55%, rgba(5,2,12,0.55) 100%)' }} />
    </AbsoluteFill>
  );
};

/* ---------- Hook ---------- */
const Clock: React.FC = () => {
  const f = useCurrentFrame();
  // 03:04 present from frame 0, the colon breathes
  const colon = 0.35 + 0.65 * Math.abs(Math.cos((f / 30) * Math.PI));
  return (
    <div style={{ ...centre, top: 560, fontFamily: DISPLAY, fontWeight: 300, fontSize: 210, letterSpacing: -6, color: C.moon, lineHeight: 1 }}>
      3<span style={{ opacity: colon }}>:</span>04
      <span style={{ fontFamily: BODY, fontSize: 40, fontWeight: 700, letterSpacing: 4, marginLeft: 14, color: C.pink, verticalAlign: '0.9em' }}>
        AM
      </span>
    </div>
  );
};

const Vignette1: React.FC = () => (
  <Show from={0} to={s(4.3)}>
    <Out at={s(3.85)}>
      <Clock />
      <div style={{ ...centre, top: 860 }}>
        <Words text="Three in|the morning." at={s(T.l1a)} style={big} />
        <Words text="Soaked through,|again." at={s(T.l1b)} style={{ ...big, fontStyle: 'italic', color: C.pink, fontWeight: 400 }} />
      </div>
    </Out>
  </Show>
);

const Gone: React.FC<{ at: number }> = ({ at }) => {
  const f = useCurrentFrame();
  const letters = 'gone.'.split('');
  const appear = ramp(f, at, at + 10);
  return (
    <span style={{ display: 'inline-block', fontStyle: 'italic', color: C.pink, fontWeight: 400 }}>
      {letters.map((ch, i) => {
        const d0 = at + 16 + i * 3;
        const p = ramp(f, d0, d0 + 20, easeIn);
        return (
          <span
            key={i}
            style={{
              display: 'inline-block',
              opacity: appear * (1 - p),
              transform: `translate(${p * (rnd(i + 3) * 60 - 10)}px, ${-p * (50 + rnd(i) * 70)}px)`,
              filter: `blur(${(1 - appear) * 8 + p * 14}px)`,
            }}
          >
            {ch}
          </span>
        );
      })}
    </span>
  );
};

const Vignette2: React.FC = () => (
  <Show from={s(4.2)} to={s(7.75)}>
    <Out at={s(7.3)}>
      <div style={{ ...centre, top: 640 }}>
        <Words text="Mid-sentence," at={s(T.l2a)} style={{ ...eyebrow }} />
      </div>
      <div style={{ ...centre, top: 730 }}>
        <Words text="and the word|is just" at={s(T.l2a + 0.75)} style={big} />
        <span style={{ ...big }}>
          <Gone at={s(T.l2b)} />
        </span>
      </div>
    </Out>
  </Show>
);

const Vignette3: React.FC = () => {
  const f = useCurrentFrame();
  const beat = (t: number) => {
    const p = f - s(t);
    return p >= 0 && p < 10 ? Math.sin((p / 10) * Math.PI) : 0;
  };
  const pulse = 1 + 0.04 * (beat(8.2) + beat(8.55) + beat(9.25) + beat(9.6));
  return (
    <Show from={s(7.65)} to={s(10.55)}>
      <Out at={s(10.15)}>
        <div style={{ ...centre, top: 760, transform: `scale(${pulse})` }}>
          <Words text="Your heart|racing," at={s(T.l3)} style={big} />
          <Words text="for no reason|at all." at={s(T.l3b)} style={{ ...big, fontStyle: 'italic', color: C.pink, fontWeight: 400 }} />
        </div>
      </Out>
    </Show>
  );
};

const Strike: React.FC<{ at: number; children: React.ReactNode }> = ({ at, children }) => {
  const f = useCurrentFrame();
  const p = ramp(f, at, at + 14);
  return (
    <span style={{ position: 'relative', display: 'inline-block' }}>
      {children}
      <svg
        viewBox="0 0 100 20"
        preserveAspectRatio="none"
        style={{
          position: 'absolute',
          left: '-3%',
          width: '104%',
          top: '40%',
          height: '0.36em',
          overflow: 'visible',
          clipPath: `inset(-50% ${(1 - p) * 100}% -50% -2%)`,
        }}
      >
        <path d="M1 12 C 18 6, 36 15, 54 9 S 84 6, 99 10" fill="none" stroke={C.rose} strokeWidth="9" strokeLinecap="round" vectorEffect="non-scaling-stroke" />
      </svg>
    </span>
  );
};

const Stress: React.FC = () => (
  <Show from={s(10.45)} to={s(13.55)}>
    <Out at={s(13.15)}>
      <div style={{ ...centre, top: 760 }}>
        <Words text="And you keep|telling yourself" at={s(T.l4)} style={{ ...big, fontSize: 84 }} />
        <span style={{ ...big, fontSize: 84, display: 'block', whiteSpace: 'nowrap' }}>
          <Words text="it's" at={s(T.l4b)} style={{ ...big, fontSize: 84 }} />{' '}
          <Strike at={s(12.75)}>
            <Words text="just stress." at={s(T.l4b) + 3} style={{ ...big, fontSize: 84 }} />
          </Strike>
        </span>
      </div>
    </Out>
  </Show>
);

const GP: React.FC = () => {
  const f = useCurrentFrame();
  const lines = ['“How long has this', 'been going on?”'];
  const words = lines.join(' ').split(' ');
  const scatterAt = s(16.95);
  return (
    <Show from={s(13.55)} to={s(19.0)}>
      <div style={{ ...centre, top: 640 }}>
        <Out at={scatterAt} dur={16}>
          <Words text="Then the GP asks," at={s(T.l5)} style={eyebrow} />
        </Out>
      </div>
      <div style={{ ...centre, top: 730 }}>
        <span style={{ ...big, fontStyle: 'italic', fontWeight: 400, fontSize: 96 }}>
          {words.map((w, i) => {
            const a = s(T.l5q) + i * 4.5;
            const pin = ramp(f, a, a + 16);
            const d0 = scatterAt + rnd(i + 30) * 10;
            const p = ramp(f, d0, d0 + 26, easeIn);
            const dx = (rnd(i + 11) - 0.5) * 220;
            const dy = -40 - rnd(i + 19) * 160;
            return (
              <React.Fragment key={i}>
              <span
                style={{
                  display: 'inline-block',
                  whiteSpace: 'pre',
                  opacity: pin * (1 - p) * (1 - p),
                  transform: `translate(${p * dx}px, ${(1 - pin) * 40 + p * dy}px) rotate(${p * (rnd(i) - 0.5) * 30}deg)`,
                  filter: `blur(${(1 - pin) * 10 + p * 34}px)`,
                }}
              >
                {w}
                {i < words.length - 1 && i !== 3 ? ' ' : ''}
              </span>
              {i === 3 ? <br /> : null}
              </React.Fragment>
            );
          })}
        </span>
      </div>
      <div style={{ ...centre, top: 1090 }}>
        <Out at={s(18.35)} dur={14} rise={0}>
          <Words text="And your mind goes blank." at={s(T.l6 + 0.1)} stagger={3.5} style={{ fontFamily: BODY, fontSize: 40, fontWeight: 500, color: 'rgba(255,255,255,0.55)', letterSpacing: 0.5 }} />
        </Out>
      </div>
    </Show>
  );
};

/* ---------- Reveal ---------- */
const Reveal: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = s(18.85);
  const pop = spring({ frame: f - t0, fps, config: { damping: 15, stiffness: 70, mass: 1 } });
  const ring = ramp(f, t0, t0 + 40);
  const leave = ramp(f, s(21.55), s(22.25), easeIn);
  const word = ramp(f, t0 + 10, t0 + 30);
  return (
    <Show from={t0} to={s(22.4)}>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 520, display: 'flex', justifyContent: 'center', opacity: 1 - leave, transform: `translateY(${-leave * 120}px) scale(${1 - leave * 0.2})` }}>
        <div style={{ position: 'relative' }}>
          <div
            style={{
              position: 'absolute',
              left: '50%',
              top: '50%',
              width: 520,
              height: 520,
              marginLeft: -260,
              marginTop: -260,
              borderRadius: '50%',
              border: '2px solid rgba(255,243,214,0.6)',
              transform: `scale(${0.3 + ring * 1.1})`,
              opacity: (1 - ring) * 0.8,
            }}
          />
          <Moon size={230} glow={pop} style={{ transform: `scale(${pop}) rotate(${(1 - pop) * -25}deg)` }} />
        </div>
      </div>
      <div style={{ ...centre, top: 800, opacity: 1 - leave, transform: `translateY(${-leave * 120}px)` }}>
        <div
          style={{
            fontFamily: DISPLAY,
            fontWeight: 600,
            fontSize: 150,
            letterSpacing: -3,
            color: C.ink,
            opacity: word,
            transform: `translateY(${(1 - word) * 30}px)`,
            filter: `blur(${(1 - word) * 10}px)`,
          }}
        >
          Clari
        </div>
        <div style={{ marginTop: 26 }}>
          <Words text="A quiet, private place|to log how you feel." at={s(T.l7 + 0.1)} stagger={2.6} style={{ ...big, fontSize: 56, fontWeight: 400, color: C.soft, letterSpacing: -0.5 }} />
        </div>
      </div>
    </Show>
  );
};

const Branch: React.FC<{ from: number; to: number }> = ({ from, to }) => {
  const f = useCurrentFrame();
  const inP = ramp(f, from, from + 30);
  const outP = ramp(f, to - 12, to, easeIn);
  const sway = Math.sin(f / 40) * 1.4;
  return (
    <Show from={from} to={to}>
      <Img
        src={staticFile('blossom-branch.svg')}
        style={{
          position: 'absolute',
          top: -20,
          left: -70,
          width: 560,
          opacity: inP * (1 - outP),
          transform: `translate(${(1 - inP) * -60}px, ${(1 - inP) * -40}px) rotate(${sway}deg)`,
          transformOrigin: '0% 0%',
        }}
      />
    </Show>
  );
};

/* ---------- Phone ---------- */
const PHONE_W = 600;
const BEZEL = 13;
const SCREEN_W = PHONE_W - BEZEL * 2;
const SCREEN_H = Math.round((SCREEN_W * 1864) / 860);

const Clip: React.FC<{ src: string; from: number; to: number; trim?: number; fadeIn?: number }> = ({ src, from, to, trim = 0, fadeIn = 8 }) => {
  const f = useCurrentFrame();
  const p = ramp(f, from, from + fadeIn);
  return (
    <Sequence from={from} durationInFrames={to - from} layout="none">
      <div style={{ position: 'absolute', inset: 0, opacity: p, transform: `scale(${1.04 - p * 0.04})` }}>
        <OffthreadVideo src={staticFile(src)} trimBefore={trim} muted style={{ width: SCREEN_W, height: SCREEN_H, display: 'block' }} />
        {/* hide the screen-recording dot in the Dynamic Island */}
        <div style={{ position: 'absolute', left: (288 / 860) * SCREEN_W - 18, top: (59 / 1864) * SCREEN_H - 18, width: 36, height: 36, borderRadius: 18, background: '#000' }} />
      </div>
    </Sequence>
  );
};

const Phone: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const inAt = s(21.6);
  const rise = spring({ frame: f - inAt, fps, config: { damping: 18, stiffness: 80 } });
  const out = ramp(f, s(32.15), s(32.85), easeIn);
  const pdf = ramp(f, s(30.6), s(31.4));
  const tilt = Math.sin(f / 70) * 1.2;
  if (f < inAt || f > s(33)) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: (1080 - PHONE_W) / 2,
        top: 600,
        width: PHONE_W,
        transform: `translateY(${(1 - rise) * 1100 + out * 900}px) rotate(${tilt}deg) scale(${1 - pdf * 0.06})`,
        filter: `blur(${pdf * 3 + out * 6}px) brightness(${1 - pdf * 0.35})`,
        opacity: 1 - out,
      }}
    >
      <div
        style={{
          padding: BEZEL,
          borderRadius: 78,
          background: 'linear-gradient(145deg,#2A2238,#0B0712 40%,#1B1526)',
          boxShadow: '0 0 0 2px rgba(255,255,255,0.08), 0 60px 120px -30px rgba(5,0,15,0.85), 0 30px 60px -30px rgba(91,42,147,0.6)',
        }}
      >
        <div style={{ position: 'relative', width: SCREEN_W, height: SCREEN_H, borderRadius: 66, overflow: 'hidden', background: '#F6F1FC' }}>
          <Clip src="log.mp4" from={inAt} to={s(26.3)} fadeIn={1} />
          <Clip src="cal.mp4" from={s(26.1)} to={s(28.9)} trim={50} />
          <Clip src="sum.mp4" from={s(28.7)} to={s(33)} trim={0} />
          {/* glass sheen */}
          <div style={{ position: 'absolute', inset: 0, background: 'linear-gradient(115deg, rgba(255,255,255,0.10) 0%, rgba(255,255,255,0) 35%)', pointerEvents: 'none' }} />
        </div>
      </div>
    </div>
  );
};

const Caption: React.FC<{ from: number; to: number; a: string; b?: string; bAt?: number }> = ({ from, to, a, b, bAt }) => (
  <Show from={from} to={to}>
    <Out at={to - 10} dur={10}>
      <div style={{ ...centre, top: 300 }}>
        <Words text={a} at={from} stagger={2.4} style={{ ...big, fontSize: 64 }} />
        {b ? (
          <>
            <Words text={b} at={bAt ?? from + 12} stagger={2.4} style={{ ...big, fontSize: 64, fontStyle: 'italic', fontWeight: 400, color: C.pink }} />
          </>
        ) : null}
      </div>
    </Out>
  </Show>
);

const PDF: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = s(30.6);
  const p = spring({ frame: f - t0, fps, config: { damping: 16, stiffness: 70 } });
  const out = ramp(f, s(32.15), s(32.85), easeIn);
  if (f < t0 || f > s(33)) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: 540 - 330,
        top: 620,
        width: 660,
        transformOrigin: '50% 60%',
        transform: `translate(${p * 18}px, ${(1 - p) * 320 + out * 900}px) scale(${0.42 + p * 0.58}) rotate(${-p * 4}deg)`,
        opacity: Math.min(1, p * 2) * (1 - out),
      }}
    >
      <Img src={staticFile('pdf.webp')} style={{ width: 660, borderRadius: 10, display: 'block', boxShadow: '-24px 28px 0 -6px rgba(195,168,234,0.28), 0 60px 110px -30px rgba(0,0,0,0.75)' }} />
    </div>
  );
};

/* ---------- Statement + end card ---------- */
const Proof: React.FC = () => (
  <Show from={s(32.4)} to={s(35.75)}>
    <Out at={s(35.35)}>
      <div style={{ ...centre, top: 600 }}>
        <Words
          text="Walk in|with proof,"
          at={s(T.l11a)}
          stagger={3}
          style={{ ...big, fontSize: 112 }}
          wordStyle={(w) => (w.startsWith('proof') ? { fontStyle: 'italic', color: C.pink, fontWeight: 400 } : undefined)}
        />
        <Words text="not just|a feeling." at={s(T.l11b)} stagger={3} style={{ ...big, fontSize: 112 }} />
      </div>
    </Out>
  </Show>
);

const End: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t0 = s(35.6);
  const pop = spring({ frame: f - t0, fps, config: { damping: 14, stiffness: 60 } });
  const name = ramp(f, s(T.l12a), s(T.l12a) + 18);
  const tag = ramp(f, s(36.5), s(36.5) + 18);
  const badges = ramp(f, s(37.0), s(37.0) + 18);
  const small = ramp(f, s(37.6), s(37.6) + 18);
  if (f < t0) return null;
  const lift = (p: number): React.CSSProperties => ({ opacity: p, transform: `translateY(${(1 - p) * 26}px)`, filter: `blur(${(1 - p) * 8}px)` });
  return (
    <>
      <div style={{ position: 'absolute', left: 0, right: 0, top: 470, display: 'flex', justifyContent: 'center' }}>
        <Moon size={200} glow={pop} style={{ transform: `scale(${pop})` }} />
      </div>
      <div style={{ ...centre, top: 720 }}>
        <div style={{ fontFamily: DISPLAY, fontWeight: 600, fontSize: 180, letterSpacing: -4, color: C.ink, lineHeight: 1, ...lift(name) }}>Clari</div>
        <div style={{ marginTop: 26, fontFamily: BODY, fontWeight: 600, fontSize: 42, color: C.soft, ...lift(tag) }}>
          Private perimenopause &amp; menopause tracker
        </div>
        <div style={{ marginTop: 54, display: 'flex', justifyContent: 'center', gap: 22, ...lift(badges) }}>
          <Img src={staticFile('app-store-badge.svg')} style={{ height: 96 }} />
          <Img src={staticFile('google-play-badge.png')} style={{ height: 96 }} />
        </div>
        <div style={{ marginTop: 34, fontFamily: BODY, fontWeight: 700, fontSize: 30, letterSpacing: 5, textTransform: 'uppercase', color: C.pink, ...lift(small) }}>
          Free to download
        </div>
      </div>
    </>
  );
};

export const Launch: React.FC = () => {
  const f = useCurrentFrame();
  const fadeOut = ramp(f, LAUNCH_FRAMES - 12, LAUNCH_FRAMES);
  return (
    <AbsoluteFill style={{ background: '#0A0418', overflow: 'hidden' }}>
      <Fonts />
      <Sky />
      <Branch from={s(18.9)} to={s(22.3)} />
      <Branch from={s(35.6)} to={LAUNCH_FRAMES + 30} />
      <Petals from={s(19.2)} />
      <Vignette1 />
      <Vignette2 />
      <Vignette3 />
      <Stress />
      <GP />
      <Reveal />
      <Caption from={s(22.5)} to={s(26.15)} a="Tap a symptom." b="The moon fills|as it gets stronger." bAt={s(23.55)} />
      <Caption from={s(26.2)} to={s(28.75)} a="Weeks later," b="your patterns|start to show." bAt={s(26.85)} />
      <Caption from={s(28.8)} to={s(32.2)} a="Before your appointment," b="months become|one clear summary." bAt={s(30.0)} />
      <Phone />
      <PDF />
      <Proof />
      <End />
      <Grain />
      <AbsoluteFill style={{ background: '#000', opacity: fadeOut * 0.0 }} />
    </AbsoluteFill>
  );
};
