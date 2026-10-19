import {storyActionSound} from './action-sounds.js?v=1f251ee98b8c';
import {t,localize} from './i18n.js?v=1f251ee98b8c';
import {CAST,portrait,sceneSVG} from './adventure-art.js?v=1f251ee98b8c';
const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
let current=null;
const motionKey='tcl-quest-motion';
function motionPreference(){try{const saved=localStorage.getItem(motionKey);if(saved!==null)return saved==='on';}catch{}return !matchMedia('(prefers-reduced-motion: reduce)').matches;}
export function clearAdventure(){current?.destroy();current=null;}
export function updateAdventure(event){current?.update(event);}
export function mountAdventure(root,lesson,storyboard,onLoad,{onAction=()=>{}}={}){
 clearAdventure();
 const npc=CAST[lesson.world+1],abort=new AbortController();
 let step=0,selection=0,timer=null,motion=motionPreference(),mood='ready';
 const on=(element,event,fn)=>element.addEventListener(event,fn,{signal:abort.signal});
 root.innerHTML=`<section class="adventure ${motion?'':'still'}" aria-labelledby="scene-title"><header class="adventure-header"><div><span class="eyebrow">STORY IN MOTION · ${esc(storyboard.setting)}</span><h2 id="scene-title">${esc(storyboard.title)}</h2></div><button class="secondary motion-toggle" aria-pressed="${motion}">动作动画 ${motion?'开':'关'}</button></header><div class="scene-layout"><div class="scene-left"><div class="adventure-canvas"></div><div class="scene-controls"><button class="scene-play primary" aria-label="播放四幕图解">▶ 播放剧情</button><button class="scene-prev secondary" aria-label="上一幕">←</button><span class="scene-counter">1 / 4 幕</span><button class="scene-next secondary" aria-label="下一幕">→</button><button class="scene-restart secondary">从头看</button></div></div><div class="scene-reading"><div class="scene-cast"><button class="scene-character" data-person="0" aria-label="认识芯芯">${portrait('robot')}<span>芯芯</span></button><span class="cast-between">一起探索</span><button class="scene-character" data-person="${lesson.world+1}" aria-label="与${npc.name}对话">${portrait(npc.kind)}<span>${npc.name}</span></button><span class="npc-role">${npc.role.split(' · ')[1]}</span></div><div class="npc-dialogue"><strong class="scene-speaker">${npc.name}说</strong><h3 class="scene-beat-title"></h3><p class="scene-beat-text" role="status" aria-live="polite"></p></div><div class="scene-code-label">这一幕对应的 Tcl 代码</div><pre class="scene-code"><code></code></pre><span class="scene-line-hint"></span></div></div><div class="scene-beats" role="group" aria-label="选择剧情分镜">${storyboard.steps.map((b,i)=>`<button data-beat="${i}" aria-pressed="${i===0}"><span>0${i+1}</span>${esc(b.title)}</button>`).join('')}</div><div class="scene-experiment"><div><strong>换个输入，故事会怎样？</strong><p>这里是任务代码的图解演示，不计通关。选择后可送到右侧实验室真实运行。</p></div><div class="scene-variants" role="group" aria-label="切换演示输入">${storyboard.variants.map((v,i)=>`<button class="secondary" data-variant="${i}" aria-pressed="${i===0}">${esc(v.label)}</button>`).join('')}</div><div class="scene-preview"><span>所选代码的预期结果</span><pre></pre></div><div class="scene-send"><button class="secondary scene-load">把这段演示送到实验室 →</button><span>会替换编辑器中的代码</span></div></div><div class="scene-live" data-status="idle" aria-live="polite"><span class="live-indicator" aria-hidden="true"></span><div><strong class="live-title">芯芯的实时回声</strong><p class="live-message">在实验室运行代码，芯芯会带回真实的 Tcl 结果。</p><pre class="live-output" hidden></pre></div></div></section>`;
 const el=root.querySelector('.adventure'),q=s=>el.querySelector(s);
 const variant=()=>storyboard.variants[selection];
 const pause=()=>{onAction(null);clearInterval(timer);timer=null;q('.scene-play').textContent=step===3?'↺ 重播剧情':'▶ 播放剧情';q('.scene-play').setAttribute('aria-label',step===3?'重播四幕图解':'播放四幕图解');};
 function render(){
  const v=variant(),beat=storyboard.steps[step];
  const art=sceneSVG(lesson.id,lesson.world,v.props,step,mood);
  q('.adventure-canvas').innerHTML=art.replace('class="adventure-svg"','class="adventure-svg scene-wide"')+art.replace('class="adventure-svg"','class="adventure-svg scene-close"').replace('viewBox="0 0 960 360"','viewBox="245 75 490 260"');
  q('.scene-speaker').textContent=`${npc.name}说`;
  q('.scene-beat-title').textContent=beat.title;
  q('.scene-beat-text').textContent=beat.text;
  const code=v.code.split('\n');
  // Only show a small actual excerpt; never claim that this is a Tcl debugger.
  const line=Math.min(beat.line,code.length-1),start=Math.max(0,line-1),end=Math.min(code.length,line+2);
  q('.scene-code code').innerHTML=code.slice(start,end).map((s,i)=>`<span class="${start+i===line?'highlight-line':''}"><b aria-hidden="true">${start+i+1}</b>${esc(s)||' '}</span>`).join('');
  q('.scene-line-hint').textContent=`第 ${line+1} 行高亮 · 图解顺序帮助理解，不是逐行调试器`;
  q('.scene-counter').textContent=`${step+1} / 4 幕`;if(!timer){q('.scene-play').textContent=step===3?'↺ 重播剧情':'▶ 播放剧情';q('.scene-play').setAttribute('aria-label',step===3?'重播四幕图解':'播放四幕图解');}
  q('.scene-prev').disabled=step===0;q('.scene-next').disabled=step===3;
  el.querySelectorAll('[data-beat]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.beat===step)));
  el.querySelectorAll('[data-variant]').forEach(b=>b.setAttribute('aria-pressed',String(+b.dataset.variant===selection)));
  q('.scene-preview pre').textContent=v.props.error?t(`Tcl 错误：${v.props.error}`):v.output||t('（空输出）');localize(el);
 }
 function move(next){const previous=step;step=next;render();if(step>previous&&!document.hidden){const cue=storyActionSound(lesson.id,step,variant().props);if(cue)onAction(cue);}}
 on(q('.scene-play'),'click',()=>{if(timer){pause();return;}if(step===3)step=0;render();q('.scene-play').textContent='Ⅱ 暂停剧情';q('.scene-play').setAttribute('aria-label','暂停四幕图解');timer=setInterval(()=>{move(step+1);if(step===3){clearInterval(timer);timer=null;q('.scene-play').textContent='↺ 重播剧情';q('.scene-play').setAttribute('aria-label','重播四幕图解');}},2200);});
 on(q('.scene-prev'),'click',()=>{pause();move(Math.max(0,step-1));});
 on(q('.scene-next'),'click',()=>{pause();move(Math.min(3,step+1));});
 on(q('.scene-restart'),'click',()=>{pause();step=0;render();});
 el.querySelectorAll('[data-beat]').forEach(b=>on(b,'click',()=>{pause();move(+b.dataset.beat);}));
 el.querySelectorAll('[data-variant]').forEach(b=>on(b,'click',()=>{pause();selection=+b.dataset.variant;step=0;render();}));
 el.querySelectorAll('[data-person]').forEach(b=>on(b,'click',()=>{pause();const c=CAST[+b.dataset.person];q('.scene-speaker').textContent=`${c.name}说`;q('.scene-beat-title').textContent=c.role;q('.scene-beat-text').textContent=c.intro;}));
 on(q('.scene-load'),'click',()=>{onLoad(variant().code);q('.live-title').textContent='芯芯：演示已经放进实验室';q('.live-message').textContent='点击「运行代码」看真实输出。演示输入可能与任务不同；提交挑战仍按原任务检查。';});
 on(q('.motion-toggle'),'click',()=>{motion=!motion;el.classList.toggle('still',!motion);q('.motion-toggle').textContent=`动作动画 ${motion?'开':'关'}`;q('.motion-toggle').setAttribute('aria-pressed',String(motion));try{localStorage.setItem(motionKey,motion?'on':'off');}catch{}});
 on(document,'visibilitychange',()=>{if(document.hidden)pause();});
 current={destroy(){pause();abort.abort();},update(event){
  const status=event.status;
  const messages={loading:['芯芯正在执行代码','正在唤醒真实 Tcl 引擎，结果马上送达。'],run:['芯芯带回了运行结果','下面是这次代码的真实结果；提交挑战后才会检查是否完成任务。'],error:['芯芯：我们一起排查一下','这次执行遇到问题。看看实验室里的错误说明，代码仍然保留着。'],failed:['NPC：再检查一小步','代码已经运行，但还没有通过全部任务检查。请对照实验室的检查项和提示。'],passed:[`${npc.name}：任务完成！`,'全部任务检查通过，芯芯和你一起完成了这一站的冒险。'],edited:['芯芯：草稿已经改变','下方保留上次运行的结果；点击运行，查看修改后的表现。']};
  const [title,message]=messages[status]||messages.run;
  q('.scene-live').dataset.status=status;q('.live-title').textContent=title;q('.live-message').textContent=message;
  if(event.output!==undefined){q('.live-output').hidden=!event.output;q('.live-output').textContent=event.output.length>1800?event.output.slice(0,1800)+'\n…（完整结果见实验室）':event.output;}
  mood=status==='passed'?'success':status==='loading'?'working':'ready';
  q('.scene-character[data-person="0"]').innerHTML=portrait('robot',mood)+'<span>芯芯</span>';
  // Only successful challenge validation advances the canonical story to its ending.
  if(status==='passed'){pause();selection=0;step=3;render();}else if(status!=='edited')render();
 }};
 render();
}
