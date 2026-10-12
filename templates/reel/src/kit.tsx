import React from 'react';
import { AbsoluteFill, Easing, interpolate, staticFile, useCurrentFrame, continueRender, delayRender } from 'remotion';

export const FPS = 30;
export const s = (sec: number) => Math.round(sec * FPS);

export const C = {
  ink: '#FFFFFF',
  soft: 'rgba(255,255,255,0.78)',
  pink: '#F9C9D8',
  rose: '#E8628F',
  moon: '#FFF3D6',
  lilac: '#C3A8EA',
};
export const DISPLAY = 'Fraunces, Georgia, serif';
export const BODY = 'Figtree, Helvetica, Arial, sans-serif';

const fontHandle = { done: false };
export const Fonts: React.FC = () => {
  const [h] = React.useState(() => (fontHandle.done ? null : delayRender('fonts')));
  React.useEffect(() => {
    const faces = [
      new FontFace('Fraunces', `url(${staticFile('fraunces.woff2')})`, { weight: '100 900', style: 'normal' }),
      new FontFace('Fraunces', `url(${staticFile('fraunces-italic.woff2')})`, { weight: '100 900', style: 'italic' }),
      new FontFace('Figtree', `url(${staticFile('figtree.woff2')})`, { weight: '300 900', style: 'normal' }),
    ];
    Promise.all(faces.map((f) => f.load().then((ff) => (document as any).fonts.add(ff)))).then(() => {
      fontHandle.done = true;
      if (h !== null) continueRender(h);
    });
  }, [h]);
  return null;
};

export const ease = Easing.bezier(0.22, 1, 0.36, 1);
export const easeIn = Easing.bezier(0.55, 0, 0.75, 0.2);
export const clamp = { extrapolateLeft: 'clamp', extrapolateRight: 'clamp' } as const;

export const ramp = (f: number, a: number, b: number, e = ease) => interpolate(f, [a, b], [0, 1], { ...clamp, easing: e });

// deterministic pseudo random
export const rnd = (i: number) => {
  const x = Math.sin(i * 127.1 + 311.7) * 43758.5453;
  return x - Math.floor(x);
};

/** Word-by-word reveal: rise, unblur, fade in. */
export const Words: React.FC<{
  text: string;
  at: number; // frame
  stagger?: number;
  dur?: number;
  style?: React.CSSProperties;
  wordStyle?: (w: string, i: number) => React.CSSProperties | undefined;
  render?: (w: string, i: number) => React.ReactNode;
}> = ({ text, at, stagger = 2.4, dur = 16, style, wordStyle, render }) => {
  const f = useCurrentFrame();
  const lines = text.split('|');
  let idx = 0;
  return (
    <span style={style}>
      {lines.map((line, li) => {
        const words = line.split(' ');
        return (
          <span key={li} style={{ display: lines.length > 1 ? 'block' : 'inline', whiteSpace: 'nowrap' }}>
            {words.map((w, wi) => {
              const i = idx++;
              const p = ramp(f, at + i * stagger, at + i * stagger + dur);
              return (
                <span
                  key={wi}
                  style={{
                    display: 'inline-block',
                    opacity: p,
                    transform: `translateY(${(1 - p) * 0.42}em)`,
                    filter: `blur(${(1 - p) * 10}px)`,
                    whiteSpace: 'pre',
                    ...(wordStyle ? wordStyle(w, i) : {}),
                  }}
                >
                  {render ? render(w, i) : w}
                  {wi < words.length - 1 ? ' ' : ''}
                </span>
              );
            })}
          </span>
        );
      })}
    </span>
  );
};

/** Fades and lifts a block out. */
export const Out: React.FC<{ at: number; dur?: number; children: React.ReactNode; style?: React.CSSProperties; rise?: number }> = ({
  at,
  dur = 12,
  children,
  style,
  rise = 30,
}) => {
  const f = useCurrentFrame();
  const p = ramp(f, at, at + dur, easeIn);
  return (
    <div style={{ opacity: 1 - p, transform: `translateY(${-p * rise}px)`, filter: `blur(${p * 8}px)`, ...style }}>{children}</div>
  );
};

/** Visible only within [from, to) frames. */
export const Show: React.FC<{ from: number; to: number; children: React.ReactNode }> = ({ from, to, children }) => {
  const f = useCurrentFrame();
  if (f < from || f >= to) return null;
  return <>{children}</>;
};

