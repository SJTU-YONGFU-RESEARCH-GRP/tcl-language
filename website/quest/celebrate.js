// A single short-lived overlay; it never captures clicks or changes progress.
export function createCelebration(){
 let layer=null,timer=null;
 function clear(){clearTimeout(timer);timer=null;layer?.remove();layer=null;}
 function play(kind,title,subtitle=''){
  clear();if(document.hidden)return;
  let motion=!matchMedia('(prefers-reduced-motion: reduce)').matches;
  try{motion=motion&&localStorage.getItem('tcl-quest-motion')!=='off';}catch{}
  layer=document.createElement('div');layer.className=`quest-fest quest-fest-${kind} ${motion?'':'quest-fest-still'}`;
  layer.setAttribute('aria-hidden','true');
  // A manual popover renders above the completion dialog, without stealing focus.
  const topLayer=typeof layer.showPopover==='function';
  if(topLayer)layer.setAttribute('popover','manual');
  const particles=document.createElement('div');particles.className='quest-confetti';
  if(motion)for(let i=0;i<(kind==='quiz'?38:76);i++){
   const p=document.createElement('i');const x=5+Math.random()*90;
   p.style.cssText=`--x:${x}vw;--dx:${(Math.random()-.5)*34}vw;--delay:${Math.random()*.28}s;--spin:${Math.random()*900-450}deg;--color:${['#d9ac52','#79a777','#81b5b3','#d39a86','#aaa0c9'][i%5]};--fall:${1.25+Math.random()*.75}s`;
   if(i%3===0)p.className='quest-confetti-star';particles.append(p);
  }
  const banner=document.createElement('div');banner.className='quest-fest-banner';
  const emblem=document.createElement('span');emblem.className='quest-fest-emblem';emblem.textContent=kind==='quiz'?'✓':'✦';
  const heading=document.createElement('strong');heading.textContent=title;
  const caption=document.createElement('span');caption.textContent=subtitle;
  banner.append(emblem,heading,caption);layer.append(particles,banner);
  (topLayer?document.body:document.querySelector('dialog[open]')||document.body).append(layer);
  if(topLayer)layer.showPopover();
  timer=setTimeout(clear,motion?(kind==='quiz'?1900:2900):1400);
 }
 document.addEventListener('visibilitychange',()=>{if(document.hidden)clear();});
 return {play,clear};
}
