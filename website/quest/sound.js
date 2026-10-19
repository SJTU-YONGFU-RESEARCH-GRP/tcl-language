/* Unlock one reusable context during a click, before Worker/replay callbacks. */
const melodies={
  enable:[523.25,783.99], run:[392], success:[659.25,783.99],
  error:[220,174.61], reward:[523.25,659.25,783.99,1046.5],
 click:[640],collect:[1174.66,1567.98],coin:[1318.51,1760],item:[523.25,783.99,1046.5],
 door:[110,164.81,220],denied:[196,174.61],power:[261.63,392,523.25],magic:[659.25,987.77],
 heal:[523.25,659.25,880],write:[960,640],page:[330,440],wipe:[480,320],
 shield:[196,392,587.33],craft:[146.83,293.66,587.33],scan:[880,1174.66],
 vanish:[523.25,261.63,130.81],signal:[783.99,1046.5],quiz:[659.25,880,1318.51]
};
export function createSoundPlayer({Context=globalThis.AudioContext||globalThis.webkitAudioContext,onStatus=()=>{}}={}){
  let enabled=false,context=null,master=null,revision=0,pending=null;
  const voices=new Map(),epochs=new Map(),lastPlayed=new Map();
  function status(value){onStatus(value);}
  function stop(channel){
    if(channel)epochs.set(channel,(epochs.get(channel)||0)+1);
    else{revision++;if(master)master.gain.value=0;}
    for(const [voice,owner] of voices){if(channel&&owner!==channel)continue;try{voice.stop();}catch{}voice.disconnect();voices.delete(voice);}
    if(channel)lastPlayed.delete(channel);else lastPlayed.clear();
  }
  function unlock(){
    if(!enabled)return Promise.resolve(false);
    if(!Context){status('unsupported');return Promise.resolve(false);}
    try{
      if(!context||context.state==='closed'){
        context=new Context();master=context.createGain();master.gain.value=0;master.connect(context.destination);
        context.onstatechange=()=>{if(enabled&&context.state!=='running')status('blocked');};
      }
      if(context.state==='running'){status('ready');return Promise.resolve(true);}
      if(pending)return pending;
      status('pending');
      // Call resume synchronously in the input handler, not after an await.
      const resume=context.resume();let timeout;
      pending=Promise.race([
        Promise.resolve(resume).then(()=>context.state==='running'),
        new Promise(resolve=>{timeout=setTimeout(()=>resolve(false),1800);})
      ]).catch(()=>false).then(ok=>{if(enabled)status(ok?'ready':'blocked');return ok;}).finally(()=>{clearTimeout(timeout);pending=null;});
      return pending;
    }catch{status('blocked');return Promise.resolve(false);}
  }
  async function play(name,{channel='feedback'}={}){
    if(!enabled||!melodies[name])return false;
    const request=revision,epoch=epochs.get(channel)||0;
    if(!await unlock()||!enabled||request!==revision||epoch!==(epochs.get(channel)||0))return false;
    const gap=channel==='ui'?.055:channel==='scene'?.04:0;
    if(gap&&context.currentTime-(lastPlayed.get(channel)??-Infinity)<gap)return false;
    lastPlayed.set(channel,context.currentTime);
    try{
      master.gain.value=.22;
      const start=context.currentTime+.008;
      const short=!['enable','reward','success','error','quiz'].includes(name);
      const gapTime=name==='click'?0:name==='door'?.09:short?.06:.13;
      const duration=name==='click'?.045:name==='door'?.22:short?.105:.19;
      melodies[name].forEach((frequency,i)=>{
        const oscillator=context.createOscillator(),gain=context.createGain(),at=start+i*gapTime;
        oscillator.type=['collect','coin','heal','magic'].includes(name)?'sine':'triangle';oscillator.frequency.value=frequency;
        gain.gain.setValueAtTime(0,at);gain.gain.linearRampToValueAtTime(name==='click'?.13:.27,at+.008);
        gain.gain.exponentialRampToValueAtTime(.001,at+duration-.01);
        oscillator.connect(gain);gain.connect(master);voices.set(oscillator,channel);
        oscillator.onended=()=>{voices.delete(oscillator);oscillator.disconnect();gain.disconnect();};
        oscillator.start(at);oscillator.stop(at+duration);
      });
      status('ready');return true;
    }catch{stop();status('blocked');return false;}
  }
  function setEnabled(value,{preview=true}={}){
    revision++;enabled=!!value;
    if(!enabled){stop();status('off');return Promise.resolve(false);}
    status('pending');return preview?play('enable'):Promise.resolve(false);
  }
  return {setEnabled,play,unlock,stop,get enabled(){return enabled;}};
}
