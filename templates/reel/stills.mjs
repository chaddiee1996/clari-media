import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'path';
const times=process.argv.slice(2).map(Number);
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts')});
const opts={serveUrl,id:process.env.COMP||'Launch',browserExecutable:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',chromiumOptions:{gl:'swangle'}};
const composition=await selectComposition(opts);
for(const t of times){const frame=Math.round(t*30);await renderStill({...opts,composition,frame,output:`out/${process.env.COMP||'Launch'}-${t}.png`,scale:0.5});console.log('done',t);}
