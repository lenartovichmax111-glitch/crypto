const encoder = new TextEncoder();
const decoder = new TextDecoder();
const toBase64 = bytes => btoa(String.fromCharCode(...bytes));
const fromBase64 = text => Uint8Array.from(atob(text), c => c.charCodeAt(0));
async function keyFromPassword(password, salt) {
  const material = await crypto.subtle.importKey('raw', encoder.encode(password), 'PBKDF2', false, ['deriveKey']);
  return crypto.subtle.deriveKey({name:'PBKDF2',salt,iterations:250000,hash:'SHA-256'},material,{name:'AES-GCM',length:256},false,['encrypt','decrypt']);
}
export async function encryptNote(text,password){
  const salt=crypto.getRandomValues(new Uint8Array(16));
  const iv=crypto.getRandomValues(new Uint8Array(12));
  const key=await keyFromPassword(password,salt);
  const encrypted=new Uint8Array(await crypto.subtle.encrypt({name:'AES-GCM',iv},key,encoder.encode(text)));
  return JSON.stringify({v:1,salt:toBase64(salt),iv:toBase64(iv),data:toBase64(encrypted)});
}
export async function decryptNote(payload,password){
  const note=JSON.parse(payload);
  if(note.v!==1)throw new Error('Невідома версія шифрування');
  const key=await keyFromPassword(password,fromBase64(note.salt));
  return decoder.decode(await crypto.subtle.decrypt({name:'AES-GCM',iv:fromBase64(note.iv)},key,fromBase64(note.data)));
}
