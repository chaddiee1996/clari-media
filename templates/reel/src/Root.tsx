import React from 'react';
import { Composition } from 'remotion';
import { Launch, LAUNCH_FRAMES } from './Launch';
import { Joints, JOINTS_FRAMES } from './Joints';

export const Root: React.FC = () => (
  <>
    <Composition id="Launch" component={Launch} durationInFrames={LAUNCH_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Joints" component={Joints} durationInFrames={JOINTS_FRAMES} fps={30} width={1080} height={1920} />
  </>
);
