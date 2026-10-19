// Called when a scene is displayed, not when the Worker first queues its event.
const changed=(a,b,key)=>JSON.stringify(a[key])!==JSON.stringify(b[key]);
export function runtimeActionSound(id,before,after,event,oldStep,newStep){
 const k=event.kind,a=event.args||[],diff=key=>changed(before,after,key);
 if(k!=='stdout'&&event.phase==='enter')return null;
 if(k!=='stdout'&&event.kind!=='object-deleted'&&event.code!==0&&event.code!==2)return null;
 switch(id){
  case 1:return k==='stdout'?'speak':null;
  case 2:return diff('coins')&&after.coins!=='?'?'coin':diff('name')?'item':null;
  case 3:return k==='stdout'&&newStep>oldStep?'door':diff('upper')?'magic':null;
  case 4:return diff('energy')?'power':null;
  case 5:return k==='stdout'&&newStep>oldStep?'signal':diff('energy')?'power':null;
  case 6:return (diff('enter')||(oldStep<2&&newStep>=2))?(after.enter?'door':'denied'):null;
  case 7:return k==='lindex'&&after.selectedItem!==undefined?'item':diff('items')&&after.items.length?'item':null;
  case 8:return after.walk&&after.taken>before.taken?'collect':null;
  case 9:return diff('clean')?'magic':diff('trimmed')?'wipe':null;
  case 10:return after.selected.length>before.selected.length?'item':null;
  case 11:return diff('result')&&after.result!=='?'?'magic':null;
  case 12:return diff('gain')&&after.gain>0?'heal':diff('name')?'item':null;
  case 13:return k==='open'?'page':after.lines.length>before.lines.length?'write':k==='gets'?'page':null;
  case 14:return diff('zero')?'shield':diff('result')?'item':null;
  case 15:return diff('result')?'magic':null;
  case 16:return diff('result')?'craft':newStep>oldStep&&newStep===1?'item':null;
  case 17:return diff('value')&&after.value!=='?'?'scan':null;
  case 18:return k==='object-deleted'||(k==='object'&&a[1]==='destroy')?'vanish':k==='class'&&a[1]==='new'?'craft':k==='object'&&a[1]==='label'?'speak':null;
  case 19:return diff('flow')?'craft':null;
  case 20:return after.visited>before.visited?'scan':null;
  default:return null;
 }
}
const storyCues=[
 ['speak','speak','signal'],['coin','item','magic'],['door','door','door'],
 ['power','power','magic'],['power','signal','signal'],['coin','gate','signal'],
 ['item','click','item'],['collect','collect','collect'],['wipe','magic','magic'],
 ['scan','item','signal'],['craft','magic','magic'],['heal','scan','signal'],
 ['write','page','page'],['shield','item','magic'],['collect','magic','signal'],
 ['item','craft','signal'],['scan','scan','item'],['craft','speak','vanish'],
 ['scan','craft','signal'],['scan','scan','signal']
];
export function storyActionSound(id,step,props={}){
 if(step<1||step>3)return null;
 const cue=storyCues[id-1]?.[step-1]||null;
 return cue==='gate'?(props.enter?'door':'denied'):cue;
}
