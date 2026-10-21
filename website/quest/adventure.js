import {storyActionSound} from './action-sounds.js?v=1f251ee98b8c';
import {language,t,localize} from './i18n.js?v=1f251ee98b8c';
import {getCast,portrait,sceneSVG} from './adventure-art.js?v=1f251ee98b8c';
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let current=null;
const motionKey='tcl-quest-motion';
function motionPreference(){try{const saved=localStorage.getItem(motionKey);if(saved!==null)return saved==='on';}catch{}return !matchMedia('(prefers-reduced-motion: reduce)').matches;}
export function clearAdventure(){current?.destroy();current=null;}
export function updateAdventure(event){current?.update(event);}
export function mountAdventure(root,lesson,storyboard,onLoad,{onAction=()=>{}}={}){
 clearAdventure();
 const isEn = language() === 'en';
 const cast = getCast(isEn);
 const npc = cast[lesson.world+1];
 const heroName = isEn ? 'Chip' : '芯芯';
 const abort = new AbortController();
 let step=0,selection=0,timer=null,motion=motionPreference(),mood='ready';
 const on=(element,event,fn)=>element.addEventListener(event,fn,{signal:abort.signal});

 const motionToggleText = isEn ? `Animation ${motion?'On':'Off'}` : `动作动画 ${motion?'开':'关'}`;
 const playBtnText = isEn ? '▶ Play Story' : '▶ 播放剧情';
 const pauseBtnText = isEn ? 'Ⅱ Pause Story' : 'Ⅱ 暂停剧情';
 const replayBtnText = isEn ? '↺ Replay Story' : '↺ 重播剧情';
 const restartBtnText = isEn ? 'Restart' : '从头看';
 const meetHeroAria = isEn ? `Meet ${heroName}` : '认识芯芯';
 const exploreTogetherText = isEn ? 'Explore Together' : '一起探索';
 const talkNpcAria = isEn ? `Talk with ${npc.name}` : `与${npc.name}对话`;
 const speakerSays = isEn ? `${npc.name} says` : `${npc.name}说`;
 const codeLabel = isEn ? 'Tcl Code for this Act' : '这一幕对应的 Tcl 代码';
 const beatsAria = isEn ? 'Select Storyboard Act' : '选择剧情分镜';
 const expTitle = isEn ? 'What if we change the input?' : '换个输入，故事会怎样？';
 const expDesc = isEn ? 'Visual demo of code execution (does not count toward completion). Send to the lab on the right to run live.' : '这里是任务代码的图解演示，不计通关。选择后可送到右侧实验室真实运行。';
 const variantsAria = isEn ? 'Switch demo input' : '切换演示输入';
 const previewLabel = isEn ? 'Expected output for selected input' : '所选代码的预期结果';
 const loadBtnText = isEn ? 'Send this demo to lab →' : '把这段演示送到实验室 →';
 const loadHint = isEn ? 'Replaces code in editor' : '会替换编辑器中的代码';
 const liveTitleDefault = isEn ? `${heroName}’s Live Echo` : '芯芯的实时回声';
 const liveMsgDefault = isEn ? `Run code in the lab, and ${heroName} will bring back real Tcl results.` : '在实验室运行代码，芯芯会带回真实的 Tcl 结果。';
 const npcRoleShort = npc.role.includes(' · ') ? npc.role.split(' · ')[1] : npc.role;

 root.innerHTML=`<section class="adventure ${motion?'':'still'}" aria-labelledby="scene-title"><header class="adventure-header"><div><span class="eyebrow">STORY IN MOTION · ${esc(storyboard.setting)}</span><h2 id="scene-title">${esc(storyboard.title)}</h2></div><button class="secondary motion-toggle" aria-pressed="${motion}">${motionToggleText}</button></header><div class="scene-layout"><div class="scene-left"><div class="adventure-canvas"></div><div class="scene-controls"><button class="scene-play primary" aria-label="${isEn?'Play story':'播放四幕图解'}">${playBtnText}</button><button class="scene-prev secondary" aria-label="${isEn?'Previous act':'上一幕'}">←</button><span class="scene-counter">${isEn?`Act 1 / 4`:'1 / 4 幕'}</span><button class="scene-next secondary" aria-label="${isEn?'Next act':'下一幕'}">→</button><button class="scene-restart secondary">${restartBtnText}</button></div></div><div class="scene-reading"><div class="scene-cast"><button class="scene-character" data-person="0" aria-label="${meetHeroAria}">${portrait('robot')}<span>${heroName}</span></button><span class="cast-between">${exploreTogetherText}</span><button class="scene-character" data-person="${lesson.world+1}" aria-label="${talkNpcAria}">${portrait(npc.kind)}<span>${npc.name}</span></button><span class="npc-role">${npcRoleShort}</span></div><div class="npc-dialogue"><strong class="scene-speaker">${speakerSays}</strong><h3 class="scene-beat-title"></h3><p class="scene-beat-text" role="status" aria-live="polite"></p></div><div class="scene-code-label">${codeLabel}</div><pre class="scene-code"><code></code></pre><span class="scene-line-hint"></span></div></div><div class="scene-beats" role="group" aria-label="${beatsAria}">${storyboard.steps.map((b,i)=>`<button data-beat="${i}" aria-pressed="${i===0}"><span>0${i+1}</span>${esc(b.title)}</button>`).join('')}</div><div class="scene-experiment"><div><strong>${expTitle}</strong><p>${expDesc}</p></div><div class="scene-variants" role="group" aria-label="${variantsAria}">${storyboard.variants.map((v,i)=>`<button class="secondary" data-variant="${i}" aria-pressed="${i===0}">${esc(v.label)}</button>`).join('')}</div><div class="scene-preview"><span>${previewLabel}</span><pre></pre></div><div class="scene-send"><button class="secondary scene-load">${loadBtnText}</button><span>${loadHint}</span></div></div><div class="scene-live" data-status="idle" aria-live="polite"><span class="live-indicator" aria-hidden="true"></span><div><strong class="live-title">${liveTitleDefault}</strong><p class="live-message">${liveMsgDefault}</p><pre class="live-output" hidden></pre></div></div></section>`;
 const el=root.querySelector('.adventure'),q=s=>el.querySelector(s);
 const variant=()=>storyboard.variants[selection];
 const pause=()=>{onAction(null);clearInterval(timer);timer=null;q('.scene-play').textContent=step===3?replayBtnText:playBtnText;q('.scene-play').setAttribute('aria-label',step===3?(isEn?'Replay story':'重播四幕图解'):(isEn?'Play story':'播放四幕图解'));};
 function render(){
  const v=variant(),beat=storyboard.steps[step];
  const art=sceneSVG(lesson.id,lesson.world,v.props,step,mood);
  q('.adventure-canvas').innerHTML=art.replace('class="adventure-svg"','class="adventure-svg scene-wide"')+art.replace('class="adventure-svg"','class="adventure-svg scene-close"').replace('viewBox="0 0 960 360"','viewBox="245 75 490 260"');
  q('.scene-speaker').textContent=isEn?`${npc.name} says`:`${npc.name}说`;
  q('.scene-beat-title').textContent=beat.title;
  q('.scene-beat-text').textContent=beat.text;
  const code=v.code.split('\n');
  const line=Math.min(beat.line,code.length-1),start=Math.max(0,line-1),end=Math.min(code.length,line+2);
  q('.scene-code code').innerHTML=code.slice(start,end).map((s,i)=>`<span class="${start+i===line?'highlight-line':''}"><b aria-hidden="true">${start+i+1}</b>${esc(s)||' '}</span>`).join('');
  q('.scene-line-hint').textContent=isEn?`Line ${line+1} highlighted · Illustrated sequence for intuition, not a line-by-line debugger`:`第 ${line+1} 行高亮 · 图解顺序帮助理解，不是逐行调试器`;
  q('.scene-counter').textContent=isEn?`Act ${step+1} / 4`:`${step+1} / 4 幕`;if(!timer){q('.scene-play').textContent=step===3?replayBtnText:playBtnText;q('.scene-play').setAttribute('aria-label',step===3?(isEn?'Replay story':'重播四幕图解'):(isEn?'Play story':'播放四幕图解'));}
  q('.scene-prev').disabled=step===0;q('.scene-next').disabled=step===3;
  el.querySelectorAll('[data-beat]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.beat===step)));
  el.querySelectorAll('[data-variant]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.variant===selection)));
  q('.scene-preview pre').textContent=v.props.error?(isEn?`Tcl Error: ${v.props.error}`:`Tcl 错误：${v.props.error}`):v.output||(isEn?'(Empty output)':'（空输出）');localize(el);
 }
 function move(next){const previous=step;step=next;render();if(step>previous&&!document.hidden){const cue=storyActionSound(lesson.id,step,variant().props);if(cue)onAction(cue);}}
 on(q('.scene-play'),'click',()=>{if(timer){pause();return;}if(step===3)step=0;render();q('.scene-play').textContent=pauseBtnText;q('.scene-play').setAttribute('aria-label',isEn?'Pause story':'暂停四幕图解');timer=setInterval(()=>{move(step+1);if(step===3){clearInterval(timer);timer=null;q('.scene-play').textContent=replayBtnText;q('.scene-play').setAttribute('aria-label',isEn?'Replay story':'重播四幕图解');}},2200);});
 on(q('.scene-prev'),'click',()=>{pause();move(Math.max(0,step-1));});
 on(q('.scene-next'),'click',()=>{pause();move(Math.min(3,step+1));});
 on(q('.scene-restart'),'click',()=>{pause();step=0;render();});
 el.querySelectorAll('[data-beat]').forEach(b=>on(b,'click',()=>{pause();move(+b.dataset.beat);}));
 el.querySelectorAll('[data-variant]').forEach(b=>on(b,'click',()=>{pause();selection=+b.dataset.variant;step=0;render();}));
 el.querySelectorAll('[data-person]').forEach(b=>on(b,'click',()=>{pause();const c=cast[+b.dataset.person];q('.scene-speaker').textContent=isEn?`${c.name} says`:`${c.name}说`;q('.scene-beat-title').textContent=c.role;q('.scene-beat-text').textContent=c.intro;}));
 on(q('.scene-load'),'click',()=>{
  onLoad(variant().code);
  q('.live-title').textContent=isEn?`${heroName}: Demo loaded into lab`:'芯芯：演示已经放进实验室';
  q('.live-message').textContent=isEn?'Click "Run Code" to inspect output. Demo input may differ from mission tests; submission evaluates original tests.':'点击「运行代码」看真实输出。演示输入可能与任务不同；提交挑战仍按原任务检查。';
 });
 on(q('.motion-toggle'),'click',()=>{
  motion=!motion;el.classList.toggle('still',!motion);
  q('.motion-toggle').textContent=isEn?`Animation ${motion?'On':'Off'}`:`动作动画 ${motion?'开':'关'}`;
  q('.motion-toggle').setAttribute('aria-pressed',String(motion));
  try{localStorage.setItem(motionKey,motion?'on':'off');}catch{}
 });
 on(document,'visibilitychange',()=>{if(document.hidden)pause();});
 current={destroy(){pause();abort.abort();},update(event){
  const status=event.status;
  const messages=isEn?{
   loading:[`${heroName} is executing code`,'Waking up native Tcl engine; results arriving shortly.'],
   run:[`${heroName} brought back results`,'Real execution output shown below. Click Check Mission to test requirements.'],
   error:[`${heroName}: Let’s debug together`,'Execution hit an issue. Review error diagnostics in the lab; code is preserved.'],
   failed:['NPC: Keep going, check the hints','Code executed, but some mission checks did not pass yet. Compare with the checklist.'],
   passed:[`${npc.name}: Mission Complete!`,`All checks passed! ${heroName} and you completed this step of the adventure.`],
   edited:[`${heroName}: Draft changed`,'Previous execution shown below. Click Run Code to inspect updated output.']
  }:{
   loading:['芯芯正在执行代码','正在唤醒真实 Tcl 引擎，结果马上送达。'],
   run:['芯芯带回了运行结果','下面是这次代码的真实结果；提交挑战后才会检查是否完成任务。'],
   error:['芯芯：我们一起排查一下','这次执行遇到问题。看看实验室里的错误说明，代码仍然保留着。'],
   failed:['NPC：再检查一小步','代码已经运行，但还没有通过全部任务检查。请对照实验室的检查项和提示。'],
   passed:[`${npc.name}：任务完成！`,'全部任务检查通过，芯芯和你一起完成了这一站的冒险。'],
   edited:['芯芯：草稿已经改变','下方保留上次运行的结果；点击运行，查看修改后的表现。']
  };
  const [title,message]=messages[status]||messages.run;
  q('.scene-live').dataset.status=status;q('.live-title').textContent=title;q('.live-message').textContent=message;
  if(event.output!==undefined){
   q('.live-output').hidden=!event.output;
   q('.live-output').textContent=event.output.length>1800?event.output.slice(0,1800)+(isEn?'\n… (Full output in lab)':'\n…（完整结果见实验室）'):event.output;
  }
  mood=status==='passed'?'success':status==='loading'?'working':'ready';
  q('.scene-character[data-person="0"]').innerHTML=portrait('robot',mood)+`<span>${heroName}</span>`;
  if(status==='passed'){pause();selection=0;step=3;render();}else if(status!=='edited')render();
 }};
 render();
}
