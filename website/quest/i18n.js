import {translateText} from './locale-core.js?v=1f251ee98b8c';
let lang='zh',messages=null;
try{lang=localStorage.getItem('tcl-quest-language')==='en'?'en':'zh';}catch{}
const textSources=new WeakMap(),attributeSources=new WeakMap();
export const language=()=>lang;
export const t=value=>lang==='en'?translateText(value,messages):String(value);
export async function initLanguage(){const r=await fetch(new URL('locales/en.json',import.meta.url),{cache:'no-cache'});if(!r.ok)throw Error('Could not load English text');messages=await r.json();}
export function setLanguage(value){lang=value==='en'?'en':'zh';try{localStorage.setItem('tcl-quest-language',lang);}catch{}document.documentElement.lang=lang==='en'?'en':'zh-CN';document.title=lang==='en'?'Tcl Quest · Chip Island Adventure':'Tcl Quest · 芯片岛冒险';document.querySelector('meta[name=description]')?.setAttribute('content',lang==='en'?'Learn Tcl through 20 illustrated missions, execution-driven stories, English videos and a real browser Tcl lab.':'在芯片岛闯关学 Tcl：20 个图文任务、执行驱动剧情、演示视频和真正的浏览器 Tcl 实验室。');}
const protectedText='pre,code,textarea,script,style,[data-verbatim],.line-numbers';
function textNode(node){
 if(node.parentElement?.closest(protectedText))return;
 let old=textSources.get(node);
 if(old&&node.nodeValue!==old.source&&node.nodeValue!==old.translation)old=null;
 const source=old?.source??node.nodeValue;
 const translated=lang==='en'?t(source):source;
 if(translated!==node.nodeValue)node.nodeValue=translated;
 textSources.set(node,{source,translation:translated});
}
export function localize(root=document.body){
 if(!root)return;if(root.nodeType===3){textNode(root);return;}
 const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);let node;while((node=walker.nextNode()))textNode(node);
 const elements=root.nodeType===1?[root,...root.querySelectorAll('[aria-label],[title],[placeholder],[alt]')]:[];
 for(const el of elements)for(const name of ['aria-label','title','placeholder','alt']){
  if(!el.hasAttribute(name))continue;
  const map=attributeSources.get(el)||{};let old=map[name];const now=el.getAttribute(name);
  if(old&&now!==old.source&&now!==old.translation)old=null;
  const source=old?.source??now,translated=lang==='en'?t(source):source;
  if(now!==translated)el.setAttribute(name,translated);map[name]={source,translation:translated};attributeSources.set(el,map);
 }
}
export function observeTranslations(){
 const observer=new MutationObserver(records=>{if(lang!=='en')return;const targets=new Set();for(const r of records){if(r.type==='childList'){for(const n of r.addedNodes)targets.add(n);}else targets.add(r.target);}for(const target of targets)if(target.isConnected)localize(target);});
 observer.observe(document.body,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['aria-label','title','placeholder','alt']});
}
