import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import path from 'path';
const serveUrl=await bundle({entryPoint:path.resolve('src/index.ts')});
const opts={serveUrl,id:process.env.COMP||'Launch',browserExecutable:'/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell',chromiumOptions:{gl:'swangle'}};
const composition=await selectComposition(opts);
let last=0;
await renderMedia({...opts,composition,codec:'h264',crf:16,muted:true,concurrency:2,outputLocation:'out/'+(process.env.COMP||'Launch')+'-silent.mp4',onProgress:({progress})=>{if(progress-last>0.1){last=progress;console.log(Math.round(progress*100)+'%')}}});
console.log('rendered');
