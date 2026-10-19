// This model consumes execution events, never the text of an unexecuted program.
const number=v=>v!==''&&v!==undefined&&v!==null&&Number.isFinite(Number(v))?Number(v):null;
const leaf=name=>String(name||'').split('::').pop();
const pairDict=list=>Object.fromEntries((list||[]).flatMap((v,i,a)=>i%2===0&&i+1<a.length?[[v,a[i+1]]]:[]));
const defaults=[
 {lines:[]},{name:'?',coins:'?'},{name:'?',upper:'?',outputs:[]},
 {bottles:'?',each:'?',bonus:'?',energy:'?'},{name:'?',cells:'?',each:'?',energy:'?',lastOutput:''},
 {coins:'?',enter:false},{items:[],selectedIndex:1},{items:[],total:'?',taken:0},
 {raw:'',trimmed:'',clean:''},{rows:[],selected:[],live:true},
 {n:'?',result:'?'},{name:'?',hp:0,gain:0},{lines:[],fileName:'?'},
 {a:'?',b:'?',result:'?',zero:'?',zeroA:'?'},{items:[],result:'?'},
 {w:'?',h:'?',result:'?',namespace:'?'},{line:'',value:'?'},
 {name:'?'},{name:'?',period:'?'},{rows:[],violations:0,worst:'?',visited:0}
];
export function createRuntimeModel(id){return {id,step:0,props:{...structuredClone(defaults[id-1]),runtime:true},vars:{},lists:{},output:[],changed:[],additions:0,previousTotal:0,flags:new Set(),caption:null,lastEvent:null};}
export function advanceRuntime(model,event){
 const m=model,p=m.props,id=m.id,e=event,a=e.args||[],k=e.kind,phase=e.phase||'leave';
 const before=JSON.stringify([m.step,p]);
 if(id===8)p.walk=false;
 m.lastEvent=e;
 Object.assign(m.vars,e.vars||{});Object.assign(m.lists,e.lists||{});
 const v=m.vars,L=m.lists;
 const set=(key,value)=>{if(value!==undefined)p[key]=value;};
 const nset=(key,value)=>{const n=number(value);if(n!==null)p[key]=n;};
 const step=n=>{m.step=Math.max(m.step,n);};
 if(k==='stdout'){
  m.output.push(e.text);m.output=m.output.slice(-16);
  if(id===1){p.lines=m.output.slice(-4);m.step=Math.min(3,m.output.length===1?1:m.output.length+1);}
  if(id===2){p.outputText=e.text;step(3);}
  if(id===3){p.outputs=m.output.slice(0,3);step(Math.min(3,m.output.length));}
  if([4,5,9,11,12,13,15,16,17,19,20].includes(id))step(3);
  if(id===5)p.lastOutput=e.text;
  if(id===6){p.reply=e.text;if(e.text==='Enter'||e.text==='Wait')p.enter=e.text==='Enter';step(3);}
  if(id===7)step(m.output.length>=2?3:2);
  if(id===8){nset('total',v.total);step(3);}
  if(id===10)step(3);
  if(id===14)step(m.output.length>=2?3:2);
  if(id===18)step(2);
 }else if(e.code===0||e.code===2){
  switch(id){
   case 1:break;
   case 2:set('name',v.hero);nset('coins',v.coins);if(v.coins!==undefined)step(1);break;
   case 3:set('name',v.hero);if(k==='string'&&a[1]==='toupper'){p.upper=e.result;step(2);}break;
   case 4:
    nset('bottles',v.bottles);nset('each',v.each);nset('energy',v.energy);
    if(k==='set'&&a[1]==='energy')step(1);
    if(k==='incr'&&a[1]==='energy'){nset('bonus',a[2]??1);step(2);}break;
   case 5:set('name',v.hero);nset('cells',v.cells);nset('each',v.each);nset('energy',v.energy);if(v.energy!==undefined)step(1);break;
   case 6:
    nset('coins',v.coins);
    if(k==='call'&&leaf(a[0])==='gate'){nset('coins',a[1]);p.enter=e.result==='Enter';p.reply=e.result;step(2);}break;
   case 7:
    if(L.bag){p.items=L.bag;step(1);}
    if(k==='llength')step(2);
    if(k==='lindex'){nset('selectedIndex',a[2]);p.selectedItem=e.result;step(3);}break;
   case 8:
    if(['foreach','for','while'].includes(k)&&phase==='enter')m.flags.add('loop');
    if(k==='foreach'&&phase==='enter'){const values=(e.argLists?.[2]||[]).map(number);if(values.every(n=>n!==null)){p.items=values;p.taken=0;}m.previousTotal=number(v.total)??0;}
    if((k==='incr'||k==='set')&&a[1]==='total'){
     const total=number(e.result);
     if(total!==null){
      const initial=k==='set'&&!m.flags.has('loop')&&m.additions===0;
      if(!initial){const delta=total-m.previousTotal;m.additions++;p.previousTaken=p.taken;p.walk=true;if(!p.items.length||m.additions>p.items.length)p.items.push(delta);p.taken=m.additions;step(Math.min(3,m.additions));}
      p.total=total;m.previousTotal=total;
     }
    }
    if(['foreach','for','while'].includes(k)&&phase==='leave'){nset('total',v.total);p.taken=m.additions;step(3);}break;
   case 9:
    if(k==='string'&&a[1]==='trim'){p.raw=a[2]||'';p.trimmed=e.result;step(1);}
    if(k==='string'&&a[1]==='toupper'){p.clean=e.result;step(2);}
    if(k==='call'&&leaf(a[0])==='clean'){p.raw=a[1]||'';p.clean=e.result;step(2);}break;
   case 10:
    if(k==='foreach'&&phase==='enter'){p.rows=(e.loopRows||[]).filter(r=>r.length>=2&&number(r[1])!==null).map(r=>[r[0],number(r[1])]);step(1);}
    if(L.selected){p.selected=L.selected;if(k==='lappend')step(2);}
    if(k==='call'&&leaf(a[0])==='supply'){p.selected=e.resultList||[];step(3);}break;
   case 11:
    nset('n',v.n);
    if(k==='expr'&&v.n!==undefined){p.result=e.result;step(1);}
    if(k==='call'&&leaf(a[0])==='double'){set('n',a[1]);p.result=e.result;step(2);}break;
   case 12:{
    const dict=pairDict(L.hero);
    if(dict.name!==undefined)p.name=dict.name;
    if(number(dict.hp)!==null){if(!m.flags.has('hp')){p.hp=Number(dict.hp);m.flags.add('hp');}else{p.gain=Number(dict.hp)-p.hp;step(1);}}
    if(k==='dict'&&a[1]==='get')step(2);break;}
   case 13:
    if(k==='open'){p.fileName=a[1];if(a[2]==='r')step(2);}
    if(k==='puts'&&a.length>=3&&a[1]!=='stdout'&&a[1]!=='stderr'&&a[1]!=='-nonewline'){p.lines.push(a.at(-1));p.lines=p.lines.slice(-4);step(1);}
    if(k==='close')step(2);
    if(k==='gets'){p.readBack=e.result;step(3);}break;
   case 14:
    if(k==='call'&&leaf(a[0])==='safeDivide'){
     if(number(a[2])===0){p.zero=e.result;p.zeroA=a[1];step(1);}else{p.a=a[1];p.b=a[2];p.result=e.result;step(2);}
    }break;
   case 15:
    if(L.numbers&&L.numbers.every(x=>number(x)!==null))p.items=L.numbers.map(Number);
    if(k==='set'&&a[1]==='total')step(1);
    if(k==='call'&&leaf(a[0])==='average'){p.items=(e.argLists?.[1]||[]).map(number).filter(x=>x!==null);p.result=e.result;step(2);}break;
   case 16:
    if(k==='proc'&&leaf(a[1])==='area'){p.namespace=e.scope?.replace(/^::/,'')||'?';step(1);}
    if(k==='call'&&leaf(a[0])==='area'){p.namespace=String(a[0]).includes('::')?String(a[0]).split('::').slice(0,-1).join('::').replace(/^::/,''):e.scope?.replace(/^::/,'')||'?';set('w',a[1]);set('h',a[2]);p.result=e.result;step(2);}break;
   case 17:
    if(k==='regexp'){p.line=a[2]||'';p.value=e.result==='1'?(v[a[4]]??v.value??'?'):'NA';step(2);}
    if(k==='call'&&leaf(a[0])==='slackValue'){p.line=a[1]||'';p.value=e.result;step(2);}break;
   case 18:
    if(k==='oo::class')step(0);
    if(k==='class'&&a[1]==='new'){p.name=a[2]??'?';step(1);}
    if(k==='set'&&a[1]==='name'){p.name=e.result;step(1);}
    if(k==='object'&&a[1]==='label'){p.name=e.result;step(2);}
    if((k==='object'&&a[1]==='destroy')||k==='object-deleted')step(3);break;
   case 19:
    set('name',v.design);set('period',v.period);
    if(k==='call'&&leaf(a[0])==='mockFlow'){p.name=a[1]??'?';p.period=a[2]??'?';p.flow=e.resultList||[];if(p.flow.length===3)step(2);}break;
   case 20:
    if(k==='foreach'&&phase==='enter'){p.rows=(e.loopRows||[]).filter(r=>r.length>=2&&number(r[1])!==null).map(r=>[r[0],number(r[1])]);p.visited=0;}
    if(k==='lassign'){p.visited++;step(1);}
    nset('violations',v.violations);set('worst',v.worst);
    if(k==='set'&&a[1]==='worst')step(2);
    if(k==='call'&&leaf(a[0])==='analyze'){
     const dict=pairDict(e.resultList);if(dict.violations!==undefined)nset('violations',dict.violations);set('worst',dict.worst);step(3);
    }break;
  }
 }else if(id===19&&k==='call'&&leaf(a[0])==='mockFlow'){
  p.name=a[1]??'?';p.period=a[2]??'?';p.error=e.result;m.step=1;
 }
 if(k==='set'||k==='incr'||k==='lappend'){
  const key=a[1];if(key&&!key.startsWith('::__quest_')){m.changed=m.changed.filter(x=>x.name!==key);m.changed.push({name:key,value:e.result});m.changed=m.changed.slice(-5);}
 }
 return before!==JSON.stringify([m.step,p]);
}
