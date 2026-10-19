import {createCelebration} from './celebrate.js?v=1f251ee98b8c';
import {createSoundPlayer} from './sound.js?v=1f251ee98b8c';
import {initLanguage,language,setLanguage,t,localize,observeTranslations} from './i18n.js?v=1f251ee98b8c';
import {mountRuntime,clearRuntime,runtimeSnapshot,startRuntime,pushRuntime,finishRuntime,editRuntime,afterRuntime} from './live-runtime.js?v=1f251ee98b8c';
import {mountAdventure,clearAdventure,updateAdventure} from './adventure.js?v=1f251ee98b8c';
import {CAST,portrait,partyHTML,bindParty,setArtTranslator} from './adventure-art.js?v=1f251ee98b8c';
const $ = (q) => document.querySelector(q);
const esc = (v) => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
document.querySelector('.skip').addEventListener('click',e=>{e.preventDefault();$('#main').focus();$('#main').scrollIntoView();});
const KEY='tcl-quest-progress-v1';
let data, storyboards, courses, stories, viewGeneration=0, lastExecution=null, active=null, busy=false, nextReward=1;
let state={version:1,completed:[],drafts:{},quiz:[]};
const celebrations=createCelebration();
const sceneAudio={onAction:cue=>{if(cue)void audio.play(cue,{channel:'scene'});else audio.stop('scene');}};
const SOUND_KEY='tcl-quest-sound-v1';
let audioStatus='off';
const audioMessages={
 off:'音效已关闭。打开开关可试听；点击、动作、答题和通关都有音效。',
 pending:'音效等待启用。点击开关或运行代码可重试。',
 ready:'音效已开启。打开开关可试听；点击、动作、答题和通关都有音效。',
 blocked:'浏览器暂未允许播放音效。请关闭再打开音效，并检查标签页是否静音。',
 unsupported:'此浏览器暂不支持游戏音效。'
};
function refreshSound(){
 $('#sound').textContent=t('音效 '+(audio.enabled?'开':'关'));
 $('#sound').setAttribute('aria-pressed',String(audio.enabled));
 $('#sound').dataset.audioState=audioStatus;
 $('#sound').title=t(audioMessages[audioStatus]);
 $('#sound-status').textContent=t(audioMessages[audioStatus]);
}
const audio=createSoundPlayer({onStatus:value=>{if(audioStatus!==value){audioStatus=value;refreshSound();}}});
let savedSound=false;try{savedSound=localStorage.getItem(SOUND_KEY)==='on';}catch{}
audio.setEnabled(savedSound,{preview:false});refreshSound();
$('#sound').onclick=()=>{
 const enabled=!audio.enabled;
 const preview=audio.setEnabled(enabled);
 try{localStorage.setItem(SOUND_KEY,enabled?'on':'off');}catch{}
 preview.then(ok=>{if(audio.enabled)toast(ok?'音效已开启，正在播放试听音。':audioMessages[audioStatus]);});
};
// Restore a suspended context when a visitor returns to the page and interacts.
for(const event of ['pointerdown','keydown'])document.addEventListener(event,e=>{
 if(e.isTrusted&&e.target?.id!=='sound'&&audio.enabled)void audio.unlock();
},{capture:true});
document.addEventListener('click',e=>{
 const control=e.target.closest?.('button,a,summary,[role="button"],input[type="checkbox"]');
 if(!control||control.disabled||control.getAttribute('aria-disabled')==='true'||control.matches('#sound,#run,#check,#example,[data-choice]'))return;
 void audio.play('click',{channel:'ui'});
},{capture:true});
document.addEventListener('visibilitychange',()=>{if(document.hidden)audio.stop();});

