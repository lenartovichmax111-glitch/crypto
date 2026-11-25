import {encryptNote,decryptNote} from './crypto.js';
const API='http://127.0.0.1:8000/api';
const $=id=>document.getElementById(id);
let token=null;
function message(text){$('message').textContent=text}
async function request(path,method='GET',data){
 const response=await fetch(API+path,{method,headers:{'Content-Type':'application/json',...(token?{Authorization:`Bearer ${token}`}:{})},...(data?{body:JSON.stringify(data)}:{})});
 const result=await response.json();
 if(!response.ok)throw new Error(typeof result.detail==='string'?result.detail:'Помилка запиту');
 return result;
}
async function action(fn){try{await fn()}catch(error){message(error.message)}}
$('register').onclick=()=>action(async()=>{await request('/register','POST',{username:$('username').value,password:$('password').value});message('Акаунт створено. Тепер увійди.')});
$('login').onclick=()=>action(async()=>{const result=await request('/login','POST',{username:$('username').value,password:$('password').value});token=result.access_token;$('password').value='';$('auth').hidden=true;$('vault').hidden=false;message('Вхід успішний');await refresh()});
$('logout').onclick=()=>{token=null;$('vault').hidden=true;$('auth').hidden=false;$('notes').replaceChildren();$('key').value='';message('Ви вийшли')};
$('save').onclick=()=>action(async()=>{const title=$('title').value.trim(),content=$('content').value,key=$('key').value;if(!title||!content||key.length<8)throw new Error('Заповни назву, текст і пароль шифрування (від 8 символів)');const ciphertext=await encryptNote(content,key);await request('/notes','POST',{title,ciphertext});$('title').value='';$('content').value='';message('Нотатку зашифровано й збережено');await refresh()});
async function refresh(){const notes=await request('/notes');const root=$('notes');root.replaceChildren();if(!notes.length){root.textContent='Поки немає нотаток';return}for(const note of notes){const box=document.createElement('article');box.className='note';const title=document.createElement('h3');title.textContent=note.title;const date=document.createElement('div');date.className='muted';date.textContent=note.created_at;const body=document.createElement('p');body.textContent='Вміст зашифровано';const show=document.createElement('button');show.textContent='Розшифрувати';show.onclick=()=>action(async()=>{const key=$('key').value;if(!key)throw new Error('Введи пароль шифрування у полі вище');try{body.textContent=await decryptNote(note.ciphertext,key)}catch{throw new Error('Неправильний пароль або пошкоджена нотатка')}});const del=document.createElement('button');del.className='outline';del.textContent='Видалити';del.onclick=()=>action(async()=>{if(!confirm('Видалити нотатку?'))return;await request('/notes/'+note.id,'DELETE');await refresh()});box.append(title,date,body,show,del);root.append(box)}}