/** Animated film grain. */
export const Grain: React.FC<{ opacity?: number }> = ({ opacity = 0.06 }) => {
  const f = useCurrentFrame();
  const seed = Math.floor(f / 2) % 6;
  return (
    <AbsoluteFill style={{ pointerEvents: 'none', mixBlendMode: 'overlay', opacity }}>
      <img src={staticFile(`grain${seed}.png`)} style={{ width: 1080, height: 1920, imageRendering: 'pixelated' }} />
    </AbsoluteFill>
  );
};

/** Twinkling star field. */
export const Stars: React.FC<{ count?: number; maxY?: number; opacity?: number }> = ({ count = 110, maxY = 1500, opacity = 1 }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ opacity }}>
      <svg width="1080" height="1920">
        {Array.from({ length: count }).map((_, i) => {
          const x = rnd(i) * 1080;
          const y = rnd(i + 500) * maxY;
          const r = 0.8 + rnd(i + 900) * 1.7;
          const tw = 0.35 + 0.65 * Math.abs(Math.sin(f / 30 * (0.6 + rnd(i + 77) * 1.4) + rnd(i + 3) * 6));
          return <circle key={i} cx={x} cy={y} r={r} fill="#FFF8EA" opacity={tw * (0.35 + rnd(i + 41) * 0.65)} />;
        })}
        {Array.from({ length: 7 }).map((_, i) => {
          const x = 80 + rnd(i + 1200) * 920;
          const y = 120 + rnd(i + 1300) * (maxY * 0.6);
          const sc = 0.8 + rnd(i + 1400) * 0.9;
          const tw = 0.4 + 0.6 * Math.abs(Math.sin(f / 30 * 0.9 + i));
          return (
            <path
              key={'s' + i}
              d="M0 -9 Q0 0 9 0 Q0 0 0 9 Q0 0 -9 0 Q0 0 0 -9Z"
              fill="#FFF3D6"
              opacity={tw}
              transform={`translate(${x} ${y}) scale(${sc})`}
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};

/** Crescent moon with soft glow. */
export const Moon: React.FC<{ size: number; glow?: number; style?: React.CSSProperties }> = ({ size, glow = 1, style }) => (
  <div style={{ position: 'relative', width: size, height: size, ...style }}>
    <div
      style={{
        position: 'absolute',
        inset: -size * 1.1,
        borderRadius: '50%',
        background: `radial-gradient(circle, rgba(255,228,236,${0.32 * glow}) 0%, rgba(249,201,216,${0.12 * glow}) 35%, rgba(249,201,216,0) 68%)`,
      }}
    />
    <svg width={size} height={size} viewBox="0 0 100 100" style={{ position: 'absolute', inset: 0 }}>
      <defs>
        <radialGradient id="mg" cx="0.32" cy="0.3" r="0.9">
          <stop offset="0" stopColor="#FFFBEE" />
          <stop offset="0.6" stopColor="#FFEFC9" />
          <stop offset="1" stopColor="#F2C9A0" />
        </radialGradient>
        <mask id="mm">
          <rect width="100" height="100" fill="#fff" />
          <circle cx="66" cy="34" r="36" fill="#000" />
        </mask>
      </defs>
      <circle cx="50" cy="50" r="44" fill="url(#mg)" mask="url(#mm)" />
    </svg>
  </div>
);

/** A single falling blossom petal field. */
export const Petals: React.FC<{ from: number; count?: number }> = ({ from, count = 9 }) => {
  const f = useCurrentFrame();
  const t = f - from;
  if (t < 0) return null;
  return (
    <AbsoluteFill style={{ pointerEvents: 'none' }}>
      <svg width="1080" height="1920">
        {Array.from({ length: count }).map((_, i) => {
          const speed = 1.6 + rnd(i + 60) * 1.6;
          const y = -60 + ((t * speed + rnd(i + 20) * 2200) % 2050);
          const x = rnd(i + 90) * 1080 + Math.sin((t + i * 40) / 45) * 50;
          const rot = (t * (1 + rnd(i) * 2) + i * 50) % 360;
          const sc = 0.9 + rnd(i + 10) * 1.1;
          const op = Math.min(1, t / 30) * (0.55 + rnd(i + 5) * 0.4);
          return (
            <path
              key={i}
              d="M0 0 C-5.2 -4 -5.8 -11 -1.3 -13.2 L0 -11.4 L1.3 -13.2 C5.8 -11 5.2 -4 0 0Z"
              fill={i % 2 ? '#FBD3E0' : '#F7A9C3'}
              opacity={op}
              transform={`translate(${x} ${y}) rotate(${rot}) scale(${sc * 1.5})`}
            />
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