function validateState(s){if(!s||s.version!==1||!Array.isArray(s.completed)||!s.completed.every(n=>Number.isInteger(n)&&n>=1&&n<=20)||!s.drafts||typeof s.drafts!=='object'||Array.isArray(s.drafts))throw Error('进度文件格式不正确');return {version:1,completed:[...new Set(s.completed)],drafts:Object.fromEntries(Object.entries(s.drafts).filter(([k,v])=>/^([1-9]|1\d|20)$/.test(k)&&typeof v==='string'&&v.length<100000)),quiz:Array.isArray(s.quiz)?s.quiz.filter(n=>Number.isInteger(n)&&n>=1&&n<=20):[]};}
try{const old=localStorage.getItem(KEY);if(old)state=validateState(JSON.parse(old));}catch{}
function save(){try{localStorage.setItem(KEY,JSON.stringify(state));}catch{toast('浏览器未能保存进度，请导出备份。');}}
function toast(s){$('#toast').textContent=t(s);$('#toast').classList.add('show');clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('#toast').classList.remove('show'),3500);}
function download(name,text,type='text/plain'){const u=URL.createObjectURL(new Blob([text],{type}));const a=document.createElement('a');a.href=u;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);}
function totalXP(){return data.levels.filter(l=>state.completed.includes(l.id)).reduce((n,l)=>n+l.xp,0);}
function nextLevel(){return data.levels.find(l=>!state.completed.includes(l.id))?.id||20;}
function island(){return `<svg class="island-art" viewBox="0 0 570 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="芯片岛冒险地图：从新手村跨过森林，到工坊和芯片城"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#d7ddcc"/></pattern></defs><rect width="570" height="360" fill="url(#dots)"/><ellipse cx="294" cy="306" rx="201" ry="24" fill="#dce2cf"/><path d="M88 239L290 133L499 236L298 345Z" fill="#a6ba87" stroke="#547448" stroke-width="2"/><path d="M88 219L290 113L499 216L298 325Z" fill="#e0eacb" stroke="#547448" stroke-width="2"/><path d="M88 219L298 325V345L88 239Z" fill="#b7c99c" stroke="#547448" stroke-width="2"/><path d="M150 222L225 258L300 220L366 252L433 218" fill="none" stroke="#fffef0" stroke-width="14" stroke-linecap="round"/><path d="M150 222L225 258L300 220L366 252L433 218" fill="none" stroke="#91ab71" stroke-width="2" stroke-dasharray="4 7"/><g stroke="#45643c" stroke-width="2"><path d="M120 215V176L147 162L175 176V215L147 230Z" fill="#d2e7ae"/><path d="M116 178L147 145L180 176L147 193Z" fill="#71985c"/><path d="M142 214V197L154 202V220" fill="#7d9d62"/><path d="M240 234V175L261 165L281 175V234L261 245Z" fill="#b0cf99"/><path d="M226 189L261 123L296 189L261 206Z" fill="#729b64"/><path d="M232 166L261 111L290 166L261 180Z" fill="#8fb876"/><path d="M323 215V172L352 156L383 172V215L352 231Z" fill="#e7bf7a"/><path d="M316 172L351 149L390 170L352 190Z" fill="#f8d99e"/><path d="M348 222V196L363 190V215" fill="#8d724d"/><path d="M405 195V121L435 105L465 121V195L435 211Z" fill="#b7acd9"/><path d="M405 121L435 138L465 121" fill="none"/><path d="M435 138V211" fill="none"/><rect x="417" y="142" width="8" height="11" fill="#edf2cf"/><path d="M447 147V160M447 174V187M417 167V180" stroke="#faf8e5" stroke-width="7"/></g><g><rect x="201" y="215" width="25" height="27" rx="7" fill="#35533f"/><rect x="205" y="220" width="17" height="10" rx="3" fill="#c6ed97"/><circle cx="210" cy="224" r="1.5" fill="#35533f"/><circle cx="217" cy="224" r="1.5" fill="#35533f"/><path d="M213 214V207M207 242V248M220 242V248" stroke="#35533f" stroke-width="3"/></g><g font-family="monospace" font-size="10" fill="#476140"><rect x="65" y="87" width="119" height="28" rx="6" fill="#fffef7" stroke="#d1dac4"/><text x="77" y="105">puts "Hello!"</text><path d="M184 101L216 123" stroke="#a6b595" stroke-dasharray="3 4"/><rect x="345" y="47" width="145" height="30" rx="6" fill="#fffef7" stroke="#d1dac4"/><text x="359" y="66">+100 XP · LEVEL UP</text><path d="M419 77V100" stroke="#a6b595" stroke-dasharray="3 4"/><text x="80" y="288" letter-spacing="2" font-size="9">THE CHIP ISLAND / 01</text></g><g fill="#90ad70"><path d="M198 169l4 -12 4 12Z"/><path d="M323 278l4 -12 4 12Z"/><path d="M442 257l4 -12 4 12Z"/></g></svg>`;}
function map(){active=null;const xp=totalXP();$('#view').innerHTML=`<section class="hero"><div><span class="eyebrow">A LITTLE CODE. A BIG ADVENTURE.</span><h1>写下第一行代码，<br>开启你的<em>芯片岛冒险。</em></h1><p>不需要懂编程，也不怕学得慢。和芯芯及四位伙伴一起，<br>从一句「你好」出发，把 Tcl 变成你的超能力。</p><div class="hero-actions"><a class="primary" href="#level/${nextLevel()}">${state.completed.length?'继续我的冒险':'开始冒险'} <span aria-hidden="true">→</span></a><a class="secondary" href="#guide">先看看怎么玩</a></div><div class="hero-meta"><span>20 个小任务</span><span>4 场 Boss 挑战</span><span>0 安装，直接练</span></div></div><div class="hero-art">${island()}</div></section><section class="stats" aria-label="冒险进度"><span class="avatar">t_</span><div><strong>${xp>=2000?'芯片岛探险家':xp>=1000?'技能工匠':xp>=500?'森林行者':'新晋冒险家'}</strong><p>每一次尝试，都是一次前进。</p></div><div class="progress-area"><div class="progress-label"><span>冒险进度</span><span>${state.completed.length} / 20</span></div><div class="progress-track" role="progressbar" aria-label="已通关关卡" aria-valuenow="${state.completed.length}" aria-valuemin="0" aria-valuemax="20"><div class="progress-fill" style="width:${state.completed.length*5}%"></div></div></div><div class="stat-number">${xp} <span>/ 2400 XP</span></div><div class="stat-number">${data.levels.filter(l=>l.boss&&state.completed.includes(l.id)).length} <span>/ 4 徽章</span></div></section>${partyHTML()}<section><div class="section-title"><div><h2>选一片天地，学一种本领。</h2><p>推荐从新手村出发。所有关卡随时开放，按自己的节奏探索。</p></div><span class="pill">YOUR ADVENTURE MAP</span></div><label class="sr-label" for="search">查找知识点</label> <input id="search" class="search" type="search" placeholder="搜索 puts、循环、文件……" autocomplete="off"><div class="search-results" id="search-results" aria-live="polite"></div><div class="worlds">${data.worlds.map((w,i)=>`<article class="world-card" style="--world:${w.color}"><div class="world-top"><span class="world-symbol">${w.icon}</span><span class="world-index">WORLD 0${i+1}</span></div><h3>${w.name}</h3><p>${w.subtitle}</p><div class="level-list">${data.levels.filter(l=>l.world===i).map(l=>`<a class="level-link" href="#level/${l.id}"><span class="level-number">${String(l.id).padStart(2,'0')}</span><span>${esc(l.title.replace(/.*BOSS · /,'').replace('终极 ',''))}</span>${state.completed.includes(l.id)?'<span class="complete-mark" aria-label="已通关">✓</span>':l.boss?'<span class="boss-tag">BOSS</span>':''}</a>`).join('')}</div><div class="card-bottom"><span>${data.levels.filter(l=>l.world===i&&state.completed.includes(l.id)).length} / 5 已完成</span><span>600 XP</span></div></article>`).join('')}</div></section><div class="callouts"><a href="#videos" class="callout"><span class="world-symbol" style="background:#e3e8d5">▶</span><div><strong>卡住了？来放映室看看</strong><p>四段中文字幕演示，代码一步步运行给你看。</p></div><span class="callout-arrow">↗</span></a><a href="#level/20" class="callout"><span class="world-symbol" style="background:#e9ddca">⌁</span><div><strong>终点，是一个能用的小工具</strong><p>亲手完成 VLSI 时序报告分析器。</p></div><span class="callout-arrow">↗</span></a></div>`;
bindParty($('#view'));$('#search').addEventListener('input',e=>{const q=e.target.value.trim().toLowerCase();$('#search-results').innerHTML=q?data.levels.filter(l=>(l.topic+l.title+l.explain.join('')).toLowerCase().includes(q)).map(l=>`<a href="#level/${l.id}">${l.id}. ${esc(l.title)} · ${esc(l.topic)}</a>`).join('')||'<p>没有找到，试试“变量”或“列表”。</p>':'';});}
function lesson(id,snapshot){const l=data.levels.find(x=>x.id===id);if(!l){location.hash='#map';return;}active=l;$('#view').innerHTML=`<div class="breadcrumbs"><a href="#map">← 冒险地图 / ${data.worlds[l.world].name}</a><span>LEVEL ${String(l.id).padStart(2,'0')} / 20</span></div><section class="lesson-heading"><div><span class="eyebrow">${l.boss?'BOSS CHALLENGE':'LEARN · TRY · DISCOVER'}</span><h1>${esc(l.title)}</h1><p>${esc(l.topic)} · 约 ${l.minutes} 分钟</p></div><span class="pill">${state.completed.includes(id)?'✓ 已完成':`首次通关 +${l.xp} XP`}</span></section><details class="storyboard-details"><summary>故事图解 · 可展开查看四幕教学演示</summary><div id="adventure-host"></div></details><div class="lesson-grid"><article class="lesson-reading"><div class="story"><p>${esc(l.story)}</p></div><h2>先认识这项本领</h2>${l.explain.map(p=>`<p>${esc(p)}</p>`).join('')}<div class="diagram" role="img" aria-label="${esc(l.diagram.join(language()==='en'?', then ':'，然后，'))}">${l.diagram.map((s,i)=>`${i?'<span class="diagram-arrow" aria-hidden="true">→</span>':''}<div class="diagram-box">${esc(s)}</div>`).join('')}</div><h2>看一个小例子</h2><pre class="code-block"><code>${esc(l.example)}</code></pre><button class="secondary example-button" id="example">在实验室运行这个例子 →</button><h2>现在，轮到你了</h2><p>${esc(l.task)}</p><div class="expected">目标输出<pre class="code-block">${esc(l.expected)}</pre></div><div class="hint-list">${l.hints.map((h,i)=>`<details><summary>提示 ${i+1} · ${i?'再具体一点':'给我一个方向'}</summary><p>${esc(h)}</p></details>`).join('')}</div><div class="mini-note"><strong>路上的小提醒</strong>${esc(l.pitfall)}</div><section class="quiz"><h3>想一想：${esc(l.quiz)}</h3>${l.choices.map((c,i)=>`<button data-choice="${i}">${String.fromCharCode(65+i)}. ${esc(c)}</button>`).join('')}<div class="quiz-feedback" role="status">${state.quiz.includes(id)?'✓ 你已答对过这道理解题。':''}</div></section><h2>再试一步</h2><p>${esc(l.transfer)}</p><details class="solution-details"><summary>查看参考解法（建议先自己试一试）</summary><pre class="code-block">${esc(l.solution)}</pre><button class="secondary" id="load-solution">载入参考解法</button></details><p><a href="#videos">▶ 看本区域的演示视频</a></p></article><section class="lab" aria-label="Tcl 实验室"><div class="lab-top"><span class="lab-dots"><i></i><i></i><i></i></span><strong>你的 Tcl 实验室</strong><span class="runtime-label">Tcl / WebAssembly</span></div><div class="file-bar"><label for="editor">quest_${String(id).padStart(2,'0')}.tcl</label><span id="editor-mode">挑战代码 · 自动保存</span></div><div class="editor-wrap"><div class="line-numbers" aria-hidden="true"></div><textarea id="editor" class="editor" spellcheck="false" autocapitalize="off" autocorrect="off" aria-label="Tcl 代码编辑器"></textarea></div><div class="lab-controls"><button class="primary lime" id="run">▶ 运行代码</button><button class="primary lime" id="check">提交挑战 ✓</button><button class="secondary" id="reset">恢复起始代码</button><button class="secondary" id="download-code">下载 .tcl</button><button class="secondary" id="stop" hidden>停止</button></div><div class="output-head"><span>OUTPUT / 运行结果</span><span>Ctrl / ⌘ + Enter 运行</span></div><pre id="output" class="output" aria-live="polite">准备好了。改一行代码，然后点「运行代码」。</pre><div id="test-results" class="test-results" aria-live="polite"></div><div id="runtime-host"></div><div class="lab-foot">真实 Tcl 引擎 · 每次独立运行 · 超时自动停止 · 无体力限制</div></section></div><div class="lesson-bottom">${id>1?`<a class="secondary" href="#level/${id-1}">← 上一关</a>`:'<a class="secondary" href="#map">← 回地图</a>'}${id<20?`<a class="secondary" href="#level/${id+1}">探索下一关 →</a>`:'<a class="secondary" href="#guide">查看我的冒险成果 →</a>'}</div>`;
mountAdventure($('#adventure-host'),l,storyboards.find(s=>s.id===id),code=>{setCode(code,'剧情演示代码 · 可修改后运行');$('#editor').scrollIntoView({block:'center'});},sceneAudio);
mountRuntime($('#runtime-host'),l,storyboards.find(s=>s.id===id),snapshot,sceneAudio);
$('#output').textContent=t('准备好了。改一行代码，然后点「运行代码」。');
$('#editor').value=state.drafts[id]??l.starter;lines();$('#editor').addEventListener('input',()=>{state.drafts[id]=$('#editor').value;save();lines();updateAdventure({status:'edited'});editRuntime();});$('#editor').addEventListener('keydown',e=>{if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();execute(false);}if(e.key==='Tab'){e.preventDefault();const t=e.target;const s=t.selectionStart;const end=t.selectionEnd;t.setRangeText('    ',s,end,'end');t.dispatchEvent(new Event('input'));}});
$('#run').onclick=()=>execute(false);$('#check').onclick=()=>execute(true);$('#stop').onclick=()=>stopRun?.();$('#reset').onclick=()=>setCode(l.starter,'挑战代码 · 自动保存');$('#example').onclick=()=>{setCode(l.example,'示例代码 · 先观察结果');execute(false);};$('#load-solution').onclick=()=>setCode(l.solution,'参考解法 · 读懂后试着修改');$('#download-code').onclick=()=>download(`quest_${String(id).padStart(2,'0')}.tcl`,$('#editor').value+'\n');document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{const ok=Number(b.dataset.choice)===l.answer,alreadyCorrect=b.classList.contains('correct');if(ok&&!alreadyCorrect){void audio.play('quiz');celebrations.play('quiz',t('答对了！'),t('理解一小步，冒险更进一步。'));}else if(!ok){celebrations.clear();void audio.play('denied');}else void audio.play('click',{channel:'ui'});b.classList.remove('correct','wrong');b.classList.add(ok?'correct':'wrong');$('.quiz-feedback').textContent=ok?'✓ 答对了！可以回到示例中验证你的理解。':'再想一想，看看上面的概念说明；可以继续尝试。';if(ok&&!state.quiz.includes(id)){state.quiz.push(id);save();}});}
function lines(){const n=$('#editor')?.value.split('\n').length||1;$('.line-numbers').textContent=Array.from({length:n},(_,i)=>i+1).join('\n');}
function setCode(code,mode){editRuntime();updateAdventure({status:'edited'});$('#editor').value=code;$('#editor-mode').textContent=mode;state.drafts[active.id]=code;save();lines();$('#editor').focus();}
let stopRun=null;
function engineError(key){const e=new Error(t(key));e.translationKey=key;return e;}
function evalInWorker(code,checks=[],onEvent=()=>{}){
 return new Promise((resolve,reject)=>{
  let done=false,traceLimit=false,unavailable=false;
  const worker=new Worker(new URL('runner.js?v=1f251ee98b8c',import.meta.url));
  let timer=setTimeout(()=>finish(engineError('引擎加载超过 25 秒。请检查页面是否通过 HTTP 打开，或刷新重试。')),25000);
  function finish(err,value){if(done)return;done=true;clearTimeout(timer);worker.terminate();stopRun=null;err?reject(err):resolve({...value,traceLimit,unavailable});}
  stopRun=()=>finish(engineError('本次运行已停止，代码仍保留。'));
  worker.onerror=e=>finish(Error(e.message||t('Tcl 引擎加载失败')));
  worker.onmessage=e=>{
   const msg=e.data;
   if(msg.type==='ready'){clearTimeout(timer);timer=setTimeout(()=>finish(engineError('运行超过 5 秒，已停止。检查 while / for 的条件是否会结束。')),5000);worker.postMessage({code,checks,trace:true});}
   else if(msg.type==='trace'||msg.type==='stdout')onEvent(msg);
   else if(msg.type==='trace-limit')traceLimit=true;
   else if(msg.type==='trace-unavailable')unavailable=true;
   else if(msg.type==='result')finish(null,msg);
   else if(msg.type==='failure')finish(Error(msg.message));
  };
 });
}
async function execute(check){
 if(busy||!active)return;
 celebrations.clear();void audio.play('run');
 const l=active,generation=viewGeneration;busy=true;
 $('#run').disabled=$('#check').disabled=$('#language').disabled=true;$('#stop').hidden=false;
 $('#output').classList.remove('error');$('#output').textContent=t('正在唤醒 Tcl 引擎……');$('#test-results').textContent='';
 updateAdventure({status:'loading',output:''});startRuntime();const streaming=[];
 try{
  const r=await evalInWorker($('#editor').value,check?l.checks:[],event=>{
   if(generation!==viewGeneration)return;
   if(event.type==='trace')pushRuntime(event.event);
   else{pushRuntime({kind:'stdout',text:event.text});streaming.push(event.text);$('#output').textContent=streaming.join('\n');}
  });
  if(generation!==viewGeneration)return;
  lastExecution={...r,lesson:l.id,check};
  const output=r.output||r.result||t('（执行完成，没有输出）');$('#output').textContent=output;
  if(r.error){
   void audio.play('error');
   $('#output').classList.add('error');$('#output').textContent=(r.output?r.output+'\n\n':'')+t('Tcl 提示：')+r.error+'\n\n'+t(explainError(r.error));
   updateAdventure({status:'error',output:(r.output?r.output+'\n':'')+r.error});finishRuntime({done:true,error:r.error,traceLimit:r.traceLimit,unavailable:r.unavailable});return;
  }
  updateAdventure({status:'run',output});
  if(check){
   const tests=[{label:t('输出符合任务要求'),ok:r.output.replace(/\n+$/,'')===l.expected},...r.tests];
   $('#test-results').innerHTML=tests.map(test=>`<div>${test.ok?'✓':'○'} ${esc(test.label)}${test.error?`: ${esc(test.error)}`:''}</div>`).join('');
   const passed=tests.every(test=>test.ok);
   void audio.play(passed?'success':'error');
   finishRuntime({done:true,validation:passed?'passed':'failed',traceLimit:r.traceLimit,unavailable:r.unavailable});
   updateAdventure({status:passed?'passed':'failed',output});
   if(passed){
    if(!state.completed.includes(l.id)){state.completed.push(l.id);save();afterRuntime(()=>{if(generation===viewGeneration)reward(l);});}
    else afterRuntime(()=>{if(generation===viewGeneration){void audio.play('reward');celebrations.play('mission',t('挑战完成！'),t('全部检查通过！这一关的 XP 已经领取过了。'));toast('全部检查通过！这一关的 XP 已经领取过了。');}});
   }else toast('还差一点。对照目标输出和提示，再试一次。');
  }else{void audio.play('success');finishRuntime({done:true,traceLimit:r.traceLimit,unavailable:r.unavailable});}
 }catch(e){
  if(generation!==viewGeneration)return;
  void audio.play('error');
  lastExecution={lesson:l.id,rawFailure:e.translationKey||e.message};$('#output').classList.add('error');$('#output').textContent=e.message;updateAdventure({status:'error',output:e.message});finishRuntime({done:true,error:e.message});
 }finally{
  busy=false;$('#language').disabled=false;
  if(generation===viewGeneration&&$('#run')){$('#run').disabled=$('#check').disabled=false;$('#stop').hidden=true;}
 }
}
function explainError(s){if(/can't read .*no such variable/.test(s))return '检查变量是否先用 set 定义，名字是否拼写一致。';if(/invalid command name/.test(s))return '检查命令拼写和大小写。EDA 工具扩展命令不一定能在普通 Tcl 中运行。';if(/missing close-brace/.test(s))return '花括号没有配对：检查每一个 { 是否都有对应的 }。';if(/missing close-bracket/.test(s))return '方括号没有配对：检查 [ 和 ]。';if(/wrong # args/.test(s))return '参数数量不对。检查空格、引号和命令的参数顺序。';return '从错误信息里的命令和行号开始检查，或者打开提示，和示例逐行比较。';}
function reward(l){$('#reward-party').innerHTML=portrait('robot','success')+portrait(CAST[l.world+1].kind);nextReward=l.id<20?l.id+1:0;$('#reward-title').textContent=l.boss?'Boss 挑战完成！':'又学会一项本领！';$('#reward-body').textContent=`${l.title} · +${l.xp} XP。你已经走过 ${state.completed.length} / 20 关。`;$('#reward-badge').textContent=l.boss?`✦ 获得徽章：${data.worlds[l.world].badge}`:'一行代码，一小步进步。';$('#reward-next').textContent=l.id===20?'回到冒险地图 →':'继续冒险 →';$('#celebration').showModal();void audio.play('reward');celebrations.play(l.boss?'boss':'mission',t(l.boss?'Boss 挑战完成！':'关卡完成！'),`+${l.xp} XP · ${t('又学会一项本领！')}`);}
$('#reward-next').onclick=()=>{$('#celebration').close();location.hash=nextReward?`#level/${nextReward}`:'#map';};$('#reward-close').onclick=()=>{celebrations.clear();$('#celebration').close();};
const videoTitles=['第一行代码与变量','列表、条件与循环','过程与安全计算','一份报告，一次芯片冒险'];
function videos(){active=null;const suffix=language()==='en'?'-en':'';$('#view').innerHTML=`<section class="section-page"><span class="eyebrow">WATCH · PAUSE · TRY</span><h1>把看懂，变成会做。</h1><p class="intro">四段原创代码演示，配中文画面字幕。随时暂停，回到实验室照着试。<br>视频没有配音；每段都有文字稿，读文字也能完整学习。</p><div class="video-grid">${videoTitles.map((t,i)=>`<article class="video-card"><video controls preload="metadata" playsinline poster="media/demo-${i+1}${suffix}.png"><source src="media/demo-${i+1}${suffix}.mp4" type="video/mp4"><track kind="captions" srclang="${language()==='en'?'en':'zh'}" label="${language()==='en'?'English':'中文'}" src="media/demo-${i+1}${suffix}.vtt" default>浏览器不支持视频，请阅读下方文字稿。</video><div class="video-info"><span class="eyebrow">WORLD 0${i+1} · 约 1 分钟</span><h2>${t}</h2><p>${data.worlds[i].subtitle}，跟着代码、输出和解释走一遍。</p><a href="#level/${i*5+1}">去对应关卡练一练 →</a> · <a href="media/demo-${i+1}${suffix}.txt" target="_blank">阅读文字稿</a> · <a href="media/demo-${i+1}${suffix}.mp4" download>下载视频</a></div></article>`).join('')}</div></section>`;}
function guide(){active=null;$('#view').innerHTML=`<section class="section-page"><span class="eyebrow">EVERYONE STARTS SOMEWHERE</span><h1>不用赶路。这里没有倒计时。</h1><p class="intro">你只需要会使用浏览器。可以自己探索，也可以和朋友、家长或老师一起学。建议每次学一到两关，约 10–30 分钟。</p><div class="guide-cards"><article class="guide-card"><h2>每关怎么玩？</h2><ol><li>读故事和图解，认识一个新概念。</li><li>运行小例子，猜猜修改一行会发生什么。</li><li>点击「恢复起始代码」，完成任务。</li><li>点「提交挑战」，通过检查就获得 XP。</li><li>答一道理解题，试做一个拓展练习。</li></ol><p>答错不会扣分。所有关卡都能自由进入，XP 只在首次通关时领取。</p></article><article class="guide-card"><h2>按自己的经验选择路线</h2><p><strong>第一次接触代码：</strong>从第 1 关起，先照着例子试，再改一处。不认识的英文把它当作工具名字。</p><p><strong>已有编程经验：</strong>先看第 3 关的括号规则，再挑战各区域 Boss。</p><p><strong>VLSI 课程学习：</strong>完成基础后进入第 16–20 关。这里的 EDA 操作是教学模拟，商业软件命令请使用课程工具文档。</p></article><article class="guide-card"><h2>实验室和进度</h2><p>代码区下方的实时剧情窗由实际执行驱动，可以暂停、单步回放或快进。上方的教学分镜可以展开查看。</p><p>顶栏可切换中英文。代码草稿与通关进度共享，原生输出保留原样。</p><p>首次运行下载约 4.4 MB 的本地资源。Tcl 在浏览器 Worker 中执行；每次运行环境独立，5 秒超时。文件操作使用内存文件系统。</p><p>草稿、XP 和徽章保存在当前浏览器，不跨设备同步。使用下面的导出、导入功能转移进度。导入会替换当前进度。</p><p>这是自学记录，不是防作弊成绩系统。</p></article><article class="guide-card"><h2>想在电脑或云端继续？</h2><p>本地安装 Tcl 8.6+ 后运行：</p><pre class="code-block">tclsh lessons/01/starter.tcl\npython3 scripts/check.py 1 lessons/01/starter.tcl</pre><p>仓库提供 Dev Container，可通过 GitHub Codespaces 使用。GitHub 可能按套餐限制或计费；网页实验室本身不需要账户。</p><p><a href="https://github.com/Su3037/tcl-quest" target="_blank" rel="noopener">打开仓库查看安装说明 ↗</a></p></article></div><h2>你的冒险徽章</h2><div class="badge-row">${data.worlds.map((w,i)=>`<div class="badge ${state.completed.includes((i+1)*5)?'earned':''}">${state.completed.includes((i+1)*5)?'✦':'◇'} ${w.badge}</div>`).join('')}</div><div class="guide-tools"><button id="export" class="primary">导出学习进度</button><button id="import" class="secondary">导入学习进度</button><input id="import-file" type="file" accept="application/json,.json" hidden><button id="certificate" class="secondary">导出学习记录</button></div><p class="intro">课程设计参考老师的 <a href="https://sjtu-yongfu-research-grp.github.io/tcl-language/" target="_blank" rel="noopener">Tcl Language Course</a>。这里的故事、关卡、图解与视频为本项目原创；Tcl 引擎采用 Wacl，授权文件见仓库 vendor 目录。</p></section>`;
$('#export').onclick=()=>download('tcl-quest-progress.json',JSON.stringify(state,null,2),'application/json');$('#import').onclick=()=>$('#import-file').click();$('#import-file').onchange=async e=>{try{const f=e.target.files[0];if(!f)return;if(f.size>2000000)throw Error('进度文件过大');const s=validateState(JSON.parse(await f.text()));if(!confirm(t('导入会替换此浏览器当前的草稿和进度。继续导入？')))return;state=s;save();guide();toast('进度已导入。');}catch(err){toast('无法导入：'+err.message);}};$('#certificate').onclick=()=>{
 const en=language()==='en',date=new Date().toLocaleDateString(en?'en-GB':'zh-CN',{timeZone:'Asia/Shanghai'});
 const title=en?'Tcl Quest learning record':'Tcl Quest 学习记录';
 const body=`${title}\n${en?'Date':'日期'}: ${date}\n${en?'Completed':'通关'}: ${state.completed.length}/20\n${en?'Experience':'经验'}: ${totalXP()}/2400 XP\n\n${data.levels.map(l=>`${state.completed.includes(l.id)?'✓':'○'} ${String(l.id).padStart(2,'0')} ${l.title}`).join('\n')}\n\n${en?'A self-study record stored in your browser.':'学习记录仅保存在你的浏览器中，用于自学回顾。'}\n`;
 download(en?'Tcl-Quest-learning-record.txt':'Tcl-Quest-学习记录.txt',body);
};}

function route(preserve=false){celebrations.clear();audio.stop('scene');const snapshot=preserve===true?runtimeSnapshot():null;viewGeneration++;clearAdventure();clearRuntime();if(busy&&stopRun)stopRun();const hash=location.hash||'#map';document.querySelectorAll('[data-nav]').forEach(a=>{if(hash==='#'+a.dataset.nav)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});if(hash.startsWith('#level/'))lesson(Number(hash.split('/')[1]),snapshot);else if(hash==='#videos')videos();else if(hash==='#guide')guide();else map();localize(document.body);window.scrollTo(0,0);}
function refreshLanguage(){setLanguage(language());refreshSound();data=courses[language()];storyboards=stories[language()];setArtTranslator(t);$('#language').textContent=language()==='en'?'中文':'English';$('#language').setAttribute('aria-label',language()==='en'?'Switch to Chinese':'切换为英文');}
$('#language').onclick=()=>{const y=scrollY,editor=$('#editor'),selection=editor?[editor.selectionStart,editor.selectionEnd]:null,open=$('.storyboard-details')?.open;setLanguage(language()==='en'?'zh':'en');refreshLanguage();route(true);if(open&&$('.storyboard-details'))$('.storyboard-details').open=true;if(selection&&$('#editor'))$('#editor').setSelectionRange(...selection);if(lastExecution?.lesson===active?.id){
 const r=lastExecution;
 $('#output').textContent=r.rawFailure?t(r.rawFailure):r.error?(r.output?r.output+'\n\n':'')+t('Tcl 提示：')+r.error+'\n\n'+t(explainError(r.error)):r.output||r.result||t('（执行完成，没有输出）');
 $('#output').classList.toggle('error',!!r.error||!!r.rawFailure);
 if(r.check&&!r.error){const tests=[{label:t('输出符合任务要求'),ok:r.output.replace(/\n+$/,'')===active.expected},...r.tests.map((test,i)=>({...test,label:active.checks[i]?.label||t(test.label)}))];$('#test-results').innerHTML=tests.map(test=>`<div>${test.ok?'✓':'○'} ${esc(test.label)}${test.error?`: ${esc(test.error)}`:''}</div>`).join('');}
 }
 window.scrollTo(0,y);};
try{
 await initLanguage();
 const files=['curriculum.json','curriculum.en.json','adventures.json','adventures.en.json'];
 const loaded=await Promise.all(files.map(async file=>{const r=await fetch(new URL(file,import.meta.url),{cache:'no-cache'});if(!r.ok)throw Error('Could not load '+file);return r.json();}));
 $('#language').disabled=false;courses={zh:loaded[0],en:loaded[1]};stories={zh:loaded[2],en:loaded[3]};refreshLanguage();observeTranslations();route();window.addEventListener('hashchange',()=>route());
}catch(e){$('#view').innerHTML=`<section class="section-page"><h1>${t('课程暂时没加载出来')}</h1><p>${esc(e.message)}. Start the local HTTP server: <code>python3 scripts/serve.py</code>.</p></section>`;}
