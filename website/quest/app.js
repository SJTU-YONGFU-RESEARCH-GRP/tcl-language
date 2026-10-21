import {createCelebration} from './celebrate.js?v=1f251ee98b8c';
import {createSoundPlayer} from './sound.js?v=1f251ee98b8c';
import {initLanguage,language,setLanguage,t,localize,observeTranslations} from './i18n.js?v=1f251ee98b8c';
import {mountRuntime,clearRuntime,runtimeSnapshot,startRuntime,pushRuntime,finishRuntime,editRuntime,afterRuntime} from './live-runtime.js?v=1f251ee98b8c';
import {mountAdventure,clearAdventure,updateAdventure} from './adventure.js?v=1f251ee98b8c';
import {CAST,portrait,partyHTML,bindParty,setArtTranslator} from './adventure-art.js?v=1f251ee98b8c';
const $ = (q) => document.querySelector(q);
const esc = (v) => String(v).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
document.querySelector('.skip, .md-skip')?.addEventListener('click',e=>{e.preventDefault();$('#main')?.focus();$('#main')?.scrollIntoView();});
const KEY='tcl-quest-progress-v1';
let data, storyboards, courses, stories, viewGeneration=0, lastExecution=null, active=null, busy=false, nextReward=1;
let state={version:1,completed:[],drafts:{},quiz:[]};
const celebrations=createCelebration();
const sceneAudio={onAction:cue=>{if(cue)void audio.play(cue,{channel:'scene'});else audio.stop('scene');}};
const SOUND_KEY='tcl-quest-sound-v1';
let audioStatus='off';
const audioMessages={
 en:{
  off:'Sound is off. Enable to preview sounds for controls, scene actions, quizzes and missions.',
  pending:'Sound is waiting for activation. Toggle sound or run code to retry.',
  ready:'Sound is on. Enable to preview sounds for controls, scene actions, quizzes and missions.',
  blocked:'The browser has not allowed sound. Switch it off and on, and check that the tab is not muted.',
  unsupported:'This browser does not support game sounds.'
 },
 zh:{
  off:'音效已关闭。打开开关可试听；点击、动作、答题和通关都有音效。',
  pending:'音效等待启用。点击开关或运行代码可重试。',
  ready:'音效已开启。打开开关可试听；点击、动作、答题和通关都有音效。',
  blocked:'浏览器暂未允许播放音效。请关闭再打开音效，并检查标签页是否静音。',
  unsupported:'此浏览器暂不支持游戏音效。'
 }
};
function getAudioMsg(){
 const isZh = language() === 'zh';
 const dict = isZh ? audioMessages.zh : audioMessages.en;
 return dict[audioStatus] || dict.off;
}
function refreshSound(){
 const btn = $('#sound');
 const isZh = language() === 'zh';
 if (btn) {
   const lbl = $('#sound-label');
   const icon = $('#sound-icon');
   const labelText = isZh ? ('音效 ' + (audio.enabled ? '开' : '关')) : ('Sound ' + (audio.enabled ? 'On' : 'Off'));
   if (lbl) lbl.textContent = labelText;
   else btn.textContent = labelText;
   if (icon) icon.textContent = audio.enabled ? '🔊' : '🔈';
   btn.setAttribute('aria-pressed',String(audio.enabled));
   btn.dataset.audioState=audioStatus;
   btn.title=getAudioMsg();
 }
 const status = $('#sound-status');
 if (status) status.textContent=getAudioMsg();
}
const audio=createSoundPlayer({onStatus:value=>{if(audioStatus!==value){audioStatus=value;refreshSound();}}});
let savedSound=false;try{savedSound=localStorage.getItem(SOUND_KEY)==='on';}catch{}
audio.setEnabled(savedSound,{preview:false});refreshSound();
$('#sound')?.addEventListener('click',()=>{
 const enabled=!audio.enabled;
 const preview=audio.setEnabled(enabled);
 try{localStorage.setItem(SOUND_KEY,enabled?'on':'off');}catch{}
 preview.then(ok=>{
   if(audio.enabled){
     toast(ok ? (language()==='zh'?'音效已开启，正在播放试听音。':'Sound is on. Playing preview tone.') : getAudioMsg());
   }
 });
});
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
function island(){
 const isEn = language() === 'en';
 return `<svg class="island-art" viewBox="0 0 570 360" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${isEn?'Chip Island Adventure Map: from Starter Village to Logic Forest, Workshop, and Chip City':'芯片岛冒险地图：从新手村跨过森林，到工坊和芯片城'}"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r="1" fill="#cbd5e1" opacity="0.6"/></pattern></defs><rect width="570" height="360" fill="url(#dots)"/><ellipse cx="294" cy="306" rx="201" ry="24" fill="#e2e8f0" opacity="0.6"/><path d="M88 239L290 133L499 236L298 345Z" fill="#3b82f6" stroke="#1d4ed8" stroke-width="2"/><path d="M88 219L290 113L499 216L298 325Z" fill="#60a5fa" stroke="#1d4ed8" stroke-width="2"/><path d="M88 219L298 325V345L88 239Z" fill="#2563eb" stroke="#1d4ed8" stroke-width="2"/><path d="M150 222L225 258L300 220L366 252L433 218" fill="none" stroke="#ffffff" stroke-width="14" stroke-linecap="round"/><path d="M150 222L225 258L300 220L366 252L433 218" fill="none" stroke="#38bdf8" stroke-width="2" stroke-dasharray="4 7"/><g stroke="#0f172a" stroke-width="2"><path d="M120 215V176L147 162L175 176V215L147 230Z" fill="#a7f3d0"/><path d="M116 178L147 145L180 176L147 193Z" fill="#10b981"/><path d="M142 214V197L154 202V220" fill="#059669"/><path d="M240 234V175L261 165L281 175V234L261 245Z" fill="#67e8f9"/><path d="M226 189L261 123L296 189L261 206Z" fill="#06b6d4"/><path d="M232 166L261 111L290 166L261 180Z" fill="#0891b2"/><path d="M323 215V172L352 156L383 172V215L352 231Z" fill="#fde68a"/><path d="M316 172L351 149L390 170L352 190Z" fill="#f59e0b"/><path d="M348 222V196L363 190V215" fill="#d97706"/><path d="M405 195V121L435 105L465 121V195L435 211Z" fill="#c4b5fd"/><path d="M405 121L435 138L465 121" fill="none"/><path d="M435 138V211" fill="none"/><rect x="417" y="142" width="8" height="11" fill="#8b5cf6"/><path d="M447 147V160M447 174V187M417 167V180" stroke="#ede9fe" stroke-width="7"/></g><g><rect x="201" y="215" width="25" height="27" rx="7" fill="#0f172a"/><rect x="205" y="220" width="17" height="10" rx="3" fill="#38bdf8"/><circle cx="210" cy="224" r="1.5" fill="#0f172a"/><circle cx="217" cy="224" r="1.5" fill="#0f172a"/><path d="M213 214V207M207 242V248M220 242V248" stroke="#0f172a" stroke-width="3"/></g><g font-family="'JetBrains Mono',monospace" font-size="10" fill="#0f172a"><rect x="65" y="87" width="119" height="28" rx="6" fill="#ffffff" stroke="#cbd5e1"/><text x="77" y="105">puts "Hello!"</text><path d="M184 101L216 123" stroke="#94a3b8" stroke-dasharray="3 4"/><rect x="345" y="47" width="145" height="30" rx="6" fill="#ffffff" stroke="#cbd5e1"/><text x="359" y="66">+100 XP · LEVEL UP</text><path d="M419 77V100" stroke="#94a3b8" stroke-dasharray="3 4"/><text x="80" y="288" letter-spacing="2" font-size="9" fill="#64748b">THE CHIP ISLAND / 01</text></g><g fill="#38bdf8"><path d="M198 169l4 -12 4 12Z"/><path d="M323 278l4 -12 4 12Z"/><path d="M442 257l4 -12 4 12Z"/></g></svg>`;
}
function map(){
 active=null;
 const xp=totalXP();
 const isEn = language() === 'en';
 const heroTitle = isEn
  ? `Write your first line of code,<br>and begin your <em>Chip Island Adventure.</em>`
  : `写下第一行代码，<br>开启你的<em>芯片岛冒险。</em>`;
 const heroDesc = isEn
  ? `No coding experience needed. Take your time with Chip and four friends.<br>Start with a simple "puts" greeting and turn Tcl into your new superpower.`
  : `不需要懂编程，也不怕学得慢。和芯芯及四位伙伴一起，<br>从一句「你好」出发，把 Tcl 变成你的超能力。`;
 const heroBtn = isEn
  ? (state.completed.length ? 'Continue Adventure' : 'Start Adventure')
  : (state.completed.length ? '继续我的冒险' : '开始冒险');
 const heroGuide = isEn ? 'How to Play' : '先看看怎么玩';
 const meta1 = isEn ? '20 missions' : '20 个小任务';
 const meta2 = isEn ? '4 boss battles' : '4 场 Boss 挑战';
 const meta3 = isEn ? 'Zero install, live WASM' : '0 安装，直接练';

 const rank = isEn
  ? (xp>=2000 ? 'Chip Island Explorer' : xp>=1000 ? 'Skill Maker' : xp>=500 ? 'Forest Explorer' : 'New Adventurer')
  : (xp>=2000 ? '芯片岛探险家' : xp>=1000 ? '技能工匠' : xp>=500 ? '森林行者' : '新晋冒险家');
 const rankSub = isEn ? 'Every attempt is a step forward.' : '每一次尝试，都是一次前进。';
 const progressLbl = isEn ? 'Adventure Progress' : '冒险进度';
 const badgesLbl = isEn ? 'badges' : '徽章';

 const sectionTitle = isEn ? 'Choose a world. Learn a new skill.' : '选一片天地，学一种本领。';
 const sectionDesc = isEn
  ? 'Recommended to start from Starter Village. All levels are unlocked to explore at your own pace.'
  : '推荐从新手村出发。所有关卡随时开放，按自己的节奏探索。';
 const searchPlaceholder = isEn ? 'Search puts, loops, files…' : '搜索 puts、循环、文件……';
 const searchAria = isEn ? 'Search topics' : '查找知识点';

 const completedLbl = isEn ? 'completed' : '已完成';
 const callout1Title = isEn ? 'Stuck? Visit Demo Theater' : '卡住了？来放映室看看';
 const callout1Desc = isEn ? 'Four captioned walkthrough demos show code executing step by step.' : '四段中文字幕演示，代码一步步运行给你看。';
 const callout2Title = isEn ? 'The Destination: A Real Tool' : '终点，是一个能用的小工具';
 const callout2Desc = isEn ? 'Build an industrial VLSI static timing analysis (STA) report parser.' : '亲手完成 VLSI 时序报告分析器。';

 $('#view').innerHTML=`<section class="hero"><div><span class="eyebrow">A LITTLE CODE. A BIG ADVENTURE.</span><h1>${heroTitle}</h1><p>${heroDesc}</p><div class="hero-actions"><a class="primary" href="#level/${nextLevel()}">${heroBtn} <span aria-hidden="true">→</span></a><a class="secondary" href="#guide">${heroGuide}</a></div><div class="hero-meta"><span>${meta1}</span><span>${meta2}</span><span>${meta3}</span></div></div><div class="hero-art">${island()}</div></section><section class="stats" aria-label="${progressLbl}"><span class="avatar">t_</span><div><strong>${rank}</strong><p>${rankSub}</p></div><div class="progress-area"><div class="progress-label"><span>${progressLbl}</span><span>${state.completed.length} / 20</span></div><div class="progress-track" role="progressbar" aria-label="${isEn?'Completed levels':'已通关关卡'}" aria-valuenow="${state.completed.length}" aria-valuemin="0" aria-valuemax="20"><div class="progress-fill" style="width:${state.completed.length*5}%"></div></div></div><div class="stat-number">${xp} <span>/ 2400 XP</span></div><div class="stat-number">${data.levels.filter(l=>l.boss&&state.completed.includes(l.id)).length} <span>/ 4 ${badgesLbl}</span></div></section>${partyHTML(isEn)}<section><div class="section-title"><div><h2>${sectionTitle}</h2><p>${sectionDesc}</p></div><span class="pill">YOUR ADVENTURE MAP</span></div><label class="sr-label" for="search">${searchAria}</label> <input id="search" class="search" type="search" placeholder="${searchPlaceholder}" autocomplete="off"><div class="search-results" id="search-results" aria-live="polite"></div><div class="worlds">${data.worlds.map((w,i)=>`<article class="world-card" style="--world:${w.color}"><div class="world-top"><span class="world-symbol">${w.icon}</span><span class="world-index">WORLD 0${i+1}</span></div><h3>${w.name}</h3><p>${w.subtitle}</p><div class="level-list">${data.levels.filter(l=>l.world===i).map(l=>`<a class="level-link" href="#level/${l.id}"><span class="level-number">${String(l.id).padStart(2,'0')}</span><span>${esc(l.title.replace(/.*BOSS · /,'').replace('终极 ',''))}</span>${state.completed.includes(l.id)?`<span class="complete-mark" aria-label="${isEn?'Completed':'已通关'}">✓</span>`:l.boss?'<span class="boss-tag">BOSS</span>':''}</a>`).join('')}</div><div class="card-bottom"><span>${data.levels.filter(l=>l.world===i&&state.completed.includes(l.id)).length} / 5 ${completedLbl}</span><span>600 XP</span></div></article>`).join('')}</div></section><div class="callouts"><a href="#videos" class="callout"><span class="world-symbol" style="color:var(--green)">▶</span><div><strong>${callout1Title}</strong><p>${callout1Desc}</p></div><span class="callout-arrow">↗</span></a><a href="#level/20" class="callout"><span class="world-symbol" style="color:var(--orange)">⌁</span><div><strong>${callout2Title}</strong><p>${callout2Desc}</p></div><span class="callout-arrow">↗</span></a></div>`;
 bindParty($('#view'), isEn);
 $('#search').addEventListener('input',e=>{
  const q=e.target.value.trim().toLowerCase();
  $('#search-results').innerHTML=q?data.levels.filter(l=>(l.topic+l.title+l.explain.join('')).toLowerCase().includes(q)).map(l=>`<a href="#level/${l.id}">${l.id}. ${esc(l.title)} · ${esc(l.topic)}</a>`).join('')||(isEn?'<p>No matching lessons. Try "variable" or "list".</p>':'<p>没有找到，试试“变量”或“列表”。</p>'):'';
 });
}
function lesson(id,snapshot){
 const l=data.levels.find(x=>x.id===id);
 if(!l){location.hash='#map';return;}
 active=l;
 const isEn = language() === 'en';

 const breadcrumb = isEn
  ? `← Adventure Map / ${data.worlds[l.world].name}`
  : `← 冒险地图 / ${data.worlds[l.world].name}`;
 const minutesText = isEn ? `~${l.minutes} mins` : `约 ${l.minutes} 分钟`;
 const completedBadge = state.completed.includes(id)
  ? (isEn ? '✓ Completed' : '✓ 已完成')
  : (isEn ? `First Pass +${l.xp} XP` : `首次通关 +${l.xp} XP`);
 const detailsSummary = isEn
  ? 'Storyboard & Four-Act Live Demo (Expand to View)'
  : '故事图解 · 可展开查看四幕教学演示';
 const h2Concept = isEn ? 'Meet Your New Skill' : '先认识这项本领';
 const h2Example = isEn ? 'Small Example' : '看一个小例子';
 const btnRunExample = isEn ? 'Run Example in Lab →' : '在实验室运行这个例子 →';
 const h2YourTurn = isEn ? 'Your Turn' : '现在，轮到你了';
 const targetOutputLbl = isEn ? 'Target Output' : '目标输出';
 const hintLabel = (i) => isEn
  ? `Hint ${i+1} · ${i ? 'More details' : 'General direction'}`
  : `提示 ${i+1} · ${i ? '再具体一点' : '给我一个方向'}`;
 const pitfallTitle = isEn ? 'Roadside Advice' : '路上的小提醒';
 const quizTitle = isEn ? `Think About It: ${esc(l.quiz)}` : `想一想：${esc(l.quiz)}`;
 const quizAlready = state.quiz.includes(id)
  ? (isEn ? '✓ You have answered this question correctly.' : '✓ 你已答对过这道理解题。')
  : '';
 const h2NextStep = isEn ? 'Take Another Step' : '再试一步';
 const solutionSummary = isEn
  ? 'View Reference Solution (Try on your own first)'
  : '查看参考解法（建议先自己试一试）';
 const btnLoadSolution = isEn ? 'Load Reference Solution' : '载入参考解法';
 const videoLink = isEn ? '▶ Watch demo video for this world' : '▶ 看本区域的演示视频';

 const labTitle = isEn ? 'Your Tcl Lab' : '你的 Tcl 实验室';
 const modeLabel = isEn ? 'Mission Code · Autosaved' : '挑战代码 · 自动保存';
 const btnRun = isEn ? '▶ Run Code' : '▶ 运行代码';
 const btnCheck = isEn ? 'Submit Challenge ✓' : '提交挑战 ✓';
 const btnReset = isEn ? 'Reset Starter Code' : '恢复起始代码';
 const btnDownload = isEn ? 'Download .tcl' : '下载 .tcl';
 const btnStop = isEn ? 'Stop' : '停止';
 const outputHead1 = isEn ? 'OUTPUT / Execution Result' : 'OUTPUT / 运行结果';
 const outputHead2 = isEn ? 'Ctrl / ⌘ + Enter to Run' : 'Ctrl / ⌘ + Enter 运行';
 const outputReady = isEn
  ? 'Ready. Modify a line of code and click "Run Code".'
  : '准备好了。改一行代码，然后点「运行代码」。';
 const labFoot = isEn
  ? 'Real Tcl 8.6 Engine · Isolated Executions · 5s Timeout · Unlimited Retries'
  : '真实 Tcl 引擎 · 每次独立运行 · 超时自动停止 · 无体力限制';

 const prevLink = id > 1
  ? `<a class="secondary" href="#level/${id-1}">${isEn ? '← Previous Level' : '← 上一关'}</a>`
  : `<a class="secondary" href="#map">${isEn ? '← Back to Map' : '← 回地图'}</a>`;
 const nextLink = id < 20
  ? `<a class="secondary" href="#level/${id+1}">${isEn ? 'Explore Next Level →' : '探索下一关 →'}</a>`
  : `<a class="secondary" href="#guide">${isEn ? 'View My Progress →' : '查看我的冒险成果 →'}</a>`;

 $('#view').innerHTML=`<div class="breadcrumbs"><a href="#map">${breadcrumb}</a><span>LEVEL ${String(l.id).padStart(2,'0')} / 20</span></div><section class="lesson-heading"><div><span class="eyebrow">${l.boss?'BOSS CHALLENGE':'LEARN · TRY · DISCOVER'}</span><h1>${esc(l.title)}</h1><p>${esc(l.topic)} · ${minutesText}</p></div><span class="pill">${completedBadge}</span></section><details class="storyboard-details"><summary>${detailsSummary}</summary><div id="adventure-host"></div></details><div class="lesson-grid"><article class="lesson-reading"><div class="story"><p>${esc(l.story)}</p></div><h2>${h2Concept}</h2>${l.explain.map(p=>`<p>${esc(p)}</p>`).join('')}<div class="diagram" role="img" aria-label="${esc(l.diagram.join(isEn?', then ':'，然后，'))}">${l.diagram.map((s,i)=>`${i?'<span class="diagram-arrow" aria-hidden="true">→</span>':''}<div class="diagram-box">${esc(s)}</div>`).join('')}</div><h2>${h2Example}</h2><pre class="code-block"><code>${esc(l.example)}</code></pre><button class="secondary example-button" id="example">${btnRunExample}</button><h2>${h2YourTurn}</h2><p>${esc(l.task)}</p><div class="expected">${targetOutputLbl}<pre class="code-block">${esc(l.expected)}</pre></div><div class="hint-list">${l.hints.map((h,i)=>`<details><summary>${hintLabel(i)}</summary><p>${esc(h)}</p></details>`).join('')}</div><div class="mini-note"><strong>${pitfallTitle}</strong>${esc(l.pitfall)}</div><section class="quiz"><h3>${quizTitle}</h3>${l.choices.map((c,i)=>`<button data-choice="${i}">${String.fromCharCode(65+i)}. ${esc(c)}</button>`).join('')}<div class="quiz-feedback" role="status">${quizAlready}</div></section><h2>${h2NextStep}</h2><p>${esc(l.transfer)}</p><details class="solution-details"><summary>${solutionSummary}</summary><pre class="code-block">${esc(l.solution)}</pre><button class="secondary" id="load-solution">${btnLoadSolution}</button></details><p><a href="#videos">${videoLink}</a></p></article><section class="lab" aria-label="${isEn?'Tcl Lab Sandbox':'Tcl 实验室'}"><div class="lab-top"><span class="lab-dots"><i></i><i></i><i></i></span><strong>${labTitle}</strong><span class="runtime-label">Tcl / WebAssembly</span></div><div class="file-bar"><label for="editor">quest_${String(id).padStart(2,'0')}.tcl</label><span id="editor-mode">${modeLabel}</span></div><div class="editor-wrap"><div class="line-numbers" aria-hidden="true"></div><textarea id="editor" class="editor" spellcheck="false" autocapitalize="off" autocorrect="off" aria-label="${isEn?'Tcl Code Editor':'Tcl 代码编辑器'}"></textarea></div><div class="lab-controls"><button class="primary lime" id="run">${btnRun}</button><button class="primary lime" id="check">${btnCheck}</button><button class="secondary" id="reset">${btnReset}</button><button class="secondary" id="download-code">${btnDownload}</button><button class="secondary" id="stop" hidden>${btnStop}</button></div><div class="output-head"><span>${outputHead1}</span><span>${outputHead2}</span></div><pre id="output" class="output" aria-live="polite">${outputReady}</pre><div id="test-results" class="test-results" aria-live="polite"></div><div id="runtime-host"></div><div class="lab-foot">${labFoot}</div></section></div><div class="lesson-bottom">${prevLink}${nextLink}</div>`;

 mountAdventure($('#adventure-host'),l,storyboards.find(s=>s.id===id),code=>{
  setCode(code, isEn ? 'Storyboard Code · Editable' : '剧情演示代码 · 可修改后运行');
  $('#editor').scrollIntoView({block:'center'});
 },sceneAudio);
 mountRuntime($('#runtime-host'),l,storyboards.find(s=>s.id===id),snapshot,sceneAudio);
 $('#output').textContent=outputReady;
 $('#editor').value=state.drafts[id]??l.starter;
 lines();
 $('#editor').addEventListener('input',()=>{
  state.drafts[id]=$('#editor').value;
  save();
  lines();
  updateAdventure({status:'edited'});
  editRuntime();
 });
 $('#editor').addEventListener('keydown',e=>{
  if(e.key==='Enter'&&(e.ctrlKey||e.metaKey)){e.preventDefault();execute(false);}
  if(e.key==='Tab'){
   e.preventDefault();
   const t=e.target;const s=t.selectionStart;const end=t.selectionEnd;
   t.setRangeText('    ',s,end,'end');
   t.dispatchEvent(new Event('input'));
  }
 });
 $('#run').onclick=()=>execute(false);
 $('#check').onclick=()=>execute(true);
 $('#stop').onclick=()=>stopRun?.();
 $('#reset').onclick=()=>setCode(l.starter, isEn ? 'Mission Code · Autosaved' : '挑战代码 · 自动保存');
 $('#example').onclick=()=>{
  setCode(l.example, isEn ? 'Example Code · Observe Output' : '示例代码 · 先观察结果');
  execute(false);
 };
 $('#load-solution').onclick=()=>setCode(l.solution, isEn ? 'Reference Solution · Read & Modify' : '参考解法 · 读懂后试着修改');
 $('#download-code').onclick=()=>download(`quest_${String(id).padStart(2,'0')}.tcl`,$('#editor').value+'\n');
 document.querySelectorAll('[data-choice]').forEach(b=>b.onclick=()=>{
  const ok=Number(b.dataset.choice)===l.answer,alreadyCorrect=b.classList.contains('correct');
  if(ok&&!alreadyCorrect){
   void audio.play('quiz');
   celebrations.play('quiz',isEn?'Correct!':'答对了！',isEn?'One insight step forward in your adventure.':'理解一小步，冒险更进一步。');
  }else if(!ok){
   celebrations.clear();
   void audio.play('denied');
  }else void audio.play('click',{channel:'ui'});
  b.classList.remove('correct','wrong');
  b.classList.add(ok?'correct':'wrong');
  $('.quiz-feedback').textContent=ok
   ?(isEn?'✓ Correct! Verify your understanding in the example code.':'✓ 答对了！可以回到示例中验证你的理解。')
   :(isEn?'Think again. Re-read the concept explanation above and try again.':'再想一想，看看上面的概念说明；可以继续尝试。');
  if(ok&&!state.quiz.includes(id)){state.quiz.push(id);save();}
 });
}
function lines(){const n=$('#editor')?.value.split('\n').length||1;$('.line-numbers').textContent=Array.from({length:n},(_,i)=>i+1).join('\n');}
function setCode(code,mode){editRuntime();updateAdventure({status:'edited'});$('#editor').value=code;$('#editor-mode').textContent=mode;state.drafts[active.id]=code;save();lines();$('#editor').focus();}
let stopRun=null;
function engineError(key){const e=new Error(t(key));e.translationKey=key;return e;}
function evalInWorker(code,checks=[],onEvent=()=>{}){
 return new Promise((resolve,reject)=>{
  let done=false,traceLimit=false,unavailable=false;
  const isEn = language() === 'en';
  const worker=new Worker(new URL('runner.js?v=1f251ee98b8c',import.meta.url));
  let timer=setTimeout(()=>finish(engineError(isEn?'Tcl engine load timeout (25s). Check HTTP server or refresh.':'引擎加载超过 25 秒。请检查页面是否通过 HTTP 打开，或刷新重试。')),25000);
  function finish(err,value){if(done)return;done=true;clearTimeout(timer);worker.terminate();stopRun=null;err?reject(err):resolve({...value,traceLimit,unavailable});}
  stopRun=()=>finish(engineError(isEn?'Execution stopped. Code is preserved.':'本次运行已停止，代码仍保留。'));
  worker.onerror=e=>finish(Error(e.message||(isEn?'Tcl engine failed to load':'Tcl 引擎加载失败')));
  worker.onmessage=e=>{
   const msg=e.data;
   if(msg.type==='ready'){
    clearTimeout(timer);
    timer=setTimeout(()=>finish(engineError(isEn?'Execution exceeded 5s limit. Check while/for termination conditions.':'运行超过 5 秒，已停止。检查 while / for 的条件是否会结束。')),5000);
    worker.postMessage({code,checks,trace:true});
   }
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
 const isEn = language() === 'en';
 $('#run').disabled=$('#check').disabled=$('#language').disabled=true;$('#stop').hidden=false;
 $('#output').classList.remove('error');$('#output').textContent=isEn?'Waking up Tcl engine…':'正在唤醒 Tcl 引擎……';$('#test-results').textContent='';
 updateAdventure({status:'loading',output:''});startRuntime();const streaming=[];
 try{
  const r=await evalInWorker($('#editor').value,check?l.checks:[],event=>{
   if(generation!==viewGeneration)return;
   if(event.type==='trace')pushRuntime(event.event);
   else{pushRuntime({kind:'stdout',text:event.text});streaming.push(event.text);$('#output').textContent=streaming.join('\n');}
  });
  if(generation!==viewGeneration)return;
  lastExecution={...r,lesson:l.id,check};
  const output=r.output||r.result||(isEn?'(Execution completed with no output)':'（执行完成，没有输出）');
  $('#output').textContent=output;
  if(r.error){
   void audio.play('error');
   $('#output').classList.add('error');
   $('#output').textContent=(r.output?r.output+'\n\n':'')+(isEn?'Tcl Error: ':'Tcl 提示：')+r.error+'\n\n'+explainError(r.error, isEn);
   updateAdventure({status:'error',output:(r.output?r.output+'\n':'')+r.error});
   finishRuntime({done:true,error:r.error,traceLimit:r.traceLimit,unavailable:r.unavailable});
   return;
  }
  updateAdventure({status:'run',output});
  if(check){
   const defaultLabel = isEn ? 'Output matches mission requirements' : '输出符合任务要求';
   const tests=[{label:defaultLabel,ok:r.output.replace(/\n+$/,'')===l.expected},...r.tests];
   $('#test-results').innerHTML=tests.map(test=>`<div>${test.ok?'✓':'○'} ${esc(test.label)}${test.error?`: ${esc(test.error)}`:''}</div>`).join('');
   const passed=tests.every(test=>test.ok);
   void audio.play(passed?'success':'error');
   finishRuntime({done:true,validation:passed?'passed':'failed',traceLimit:r.traceLimit,unavailable:r.unavailable});
   updateAdventure({status:passed?'passed':'failed',output});
   if(passed){
    if(!state.completed.includes(l.id)){
     state.completed.push(l.id);save();
     afterRuntime(()=>{if(generation===viewGeneration)reward(l);});
    } else {
     afterRuntime(()=>{
      if(generation===viewGeneration){
       void audio.play('reward');
       const msgTitle = isEn ? 'Challenge Completed!' : '挑战完成！';
       const msgBody = isEn ? 'All checks passed! XP for this level was already collected.' : '全部检查通过！这一关的 XP 已经领取过了。';
       celebrations.play('mission',msgTitle,msgBody);
       toast(msgBody);
      }
     });
    }
   } else {
    toast(isEn ? 'Almost there. Compare with the target output and hints, then try again.' : '还差一点。对照目标输出和提示，再试一次。');
   }
  } else {
   void audio.play('success');
   finishRuntime({done:true,traceLimit:r.traceLimit,unavailable:r.unavailable});
  }
 }catch(e){
  if(generation!==viewGeneration)return;
  void audio.play('error');
  lastExecution={lesson:l.id,rawFailure:e.translationKey||e.message};
  $('#output').classList.add('error');$('#output').textContent=e.message;
  updateAdventure({status:'error',output:e.message});
  finishRuntime({done:true,error:e.message});
 }finally{
  busy=false;$('#language').disabled=false;
  if(generation===viewGeneration&&$('#run')){$('#run').disabled=$('#check').disabled=false;$('#stop').hidden=true;}
 }
}
function explainError(s, isEn = (language()==='en')){
 if(isEn){
  if(/can't read .*no such variable/.test(s))return 'Check if the variable was defined with "set" first, and names match exactly.';
  if(/invalid command name/.test(s))return 'Check command spelling and capitalization. EDA commands might not exist in standard Tcl.';
  if(/missing close-brace/.test(s))return 'Unmatched curly braces: check that every { has a matching }.';
  if(/missing close-bracket/.test(s))return 'Unmatched square brackets: check [ and ].';
  if(/wrong # args/.test(s))return 'Wrong number of arguments. Check spaces, quotes, and command argument order.';
  return 'Start inspecting from the command and line number in the error message, or compare line-by-line with the example.';
 }
 if(/can't read .*no such variable/.test(s))return '检查变量是否先用 set 定义，名字是否拼写一致。';
 if(/invalid command name/.test(s))return '检查命令拼写和大小写。EDA 工具扩展命令不一定能在普通 Tcl 中运行。';
 if(/missing close-brace/.test(s))return '花括号没有配对：检查每一个 { 是否都有对应的 }。';
 if(/missing close-bracket/.test(s))return '方括号没有配对：检查 [ 和 ]。';
 if(/wrong # args/.test(s))return '参数数量不对。检查空格、引号和命令的参数顺序。';
 return '从错误信息里的命令和行号开始检查，或者打开提示，和示例逐行比较。';
}
function reward(l){
 const isEn = language() === 'en';
 $('#reward-party').innerHTML=portrait('robot','success')+portrait(CAST[l.world+1].kind);
 nextReward=l.id<20?l.id+1:0;
 $('#reward-title').textContent=l.boss
  ?(isEn?'Boss Challenge Defeated!':'Boss 挑战完成！')
  :(isEn?'New Skill Mastered!':'又学会一项本领！');
 $('#reward-body').textContent=isEn
  ?`${l.title} · +${l.xp} XP. You have completed ${state.completed.length} / 20 levels.`
  :`${l.title} · +${l.xp} XP。你已经走过 ${state.completed.length} / 20 关。`;
 $('#reward-badge').textContent=l.boss
  ?(isEn?`✦ Badge Earned: ${data.worlds[l.world].badge}`:`✦ 获得徽章：${data.worlds[l.world].badge}`)
  :(isEn?'One line of code. One step forward.':'一行代码，一小步进步。');
 $('#reward-next').textContent=isEn
  ?(l.id===20?'Return to Adventure Map →':'Continue Adventure →')
  :(l.id===20?'回到冒险地图 →':'继续冒险 →');
 const closeBtn = $('#reward-close');
 if (closeBtn) closeBtn.textContent = isEn ? 'Stay on this Level' : '留在这一关';
 $('#celebration').showModal();
 void audio.play('reward');
 celebrations.play(l.boss?'boss':'mission',
  isEn ? (l.boss ? 'Boss Defeated!' : 'Mission Complete!') : (l.boss ? 'Boss 挑战完成！' : '关卡完成！'),
  `+${l.xp} XP · ${isEn ? 'New Skill Mastered!' : '又学会一项本领！'}`
 );
}
$('#reward-next').onclick=()=>{$('#celebration').close();location.hash=nextReward?`#level/${nextReward}`:'#map';};
$('#reward-close').onclick=()=>{celebrations.clear();$('#celebration').close();};

const videoTitlesEn=['First Code & Variables','Lists, Conditions & Loops','Procedures & Safe Math','One Report, One Chip Adventure'];
const videoTitlesZh=['第一行代码与变量','列表、条件与循环','过程与安全计算','一份报告，一次芯片冒险'];
function videos(){
 active=null;
 const isEn = language() === 'en';
 const suffix=isEn?'-en':'';
 const titles = isEn ? videoTitlesEn : videoTitlesZh;
 const heading = isEn ? 'Turn Understanding into Action.' : '把看懂，变成会做。';
 const intro = isEn
  ? 'Four walkthrough demos with video captions. Pause anytime and experiment in the lab.<br>Videos are silent with synchronized text transcripts for accessible learning.'
  : '四段原创代码演示，配中文画面字幕。随时暂停，回到实验室照着试。<br>视频没有配音；每段都有文字稿，读文字也能完整学习。';
 const fallback = isEn
  ? 'Browser does not support video playback. Please read the transcript below.'
  : '浏览器不支持视频，请阅读下方文字稿。';
 const practiceLink = isEn ? 'Practice in Lesson →' : '去对应关卡练一练 →';
 const transcriptLink = isEn ? 'Read Transcript' : '阅读文字稿';
 const downloadLink = isEn ? 'Download Video' : '下载视频';

 $('#view').innerHTML=`<section class="section-page"><span class="eyebrow">WATCH · PAUSE · TRY</span><h1>${heading}</h1><p class="intro">${intro}</p><div class="video-grid">${titles.map((t,i)=>`<article class="video-card"><video controls preload="metadata" playsinline poster="media/demo-${i+1}${suffix}.png"><source src="media/demo-${i+1}${suffix}.mp4" type="video/mp4"><track kind="captions" srclang="${isEn?'en':'zh'}" label="${isEn?'English':'中文'}" src="media/demo-${i+1}${suffix}.vtt" default>${fallback}</video><div class="video-info"><span class="eyebrow">WORLD 0${i+1} · ${isEn?'~1 min':'约 1 分钟'}</span><h2>${t}</h2><p>${data.worlds[i].subtitle}</p><a href="#level/${i*5+1}">${practiceLink}</a> · <a href="media/demo-${i+1}${suffix}.txt" target="_blank">${transcriptLink}</a> · <a href="media/demo-${i+1}${suffix}.mp4" download>${downloadLink}</a></div></article>`).join('')}</div></section>`;
}
function guide(){
 active=null;
 const isEn = language() === 'en';
 const heading = isEn ? 'No rush. There is no countdown timer.' : '不用赶路。这里没有倒计时。';
 const intro = isEn
  ? 'All you need is a browser. Learn on your own or explore with friends, parents, or mentors. We recommend 1–2 levels per session (~10–30 minutes).'
  : '你只需要会使用浏览器。可以自己探索，也可以和朋友、家长或老师一起学。建议每次学一到两关，约 10–30 分钟。';
 
 const card1Title = isEn ? 'How to Play Each Level' : '每关怎么玩？';
 const card1Steps = isEn ? [
  'Read the story and visual diagram to understand a new concept.',
  'Run the small example and guess what changing a line does.',
  'Click "Reset Starter Code" and fulfill the task requirements.',
  'Click "Submit Challenge" — pass the tests to earn XP.',
  'Answer the quick quiz and try the stretch exercise.'
 ] : [
  '读故事和图解，认识一个新概念。',
  '运行小例子，猜猜修改一行会发生什么。',
  '点击「恢复起始代码」，完成任务。',
  '点「提交挑战」，通过检查就获得 XP。',
  '答一道理解题，试做一个拓展练习。'
 ];
 const card1Foot = isEn
  ? 'Wrong answers never penalize your score. All levels are freely accessible; XP is awarded on your first completion.'
  : '答错不会扣分。所有关卡都能自由进入，XP 只在首次通关时领取。';

 const card2Title = isEn ? 'Choose a Path Based on Your Experience' : '按自己的经验选择路线';
 const card2Content = isEn ? `
  <p><strong>First time coding:</strong> Start from Level 1. Try the examples first, then modify one piece. Treat unfamiliar English words as tool names.</p>
  <p><strong>Prior programming background:</strong> Review Level 3 quoting and substitution rules, then challenge the world Bosses directly.</p>
  <p><strong>VLSI & EDA students:</strong> Master the basics and jump to Levels 16–20. EDA operations here are teaching simulations; for commercial software commands, refer to the lab documentation.</p>
 ` : `
  <p><strong>第一次接触代码：</strong>从第 1 关起，先照着例子试，再改一处。不认识的英文把它当作工具名字。</p>
  <p><strong>已有编程经验：</strong>先看第 3 关的括号规则，再挑战各区域 Boss。</p>
  <p><strong>VLSI 课程学习：</strong>完成基础后进入第 16–20 关。这里的 EDA 操作是教学模拟，商业软件命令请使用课程工具文档。</p>
 `;

 const card3Title = isEn ? 'Lab Environment & Saving Progress' : '实验室和进度';
 const card3Content = isEn ? `
  <p>The execution-driven animation window beneath the editor can be paused, stepped, or fast-forwarded. The storyboard above expands for multi-act demonstrations.</p>
  <p>Toggle language from the subnav strip. Draft code and level completions are synchronized locally; native engine output remains unmodified.</p>
  <p>Initial run downloads ~4.4 MB local WebAssembly assets. Tcl executes inside an isolated Web Worker with a 5-second timeout and memory-based virtual file system.</p>
  <p>Drafts, XP, and badges are stored in your current browser without cross-device tracking. Use Export and Import below to transfer progress.</p>
  <p>This is a personal learning log, not an anti-cheat examination system.</p>
 ` : `
  <p>代码区下方的实时剧情窗由实际执行驱动，可以暂停、单步回放或快进。上方的教学分镜可以展开查看。</p>
  <p>顶栏可切换中英文。代码草稿与通关进度共享，原生输出保留原样。</p>
  <p>首次运行下载约 4.4 MB 的本地资源。Tcl 在浏览器 Worker 中执行；每次运行环境独立，5 秒超时。文件操作使用内存文件系统。</p>
  <p>草稿、XP 和徽章保存在当前浏览器，不跨设备同步。使用下面的导出、导入功能转移进度。导入会替换当前进度。</p>
  <p>这是自学记录，不是防作弊成绩系统。</p>
 `;

 const card4Title = isEn ? 'Continue Locally or in the Cloud' : '想在电脑或云端继续？';
 const card4Content = isEn ? `
  <p>Install Tcl 8.6+ locally and run:</p>
  <pre class="code-block">tclsh lessons/01/starter.tcl\npython3 scripts/check.py 1 lessons/01/starter.tcl</pre>
  <p>The repository provides a full Dev Container compatible with GitHub Codespaces. The web lab itself requires zero account or sign-in.</p>
  <p><a href="https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language" target="_blank" rel="noopener">Open Official GitHub Repository ↗</a></p>
 ` : `
  <p>本地安装 Tcl 8.6+ 后运行：</p>
  <pre class="code-block">tclsh lessons/01/starter.tcl\npython3 scripts/check.py 1 lessons/01/starter.tcl</pre>
  <p>仓库提供 Dev Container，可通过 GitHub Codespaces 使用。GitHub 可能按套餐限制或计费；网页实验室本身不需要账户。</p>
  <p><a href="https://github.com/SJTU-YONGFU-RESEARCH-GRP/tcl-language" target="_blank" rel="noopener">打开官方仓库 ↗</a></p>
 `;

 const badgesHeading = isEn ? 'Your Adventure Badges' : '你的冒险徽章';
 const btnExport = isEn ? 'Export Learning Progress' : '导出学习进度';
 const btnImport = isEn ? 'Import Learning Progress' : '导入学习进度';
 const btnCert = isEn ? 'Export Study Transcript' : '导出学习记录';
 const footCredits = isEn
  ? 'Curriculum aligned with the <a href="https://sjtu-yongfu-research-grp.github.io/tcl-language/" target="_blank" rel="noopener">Tcl for VLSI Automation Lab</a> systematic reference courses. Execution powered by the native WebAssembly Tcl 8.6 engine.'
  : '课程设计参考 <a href="https://sjtu-yongfu-research-grp.github.io/tcl-language/" target="_blank" rel="noopener">Tcl 统一课程体系</a>。本闯关沙箱与 40 节系统课程无缝对接；Tcl 引擎采用 Wacl WebAssembly 原生运行时。';

 $('#view').innerHTML=`<section class="section-page"><span class="eyebrow">EVERYONE STARTS SOMEWHERE</span><h1>${heading}</h1><p class="intro">${intro}</p><div class="guide-cards"><article class="guide-card"><h2>${card1Title}</h2><ol>${card1Steps.map(s=>`<li>${s}</li>`).join('')}</ol><p>${card1Foot}</p></article><article class="guide-card"><h2>${card2Title}</h2>${card2Content}</article><article class="guide-card"><h2>${card3Title}</h2>${card3Content}</article><article class="guide-card"><h2>${card4Title}</h2>${card4Content}</article></div><h2>${badgesHeading}</h2><div class="badge-row">${data.worlds.map((w,i)=>`<div class="badge ${state.completed.includes((i+1)*5)?'earned':''}">${state.completed.includes((i+1)*5)?'✦':'◇'} ${w.badge}</div>`).join('')}</div><div class="guide-tools"><button id="export" class="primary">${btnExport}</button><button id="import" class="secondary">${btnImport}</button><input id="import-file" type="file" accept="application/json,.json" hidden><button id="certificate" class="secondary">${btnCert}</button></div><p class="intro">${footCredits}</p></section>`;

 $('#export').onclick=()=>download('tcl-quest-progress.json',JSON.stringify(state,null,2),'application/json');
 $('#import').onclick=()=>$('#import-file').click();
 $('#import-file').onchange=async e=>{
  try{
   const f=e.target.files[0];
   if(!f)return;
   if(f.size>2000000)throw Error(isEn?'File too large (>2MB)':'进度文件过大');
   const s=validateState(JSON.parse(await f.text()));
   const confirmMsg = isEn
    ? 'Importing will replace your current browser drafts and progress. Continue?'
    : '导入会替换此浏览器当前的草稿和进度。继续导入？';
   if(!confirm(confirmMsg))return;
   state=s;save();guide();
   toast(isEn?'Progress successfully imported.':'进度已导入。');
  }catch(err){toast((isEn?'Import failed: ':'无法导入：')+err.message);}
 };
 $('#certificate').onclick=()=>{
  const date=new Date().toLocaleDateString(isEn?'en-GB':'zh-CN',{timeZone:'Asia/Shanghai'});
  const title=isEn?'Tcl Quest Learning Transcript':'Tcl Quest 学习记录';
  const body=`${title}\n${isEn?'Date':'日期'}: ${date}\n${isEn?'Completed':'通关'}: ${state.completed.length}/20\n${isEn?'Experience':'经验'}: ${totalXP()}/2400 XP\n\n${data.levels.map(l=>`${state.completed.includes(l.id)?'✓':'○'} ${String(l.id).padStart(2,'0')} ${l.title}`).join('\n')}\n\n${isEn?'A self-study record stored locally in your browser.':'学习记录仅保存在你的浏览器中，用于自学回顾。'}\n`;
  download(isEn?'Tcl-Quest-learning-record.txt':'Tcl-Quest-学习记录.txt',body);
 };
}

function route(preserve=false){
 celebrations.clear();audio.stop('scene');const snapshot=preserve===true?runtimeSnapshot():null;viewGeneration++;clearAdventure();clearRuntime();if(busy&&stopRun)stopRun();const hash=location.hash||'#map';
 document.querySelectorAll('[data-nav]').forEach(a=>{
  const targetNav = '#' + a.dataset.nav;
  if(hash===targetNav || (a.dataset.nav==='map' && hash.startsWith('#level/'))){
   a.setAttribute('aria-current','page');
   a.classList.add('active');
  } else {
   a.removeAttribute('aria-current');
   a.classList.remove('active');
  }
 });
 if(hash.startsWith('#level/'))lesson(Number(hash.split('/')[1]),snapshot);else if(hash==='#videos')videos();else if(hash==='#guide')guide();else map();localize(document.body);window.scrollTo(0,0);
}

function refreshLanguage(){
 setLanguage(language());refreshSound();data=courses[language()];storyboards=stories[language()];setArtTranslator(t);
 const langText = language()==='en'?'简体中文':'English';
 const langLbl = $('#language-label');
 if (langLbl) langLbl.textContent = langText;
 else if ($('#language')) $('#language').textContent = langText;
 $('#language')?.setAttribute('aria-label',language()==='en'?'Switch to Chinese':'切换为英文');
}

function switchLanguage(targetLang){
 const y=scrollY,editor=$('#editor'),selection=editor?[editor.selectionStart,editor.selectionEnd]:null,open=$('.storyboard-details')?.open;
 if(targetLang && targetLang !== language()){
  setLanguage(targetLang);
 } else {
  setLanguage(language()==='en'?'zh':'en');
 }
 refreshLanguage();
 route(true);
 if(open&&$('.storyboard-details'))$('.storyboard-details').open=true;
 if(selection&&$('#editor'))$('#editor').setSelectionRange(...selection);
 if(lastExecution?.lesson===active?.id){
  const r=lastExecution;
  const isEn = language() === 'en';
  $('#output').textContent=r.rawFailure?t(r.rawFailure):r.error?(r.output?r.output+'\n\n':'')+(isEn?'Tcl Error: ':'Tcl 提示：')+r.error+'\n\n'+explainError(r.error, isEn):r.output||r.result||(isEn?'(Execution completed with no output)':'（执行完成，没有输出）');
  $('#output').classList.toggle('error',!!r.error||!!r.rawFailure);
  if(r.check&&!r.error){
   const defaultLabel = isEn ? 'Output matches mission requirements' : '输出符合任务要求';
   const tests=[{label:defaultLabel,ok:r.output.replace(/\n+$/,'')===active.expected},...r.tests.map((test,i)=>({...test,label:active.checks[i]?.label||t(test.label)}))];
   $('#test-results').innerHTML=tests.map(test=>`<div>${test.ok?'✓':'○'} ${esc(test.label)}${test.error?`: ${esc(test.error)}`:''}</div>`).join('');
  }
 }
 window.scrollTo(0,y);
}

$('#language')?.addEventListener('click', () => switchLanguage());
$('#opt-lang-en')?.addEventListener('click', (e) => { e.preventDefault(); switchLanguage('en'); });
$('#opt-lang-zh')?.addEventListener('click', (e) => { e.preventDefault(); switchLanguage('zh'); });
$('#header-search-btn')?.addEventListener('click', (e) => {
  e.preventDefault();
  if (location.hash !== '#map' && location.hash !== '') {
    location.hash = '#map';
  }
  setTimeout(() => {
    const s = $('#search');
    if (s) {
      s.focus();
      s.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, 120);
});

function applyTheme(theme){
 const isDark = theme === 'dark' || theme === 'slate';
 const targetScheme = isDark ? 'slate' : 'default';
 const targetAccent = isDark ? 'cyan' : 'blue';

 document.body.setAttribute('data-md-color-scheme', targetScheme);
 document.body.setAttribute('data-md-color-primary', 'indigo');
 document.body.setAttribute('data-md-color-accent', targetAccent);
 document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');

 const radio0 = $('#__palette_0');
 const radio1 = $('#__palette_1');
 if (radio0 && radio1) {
  radio0.checked = !isDark;
  radio1.checked = isDark;
 }

 const lblToDark = $('#palette-label-to-dark');
 const lblToLight = $('#palette-label-to-light');
 if (lblToDark && lblToLight) {
  lblToDark.hidden = isDark;
  lblToLight.hidden = !isDark;
 }

 const paletteObj = {
  index: isDark ? 1 : 0,
  color: { scheme: targetScheme, primary: 'indigo', accent: targetAccent }
 };
 try {
  localStorage.setItem('__palette', JSON.stringify(paletteObj));
  for (let i = 0; i < localStorage.length; i++) {
   let k = localStorage.key(i);
   if (k && k.endsWith('.__palette')) {
    localStorage.setItem(k, JSON.stringify(paletteObj));
   }
  }
 } catch(e) {}
}

window.addEventListener('message', e => {
 if (e.data?.type === 'set-theme' && e.data.scheme) {
  applyTheme(e.data.scheme);
 }
});

$('#palette-label-to-dark')?.addEventListener('click', e => {
 e.preventDefault();
 applyTheme('slate');
});
$('#palette-label-to-light')?.addEventListener('click', e => {
 e.preventDefault();
 applyTheme('default');
});
$('#__palette_0')?.addEventListener('change', () => applyTheme('default'));
$('#__palette_1')?.addEventListener('change', () => applyTheme('slate'));

try {
 if (window.parent && window.parent !== window && window.parent.document?.body) {
  const s = window.parent.document.body.getAttribute('data-md-color-scheme');
  if (s) applyTheme(s);
 } else {
  let p = null;
  for (let i = 0; i < localStorage.length; i++) {
   let k = localStorage.key(i);
   if (k && (k === '__palette' || k.endsWith('.__palette'))) {
    p = localStorage.getItem(k);
    break;
   }
  }
  if (p) {
   const data = JSON.parse(p);
   const scheme = data?.color?.scheme || (data.index === 1 ? 'slate' : 'default');
   applyTheme(scheme);
  } else if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) {
   applyTheme('slate');
  }
 }
} catch(e) {}
try{
 await initLanguage();
 const files=['curriculum.json','curriculum.en.json','adventures.json','adventures.en.json'];
 const loaded=await Promise.all(files.map(async file=>{const r=await fetch(new URL(file,import.meta.url),{cache:'no-cache'});if(!r.ok)throw Error('Could not load '+file);return r.json();}));
 $('#language').disabled=false;courses={zh:loaded[0],en:loaded[1]};stories={zh:loaded[2],en:loaded[3]};refreshLanguage();observeTranslations();route();window.addEventListener('hashchange',()=>route());
}catch(e){$('#view').innerHTML=`<section class="section-page"><h1>${t('课程暂时没加载出来')}</h1><p>${esc(e.message)}. Start the local HTTP server: <code>python3 scripts/serve.py</code>.</p></section>`;}
