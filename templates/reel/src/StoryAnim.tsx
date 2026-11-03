import React from 'react';
import { AbsoluteFill, Img, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { Petals, Stars, rnd } from './kit';

/* Gentle motion over a finished story image: twinkling stars, a breathing moon glow, optional falling petals.
   The text is baked into the image, so nothing moves under the sticker area. */
export const STORY_FRAMES = 180;

const Glow: React.FC<{ x: number; y: number }> = ({ x, y }) => {
  const f = useCurrentFrame();
  const b = 0.55 + 0.45 * Math.sin((f / 180) * Math.PI * 2);
  return <div style={{ position: 'absolute', left: x - 260, top: y - 260, width: 520, height: 520, borderRadius: '50%',
    background: `radial-gradient(circle, rgba(255,232,200,${0.22 * b}) 0%, rgba(255,232,200,0) 65%)` }} />;
};

export const StoryAnim: React.FC<{ bg: string; petals?: boolean; moon?: [number, number] }> = ({ bg, petals, moon }) => {
  const f = useCurrentFrame();
  const fade = interpolate(f, [0, 8], [0, 1], { extrapolateRight: 'clamp' });
  return (
    <AbsoluteFill style={{ background: '#0E0620' }}>
      <Img src={staticFile(bg)} style={{ width: 1080, height: 1920 }} />
      {moon && <Glow x={moon[0]} y={moon[1]} />}
      <AbsoluteFill style={{ opacity: 0.55 * fade }}><Stars count={50} maxY={1100} /></AbsoluteFill>
      {petals && <Petals from={-120} count={10} />}
    </AbsoluteFill>
  );
};
