import React from 'react';
import { Composition } from 'remotion';
import { Launch, LAUNCH_FRAMES } from './Launch';
import { Joints, JOINTS_FRAMES } from './Joints';
import { Ad, AD_FRAMES } from './Ad';
import { Myths, MYTHS_FRAMES } from './Myths';
import { Day, DAY_FRAMES } from './Day';
import { Page, PAGE_FRAMES } from './Page';
import { StoryAnim, STORY_FRAMES } from './StoryAnim';

export const Root: React.FC = () => (
  <>
    <Composition id="Launch" component={Launch} durationInFrames={LAUNCH_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Joints" component={Joints} durationInFrames={JOINTS_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Ad" component={Ad} durationInFrames={AD_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Myths" component={Myths} durationInFrames={MYTHS_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Day" component={Day} durationInFrames={DAY_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="Page" component={Page} durationInFrames={PAGE_FRAMES} fps={30} width={1080} height={1920} />
    <Composition id="S04" component={StoryAnim} durationInFrames={STORY_FRAMES} fps={30} width={1080} height={1920} defaultProps={{ bg: 'st/s04.png', moon: [909, 335] as [number, number] }} />
    <Composition id="S13" component={StoryAnim} durationInFrames={STORY_FRAMES} fps={30} width={1080} height={1920} defaultProps={{ bg: 'st/s13.png' }} />
    <Composition id="S30" component={StoryAnim} durationInFrames={STORY_FRAMES} fps={30} width={1080} height={1920} defaultProps={{ bg: 'st/s30.png', petals: true }} />
  </>
);
