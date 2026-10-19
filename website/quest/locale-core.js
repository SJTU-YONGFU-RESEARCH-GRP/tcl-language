// Pure translation lookup, also reused when exporting static illustrations.
export function translateText(value,messages){
 const input=String(value);if(!messages||!/[\u3400-\u9fff]/u.test(input))return input;
 const direct=messages.text[input];if(direct!==undefined)return direct;
 const trimmed=input.trim();if(messages.text[trimmed]!==undefined)return input.replace(trimmed,messages.text[trimmed]);
 for(const [pattern,replacement] of messages.patterns||[]){const re=new RegExp(pattern,'u');if(re.test(trimmed))return input.replace(trimmed,trimmed.replace(re,replacement));}
 const speaker=trimmed.match(/^(芯芯|咕咕|芽芽|铆铆|洛洛)(说|：)([\s\S]*)$/u);
 if(speaker){const name=messages.text[speaker[1]]||speaker[1];return input.replace(trimmed,speaker[2]==='说'?`${name} says`:`${name}: ${translateText(speaker[3],messages)}`);}
 return input;
}
