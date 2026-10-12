from flask import Flask, request, jsonify, render_template_string
import urllib.request
import urllib.parse
import json
import html
import re
import ast
import operator
import os
import math
import unicodedata

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1_000_000

# =========================================================
# NYVEXIA AI — CONVERSATIONAL INTELLIGENCE ENGINE
# Keep existing browser chat-history storage key.
# =========================================================

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#080a18">
<title>Nyvexia AI — Think Beyond</title>
<style>
:root {
 --purple:#8B5CF6;--cyan:#22D3EE;--pink:#F472B6;
 --bg:#080a18;--panel:rgba(9,13,34,.94);
 --text:#F5F7FF;--muted:#98a6cf;
 --border:rgba(117,133,255,.22)
}
*{box-sizing:border-box}
html,body{margin:0;width:100%;height:100%}
body{overflow:hidden;color:var(--text);background:var(--bg);
 font-family:Inter,ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif}
button,input,textarea{font:inherit}button{cursor:pointer}
button:focus-visible,input:focus-visible,textarea:focus-visible{
 outline:2px solid var(--cyan);outline-offset:3px}
.space-background{position:fixed;inset:0;z-index:-2;background:
 radial-gradient(ellipse at 72% 15%,rgba(78,37,164,.24),transparent 36%),
 radial-gradient(ellipse at 45% 88%,rgba(15,87,170,.17),transparent 42%),#080a18}
.space-background:before{content:"";position:absolute;inset:0;opacity:.4;
 background-image:radial-gradient(1px 1px at 8% 18%,#fff 99%,transparent),
 radial-gradient(1px 1px at 22% 72%,#9eeaff 99%,transparent),
 radial-gradient(1px 1px at 41% 12%,#fff 99%,transparent),
 radial-gradient(2px 2px at 69% 35%,#a7a5ff 99%,transparent),
 radial-gradient(1px 1px at 85% 81%,#fff 99%,transparent);
 background-size:240px 220px,300px 260px,350px 300px,280px 240px,320px 290px}
.app{position:relative;display:grid;grid-template-columns:250px minmax(0,1fr) 270px;
 gap:10px;width:100%;height:100dvh;padding:12px}
.sidebar,.main,.right-panel{min-width:0;border:1px solid var(--border);
 background:var(--panel);border-radius:20px;backdrop-filter:blur(18px)}
.sidebar{display:flex;flex-direction:column;padding:17px 13px 12px;overflow:hidden}
.brand{display:flex;align-items:center;gap:11px;padding:7px 7px 23px}
.logo{width:44px;height:44px;flex-shrink:0;display:grid;place-items:center;
 border-radius:15px;color:white;font-size:24px;
 background:linear-gradient(140deg,#703cff,#263eac 70%,#126b96);
 box-shadow:0 0 25px #6f43ff38}
.brand-name{font-size:17px;font-weight:780;letter-spacing:-.5px}
.brand-sub{color:#b39bff;font-size:11px;margin-top:4px;letter-spacing:.5px}
.new-chat{width:100%;padding:13px 14px;border:1px solid #8b5cf68c;
 border-radius:12px;color:white;text-align:left;background:linear-gradient(110deg,#5424d7,#3921a7)}
.new-chat:hover{filter:brightness(1.15)}
.search-wrap{margin:13px 0 21px}
.search-wrap input{width:100%;padding:11px 12px;border:1px solid var(--border);
 border-radius:11px;color:white;background:#04081cc7;font-size:12px}
.section-label{display:flex;justify-content:space-between;padding:0 8px 10px;
 color:#8497e4;font-size:10px;font-weight:750;letter-spacing:1.3px}
.chat-list{overflow-y:auto;flex:1;min-height:60px}
.chat-item{display:flex;align-items:center;gap:9px;margin-bottom:5px;padding:11px 8px;
 border:1px solid transparent;border-radius:12px;color:#c7d1f4;cursor:pointer;font-size:12px}
.chat-item:hover{background:#5b58c21f}
.chat-item.active{background:linear-gradient(110deg,#5a30d03d,#192a6733);
 border-color:#775cff59;color:white}
.chat-icon{display:grid;place-items:center;flex-shrink:0;width:31px;height:31px;
 border:1px solid #7b71ff59;border-radius:10px;background:#5540c52e}
.chat-copy{min-width:0;flex:1}.chat-title{display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.chat-date{display:block;margin-top:4px;color:#8191c4;font-size:10px}
.delete-chat{border:0;color:#8290bc;background:transparent;font-size:17px}
.galaxy-toggle{margin-top:12px;padding:12px 10px;border:1px solid #6c52f05c;
 border-radius:13px;background:#291f6826}
.toggle-line{display:flex;align-items:center;gap:9px}
.toggle-symbol{display:grid;place-items:center;width:32px;height:32px;border-radius:10px;background:#764dff33}
.toggle-copy{flex:1;font-size:12px;font-weight:650}
.toggle-description{margin:8px 0 0 41px;color:#7f8ebc;font-size:9px}
.switch{width:34px;height:19px;border:0;border-radius:20px;padding:2px;background:#454a69}
.switch span{display:block;width:15px;height:15px;border-radius:50%;background:white;transition:transform .2s}
.switch.on{background:#7042f5}.switch.on span{transform:translateX(15px)}
.sidebar-bottom{display:flex;align-items:center;gap:10px;margin-top:11px;padding:13px 6px 4px;border-top:1px solid var(--border)}
.profile-icon{display:grid;place-items:center;width:37px;height:37px;border:1px solid #7775ff66;
 border-radius:50%;background:#171d48}
.profile-name{font-size:11px;font-weight:650}.profile-sub{margin-top:4px;color:#8b9bd0;font-size:10px}
.main{display:flex;flex-direction:column;position:relative;overflow:hidden}
.topbar{min-height:72px;flex-shrink:0;display:flex;align-items:center;justify-content:space-between;
 gap:12px;padding:0 20px;border-bottom:1px solid #7082ff29;background:#080b1d99}
.topbar-left{display:flex;align-items:center;gap:11px;min-width:0}
.topbar-icon{display:grid;place-items:center;width:36px;height:36px;flex-shrink:0;
 border-radius:12px;background:#111943;color:#a99cff}
.current-title{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:13px;font-weight:700}
.current-subtitle{margin-top:4px;color:#9aa9dc;font-size:11px}
.top-actions{display:flex;align-items:center;gap:7px}
.small-btn{padding:8px 10px;border:1px solid transparent;border-radius:10px;color:#d5ddff;background:#1f275480;font-size:12px}
.small-btn:hover{border-color:#8b5cf68c;background:#171e48}
.mobile-menu{display:none}
.messages{flex:1;min-height:0;overflow-y:auto;padding:26px 24px 24px;scroll-behavior:smooth}
.message-list{width:100%;max-width:820px;margin:0 auto}
.welcome{padding:5vh 0 25px;text-align:center}
.welcome-mark{display:grid;place-items:center;width:67px;height:67px;margin:0 auto 17px;
 border:1px solid #8973ff80;border-radius:23px;color:#eeeaff;font-size:30px;
 background:linear-gradient(145deg,#6f3dff4d,#1e6cb83b);box-shadow:0 0 42px #6645ff21}
.welcome h1{margin:0 0 9px;font-size:clamp(28px,3.4vw,43px);letter-spacing:-1.7px;font-weight:760}
.welcome h1 span{background:linear-gradient(95deg,#e0d3ff,#a58bff 52%,#67e8f9);
 -webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}
.welcome p{max-width:450px;margin:0 auto;color:#9ba9d3;font-size:13px;line-height:1.75}
.suggestions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;max-width:610px;margin:25px auto 0}
.suggestion{display:flex;align-items:center;gap:11px;min-height:68px;padding:12px;text-align:left;
 border:1px solid #6a74ff3d;border-radius:14px;color:#e4e9ff;background:linear-gradient(120deg,#182050a8,#0b0f2bb3)}
.suggestion:hover{border-color:#8b5cf6b3;background:#3d2a873d}
.suggestion-icon{display:grid;place-items:center;width:36px;height:36px;flex-shrink:0;
 border:1px solid #6482ff4d;border-radius:12px;background:#263a9c66;color:#83eaff}
.suggestion-copy{font-size:11px;font-weight:650}
.suggestion-copy span{display:block;margin-top:5px;color:#93a2d2;font-size:10px;font-weight:400}
.message{display:flex;gap:12px;margin-bottom:25px;align-items:flex-start}
.avatar{display:grid;place-items:center;width:34px;height:34px;flex-shrink:0;
 border:1px solid #8076ff59;border-radius:12px;color:white;background:linear-gradient(145deg,#6139df,#174b98);font-weight:750}
.avatar.user{background:#242c54;color:#d9e5ff}
.message-body{min-width:0;flex:1;padding-top:3px}
.message-name{margin-bottom:8px;color:#a8b4df;font-size:11px;font-weight:700}
.message-text{color:#e5eaff;font-size:13px;line-height:1.85;white-space:pre-wrap;overflow-wrap:anywhere}
.message.bot-message .message-body{padding:15px 17px;border:1px solid #6e74ff47;border-radius:5px 16px 16px 16px;
 background:linear-gradient(135deg,#161e4ed4,#0a102bd9)}
.message.bot-message .message-name{color:#b8a5ff}
.sources{display:flex;flex-wrap:wrap;gap:7px;margin-top:13px}
.source-link{max-width:100%;overflow-wrap:anywhere;padding:6px 9px;border:1px solid #7868ff61;border-radius:20px;
 color:#c4bcff;background:#6344e11f;font-size:10px;text-decoration:none}
.source-link:hover{border-color:var(--cyan);color:#aaf5ff}
.composer-area{flex-shrink:0;padding:8px 22px 18px}
.composer-wrap{max-width:850px;margin:0 auto}
.composer{display:flex;align-items:flex-end;gap:7px;padding:9px;border:1px solid #8b5cf68c;
 border-radius:24px;background:#070b1ff5;box-shadow:0 0 25px #5731eb17}
.composer:focus-within{border-color:#22d3eeb3;box-shadow:0 0 25px #22d3ee17}
#question{min-width:0;flex:1;resize:none;max-height:140px;padding:9px 7px;border:0;outline:0;
 color:white;background:transparent;font-size:13px;line-height:1.6}
#question::placeholder{color:#8998c7}
.icon-btn,.send-btn{display:grid;place-items:center;width:37px;height:37px;flex-shrink:0;border:1px solid transparent;
 border-radius:12px;color:#a7b4e5;background:transparent;font-size:17px}
.icon-btn:hover,.icon-btn.active{border-color:#22d3ee4d;color:var(--cyan);background:#22d3ee17}
.send-btn{color:white;background:linear-gradient(140deg,#8549ff,#5330d8);font-size:20px}
.disclaimer{margin-top:10px;color:#7281b0;text-align:center;font-size:9px}
.right-panel{display:flex;flex-direction:column;gap:10px;padding:12px;overflow-y:auto}
.panel-card{padding:13px;border:1px solid #6775ff3d;border-radius:16px;background:#070b20b8}
.panel-title{margin:0 0 12px;font-size:13px;font-weight:750}
.action-item{display:flex;align-items:center;gap:10px;width:100%;margin-bottom:7px;padding:9px;
 border:1px solid #6374ff40;border-radius:12px;text-align:left;color:white;background:#11173aa6}
.action-item:hover{border-color:#8b5cf6a6;background:#45309133}
.action-icon{display:grid;place-items:center;width:34px;height:34px;flex-shrink:0;border:1px solid #50a0ff4d;
 border-radius:11px;color:#7be9ff;background:#1e449f59}
.action-copy{font-size:11px;font-weight:650}
.action-copy span{display:block;margin-top:4px;color:#94a4d4;font-size:10px;font-weight:400}
.feature-list{display:grid;gap:10px}
.feature-row{display:flex;align-items:center;gap:9px;color:#c1cff6;font-size:11px}
.feature-dot{display:grid;place-items:center;width:19px;height:19px;border:1px solid #7670ff59;
 border-radius:7px;color:#a7a1ff;background:#503ebc38;font-size:10px}
.promo{position:relative;display:flex;flex:1;min-height:150px;flex-direction:column;justify-content:flex-end;
 overflow:hidden;padding:16px;border:1px solid #6e65ff52;border-radius:16px;
 background:radial-gradient(ellipse at 50% 28%,#7434ff5c,transparent 44%),radial-gradient(ellipse at 70% 75%,#1275c43d,transparent 50%),#080d27}
.promo-orbit{position:absolute;top:17px;left:50%;transform:translateX(-50%);width:95px;height:95px;
 border:1px solid #9c82ff80;border-radius:50%;box-shadow:0 0 24px #784bff26,inset 0 0 22px #594cf01f}
.promo-orbit:before,.promo-orbit:after{content:"";position:absolute;inset:16px -8px;border:2px solid #8566ffb3;border-radius:50%;transform:rotate(-32deg)}
.promo-orbit:after{inset:27px -13px;border-color:#22d3ee80;transform:rotate(35deg)}
.promo-copy{position:relative;text-align:center}.promo-copy strong{display:block;font-size:14px}
.promo-copy p{margin:7px 0 0;color:#a9b8e7;font-size:11px;line-height:1.7}
.typing{display:inline-flex;gap:5px;padding:5px 0}
.typing span{width:5px;height:5px;border-radius:50%;background:#b2a0ff;animation:pulse 1s infinite alternate}
.typing span:nth-child(2){animation-delay:.2s}.typing span:nth-child(3){animation-delay:.4s}
@keyframes pulse{from{opacity:.3;transform:translateY(0)}to{opacity:1;transform:translateY(-3px)}}
.toast{position:fixed;z-index:100;bottom:25px;left:50%;transform:translateX(-50%);display:none;max-width:calc(100vw - 30px);
 padding:11px 16px;border:1px solid var(--border);border-radius:12px;color:white;background:#171b3a;box-shadow:0 10px 40px #0008;font-size:12px}
body.galaxy-off .space-background:before{opacity:.08}
body.galaxy-off .space-background{background:radial-gradient(ellipse at 75% 5%,#17133c,transparent 42%),#0b1021}
@media(min-width:1450px){.app{grid-template-columns:280px minmax(0,1fr) 300px;gap:12px;padding:15px}.messages{padding:32px}}
@media(max-width:1120px){.app{grid-template-columns:240px minmax(0,1fr)}.right-panel{display:none}}
@media(max-width:720px){
 .app{display:block;padding:0}.sidebar{position:fixed;z-index:30;top:0;bottom:0;left:0;width:min(290px,86vw);
 border-radius:0 18px 18px 0;transform:translateX(-110%);transition:transform .22s;box-shadow:15px 0 45px #0009}
 .sidebar.open{transform:translateX(0)}.main{width:100%;height:100dvh;border:0;border-radius:0}
 .topbar{min-height:62px;padding:0 12px;gap:7px}.mobile-menu{display:inline-block}
 .current-title{max-width:155px;font-size:12px}.current-subtitle{font-size:10px}
 .top-actions{gap:4px}.small-btn{padding:7px 8px;font-size:11px}
 .messages{padding:18px 13px}.welcome{padding-top:5vh}.welcome h1{font-size:30px}
 .welcome-mark{width:58px;height:58px;border-radius:19px}
 .suggestions{grid-template-columns:1fr;gap:8px;margin-top:22px}.suggestion{min-height:59px}
 .message{gap:8px;margin-bottom:20px}.avatar{width:30px;height:30px;border-radius:10px}
 .message.bot-message .message-body{padding:12px}.message-text{font-size:13px}
 .composer-area{padding:7px 10px 12px}.composer{gap:3px;padding:7px}
 .icon-btn,.send-btn{width:34px;height:35px}.disclaimer{font-size:9px}
}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}}
</style>
</head>
<body>
<div class="space-background"></div>
<div class="app">
 <aside class="sidebar" id="sidebar">
  <div class="brand"><div class="logo">✦</div><div><div class="brand-name">Nyvexia AI</div><div class="brand-sub">Think Beyond.</div></div></div>
  <button class="new-chat" id="newChat">＋ &nbsp; New Chat</button>
  <div class="search-wrap"><input id="historySearch" placeholder="⌕  Search chats..." autocomplete="off"></div>
  <div class="section-label"><span>CHAT HISTORY</span><span>⌃</span></div>
  <div class="chat-list" id="chatList"></div>
  <div class="galaxy-toggle"><div class="toggle-line"><div class="toggle-symbol">✧</div><div class="toggle-copy">Galaxy Mode</div><button class="switch on" id="galaxyToggle" aria-label="Toggle galaxy mode"><span></span></button></div><div class="toggle-description">A little more cosmic. Still focused.</div></div>
  <div class="sidebar-bottom"><div class="profile-icon">✦</div><div><div class="profile-name">Nyvexia AI</div><div class="profile-sub">Your AI assistant</div></div></div>
 </aside>
 <main class="main">
  <header class="topbar">
   <div class="topbar-left"><button class="small-btn mobile-menu" id="menuBtn" aria-label="Open chat history">☰</button><div class="topbar-icon">▤</div><div style="min-width:0"><div class="current-title" id="currentTitle">New Chat</div><div class="current-subtitle">Your universe. Your questions.</div></div></div>
   <div class="top-actions"><button class="small-btn" id="renameBtn" title="Rename conversation">✎ <span>Rename</span></button><button class="small-btn" id="voiceToggle" title="Toggle spoken replies">◖))</button><button class="small-btn" id="fullscreenBtn" title="Toggle fullscreen">⛶</button></div>
  </header>
  <section class="messages" id="messages"><div class="message-list" id="messageList"></div></section>
  <div class="composer-area"><div class="composer-wrap">
   <form class="composer" id="form"><button class="icon-btn" type="button" id="micBtn" title="Speak your message">♩</button><textarea id="question" rows="1" placeholder="Ask Nyvexia anything..." autocomplete="off"></textarea><button class="icon-btn" type="button" id="webBtn" title="Search the web">◎</button><button class="icon-btn" type="button" id="mathBtn" title="Calculate">▦</button><button class="icon-btn" type="button" id="translateBtn" title="Translate">文</button><button class="send-btn" id="send" type="submit">➤</button></form>
   <div class="disclaimer">Nyvexia can make mistakes. Verify important information.</div>
  </div></div>
 </main>
 <aside class="right-panel">
  <section class="panel-card"><h2 class="panel-title">Quick Actions</h2>
   <button class="action-item" data-prompt="Search the web for the latest news about space exploration"><span class="action-icon">⌕</span><span class="action-copy">Search the Web<span>Find relevant web results</span></span></button>
   <button class="action-item" data-prompt="Solve 3x + 7 = 22 and show the steps"><span class="action-icon">▦</span><span class="action-copy">Solve Math<span>Calculations and equations</span></span></button>
   <button class="action-item" data-prompt="Translate 'Hello, how are you?' into French"><span class="action-icon">文</span><span class="action-copy">Translate<span>Try another language</span></span></button>
   <button class="action-item" id="voiceAction"><span class="action-icon">♩</span><span class="action-copy">Voice Input<span>Talk to Nyvexia</span></span></button>
   <button class="action-item" id="listenAction"><span class="action-icon">◖))</span><span class="action-copy">Listen<span>Toggle spoken replies</span></span></button>
  </section>
  <section class="panel-card"><h2 class="panel-title">Features</h2><div class="feature-list">
   <div class="feature-row"><span class="feature-dot">✓</span> Conversational AI</div><div class="feature-row"><span class="feature-dot">✓</span> Web search and sources</div><div class="feature-row"><span class="feature-dot">✓</span> Math and calculations</div><div class="feature-row"><span class="feature-dot">✓</span> Multilingual translation</div><div class="feature-row"><span class="feature-dot">✓</span> Voice input and speech</div><div class="feature-row"><span class="feature-dot">✓</span> Saved browser chat history</div>
  </div></section>
  <section class="promo"><div class="promo-orbit"></div><div class="promo-copy"><strong>Explore more...</strong><p>The universe of knowledge<br>starts with a question.</p></div></section>
 </aside>
</div>
<div class="toast" id="toast"></div>
<script>
const STORAGE_KEY="nyvexia_galaxy_chats_v1";
const VOICE_KEY="nyvexia_voice_enabled_v1";
const GALAXY_KEY="nyvexia_galaxy_mode_v1";
const welcomeMessage={who:"bot",text:"Hey! I'm Nyvexia AI. Ask me anything, get help with schoolwork, write a text, brainstorm, or just chat with me.",links:[]};
let chats=[],activeId=null,busy=false;
let voiceEnabled=localStorage.getItem(VOICE_KEY)==="true";
let galaxyEnabled=localStorage.getItem(GALAXY_KEY)!=="false";
let recognition=null,toastTimer=null;
const $=id=>document.getElementById(id);
const messagesBox=$("messages"),messageList=$("messageList"),questionBox=$("question"),sendButton=$("send");

function makeChat(){return{id:(crypto.randomUUID?crypto.randomUUID():String(Date.now())+Math.random()),title:"New conversation",messages:[{...welcomeMessage}],apiHistory:[],created:Date.now()}}
function loadChats(){
 try{const saved=JSON.parse(localStorage.getItem(STORAGE_KEY)||"[]");
  if(Array.isArray(saved))chats=saved.filter(c=>c&&c.id&&Array.isArray(c.messages)).map(c=>({id:c.id,title:c.title||"New conversation",messages:c.messages,apiHistory:Array.isArray(c.apiHistory)?c.apiHistory:[],created:c.created||Date.now()}))
 }catch(e){chats=[]}
 if(!chats.length)chats=[makeChat()];activeId=chats[0].id;saveChats()
}
function saveChats(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(chats))}catch(e){showToast("Could not save chats in this browser.")}}
function activeChat(){return chats.find(c=>c.id===activeId)||chats[0]}
function showToast(text){const el=$("toast");el.textContent=text;el.style.display="block";clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.style.display="none",3000)}
function relativeDate(timestamp){const d=new Date(timestamp||Date.now());const today=new Date();return d.toDateString()===today.toDateString()?"Today, "+d.toLocaleTimeString([],{hour:"2-digit",minute:"2-digit"}):d.toLocaleDateString([],{month:"short",day:"numeric"})}
function renderChats(){
 const term=$("historySearch").value.trim().toLowerCase(),list=$("chatList");list.innerHTML="";
 const filtered=[...chats].sort((a,b)=>(b.created||0)-(a.created||0)).filter(c=>!term||c.title.toLowerCase().includes(term)||c.messages.some(m=>String(m.text||"").toLowerCase().includes(term)));
 if(!filtered.length){list.textContent="No matching conversations.";list.style.padding="10px";list.style.color="#91a0cf";list.style.fontSize="12px";return}
 list.style.padding="";
 filtered.forEach(chat=>{
  const item=document.createElement("div");item.className="chat-item"+(chat.id===activeId?" active":"");
  const icon=document.createElement("span");icon.className="chat-icon";icon.textContent="◇";
  const copy=document.createElement("span");copy.className="chat-copy";
  const title=document.createElement("span");title.className="chat-title";title.textContent=chat.title;
  const date=document.createElement("span");date.className="chat-date";date.textContent=relativeDate(chat.created);copy.append(title,date);
  const del=document.createElement("button");del.className="delete-chat";del.textContent="⋮";del.title="Delete conversation";
  del.onclick=e=>{e.stopPropagation();deleteChat(chat.id)};
  item.append(icon,copy,del);item.onclick=()=>{activeId=chat.id;renderAll();if(innerWidth<=720)$("sidebar").classList.remove("open")};list.append(item)
 })
}
function welcomeHTML(){return `<div class="welcome"><div class="welcome-mark">✦</div><h1>Nyvexia <span>AI</span></h1><p>Ask. Explore. Discover. Your space to think beyond the ordinary.</p><div class="suggestions">
<button class="suggestion" data-prompt="Help me understand a school subject in simple words"><span class="suggestion-icon">✧</span><span class="suggestion-copy">Understand a subject<span>Simple explanations</span></span></button>
<button class="suggestion" data-prompt="Write a French text suitable for Secondary 3 about volcanoes"><span class="suggestion-icon">✎</span><span class="suggestion-copy">Write a text<span>Schoolwork and creativity</span></span></button>
<button class="suggestion" data-prompt="Solve 3x + 7 = 22 and show the steps"><span class="suggestion-icon">▦</span><span class="suggestion-copy">Solve a math problem<span>See the steps</span></span></button>
<button class="suggestion" data-prompt="Tell me an interesting fact and explain it"><span class="suggestion-icon">✦</span><span class="suggestion-copy">Explore an idea<span>Discover something new</span></span></button>
</div></div>`}
function renderMessages(){
 const chat=activeChat();if(!chat)return;$("currentTitle").textContent=chat.title;messageList.innerHTML="";
 if(chat.messages.length===1&&chat.messages[0].text===welcomeMessage.text){
  messageList.innerHTML=welcomeHTML();messageList.querySelectorAll("[data-prompt]").forEach(b=>b.onclick=()=>{questionBox.value=b.dataset.prompt;questionBox.focus();resizeInput()});return
 }
 chat.messages.forEach(msg=>{
  const row=document.createElement("div");row.className="message"+(msg.who==="user"?" user-message":" bot-message");
  const av=document.createElement("div");av.className="avatar "+(msg.who==="user"?"user":"bot");av.textContent=msg.who==="user"?"Y":"✦";
  const body=document.createElement("div");body.className="message-body";
  const name=document.createElement("div");name.className="message-name";name.textContent=msg.who==="user"?"You":"Nyvexia AI";
  const content=document.createElement("div");content.className="message-text";content.textContent=msg.text||"";body.append(name,content);
  if(msg.who!=="user"&&Array.isArray(msg.links)&&msg.links.length){
   const links=document.createElement("div");links.className="sources";
   msg.links.forEach(link=>{if(!link.url||!/^https?:\/\//i.test(link.url))return;const a=document.createElement("a");a.className="source-link";a.href=link.url;a.target="_blank";a.rel="noopener noreferrer";a.textContent=link.title||"Source";links.append(a)});body.append(links)
  }
  row.append(av,body);messageList.append(row)
 });
 if(busy){const row=document.createElement("div");row.className="message bot-message";row.innerHTML='<div class="avatar bot">✦</div><div class="message-body"><div class="message-name">Nyvexia AI</div><div class="typing"><span></span><span></span><span></span></div></div>';messageList.append(row)}
}
function renderAll(){renderChats();renderMessages();saveChats();$("voiceToggle").textContent=voiceEnabled?"◖)) On":"◖))";$("galaxyToggle").classList.toggle("on",galaxyEnabled);document.body.classList.toggle("galaxy-off",!galaxyEnabled);requestAnimationFrame(()=>messagesBox.scrollTop=messagesBox.scrollHeight)}
function createNewChat(){const c=makeChat();chats.unshift(c);activeId=c.id;questionBox.value="";resizeInput();renderAll();questionBox.focus();if(innerWidth<=720)$("sidebar").classList.remove("open")}
function deleteChat(id){const c=chats.find(x=>x.id===id);if(!c||!confirm('Delete "'+c.title+'"?'))return;chats=chats.filter(x=>x.id!==id);if(!chats.length)chats=[makeChat()];if(activeId===id)activeId=chats[0].id;renderAll()}
function renameChat(){const c=activeChat();if(!c)return;const v=prompt("Rename this conversation:",c.title);if(v===null)return;const n=v.trim().slice(0,70);if(!n)return showToast("The title can't be empty.");c.title=n;renderAll()}
function autoTitle(c,t){if(c.title==="New conversation"){t=t.replace(/\s+/g," ").trim();c.title=t.length>34?t.slice(0,31)+"...":t}}
function resizeInput(){questionBox.style.height="auto";questionBox.style.height=Math.min(questionBox.scrollHeight,140)+"px"}

async function sendMessage(override){
 if(busy)return;const question=(typeof override==="string"?override:questionBox.value).trim();if(!question)return;
 const chat=activeChat();questionBox.value="";resizeInput();autoTitle(chat,question);chat.messages.push({who:"user",text:question,links:[]});
 busy=true;sendButton.disabled=true;renderAll();
 try{
  const response=await fetch("/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question,history:chat.apiHistory})});
  const data=await response.json();if(!response.ok)throw Error(data.error||"Request failed");
  chat.messages.push({who:"bot",text:data.answer||"Sorry, I couldn't find an answer.",links:Array.isArray(data.links)?data.links:[]});
  if(Array.isArray(data.history))chat.apiHistory=data.history;saveChats();renderAll();if(voiceEnabled)speak(data.answer||"")
 }catch(e){chat.messages.push({who:"bot",text:"I couldn't reach the answer service. Check the connection and try again.",links:[]});renderAll();showToast("Connection problem. Try again.")}
 finally{busy=false;sendButton.disabled=false;renderAll();questionBox.focus()}
}
function speak(text){if(!("speechSynthesis"in window))return showToast("Spoken replies aren't supported in this browser.");speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.lang=detectSpeechLanguage(text);speechSynthesis.speak(u)}
function detectSpeechLanguage(t){if(/[ñ¿¡áéíóú]/i.test(t))return"es-ES";if(/[àâçéèêëîïôûùüÿœ]/i.test(t))return"fr-FR";return"en-US"}
function toggleVoice(){voiceEnabled=!voiceEnabled;localStorage.setItem(VOICE_KEY,String(voiceEnabled));if(!voiceEnabled&&"speechSynthesis"in window)speechSynthesis.cancel();renderAll();showToast(voiceEnabled?"Spoken replies enabled.":"Spoken replies disabled.")}
function startMic(){
 const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR)return showToast("Voice input works in supported browsers such as Chrome or Edge.");
 if(recognition){recognition.stop();recognition=null;$("micBtn").classList.remove("active");return}
 recognition=new SR();recognition.lang="en-US";recognition.continuous=false;recognition.interimResults=true;$("micBtn").classList.add("active");let finalText="";
 recognition.onresult=e=>{let interim="";for(let i=e.resultIndex;i<e.results.length;i++){const t=e.results[i][0].transcript;if(e.results[i].isFinal)finalText+=t;else interim+=t}questionBox.value=(finalText+" "+interim).trim();resizeInput()};
 recognition.onerror=e=>showToast(e.error==="not-allowed"?"Allow microphone access in your browser settings.":"Couldn't hear that. Try again.");
 recognition.onend=()=>{$("micBtn").classList.remove("active");recognition=null};
 try{recognition.start()}catch(e){recognition=null;$("micBtn").classList.remove("active");showToast("Microphone couldn't start. Try again.")}
}
function insertPrompt(text){questionBox.value=text;questionBox.focus();resizeInput()}
$("form").addEventListener("submit",e=>{e.preventDefault();sendMessage()});
questionBox.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();sendMessage()}});
questionBox.addEventListener("input",resizeInput);
$("newChat").onclick=createNewChat;$("renameBtn").onclick=renameChat;$("voiceToggle").onclick=toggleVoice;$("micBtn").onclick=startMic;$("historySearch").oninput=renderChats;
$("menuBtn").onclick=()=>$("sidebar").classList.toggle("open");
$("galaxyToggle").onclick=()=>{galaxyEnabled=!galaxyEnabled;localStorage.setItem(GALAXY_KEY,String(galaxyEnabled));renderAll()};
$("voiceAction").onclick=startMic;$("listenAction").onclick=toggleVoice;
$("webBtn").onclick=()=>insertPrompt("Search the web for ");$("mathBtn").onclick=()=>insertPrompt("Calculate ");$("translateBtn").onclick=()=>insertPrompt("Translate ");
$("fullscreenBtn").onclick=async()=>{try{if(!document.fullscreenElement)await document.documentElement.requestFullscreen();else await document.exitFullscreen()}catch(e){showToast("Fullscreen isn't available in this browser.")}};
document.querySelectorAll(".action-item[data-prompt]").forEach(b=>b.onclick=()=>insertPrompt(b.dataset.prompt));
loadChats();renderAll();
</script>
</body>
</html>
"""


# =========================================================
# NETWORK HELPERS
# =========================================================

def fetch_text(url, timeout=15, headers=None, data=None):
    default_headers = {"User-Agent": "NyvexiaAI/7.0"}
    if headers:
        default_headers.update(headers)
    req = urllib.request.Request(url, headers=default_headers, data=data)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def normalize(text):
    text = unicodedata.normalize("NFKC", str(text or "")).lower().strip()
    return re.sub(r"\s+", " ", text).rstrip("?!., ")


# =========================================================
# REAL CONVERSATIONAL AI — GROQ API
# Configure GROQ_API_KEY in Render Environment.
# =========================================================

AI_URL = "https://api.groq.com/openai/v1/chat/completions"
AI_MODEL = os.environ.get("NYVEXIA_MODEL", "llama-3.3-70b-versatile")

SYSTEM_PROMPT = """
You are Nyvexia AI, a helpful, intelligent, friendly conversational assistant.
Your goal is to understand what the user actually wants and answer that request.

CORE RULES:
- Talk naturally, like a real assistant. Greetings get a short friendly greeting.
- If asked your name, say your name is Nyvexia AI. Do not search the web for this.
- Answer the actual question directly. Do not turn every message into a web search.
- Match the user's language. If they write French, answer in natural French.
  If they write English, answer in English. Adapt if they switch languages.
- Be concise by default. Give more detail when requested or when the task needs it.
- Use clear headings and lists when they improve readability, not automatically.
- Remember the conversation context supplied in previous messages. If the user says
  "explain that", "make it shorter", "continue", or "write it differently", use context.
- Ask a short clarifying question only when the request truly cannot be answered
  without clarification. Otherwise make a sensible assumption and help.
- Never claim you searched the web unless search results were provided to you.
- Never invent citations, sources, facts, or actions you did not perform.
- If search results are provided, use them as evidence, explain the answer in your
  own words, and cite relevant source URLs in the links field returned by the app.
- If search results are insufficient, say what is uncertain instead of making things up.
- For school assignments, follow the requested grade and language. "Secondary 3"
  means Quebec Secondary 3: use age-appropriate vocabulary, organized paragraphs,
  and the requested length. If asked to write a text, WRITE THE TEXT; do not return
  random encyclopedia snippets. Add an introduction, development, and conclusion
  when suitable. Do not assume a topic if the user supplied one.
- For math, explain steps if requested. Check calculations carefully.
- For casual chat, be warm and natural without turning every answer into a lecture.
- Be honest about limitations. You are Nyvexia AI, not ChatGPT or Gemini.
"""


def groq_chat(question, history, search_results=None):
    api_key = os.environ.get("GROQ_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Nyvexia's AI brain isn't connected yet. Add your GROQ_API_KEY "
            "in Render → Environment, then redeploy."
        )

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Keep recent conversation context, excluding malformed entries.
    for item in history[-12:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role in ("user", "assistant") and isinstance(content, str) and content.strip():
            messages.append({"role": role, "content": content[:7000]})

    if search_results:
        evidence = []
        for item in search_results[:6]:
            evidence.append(
                "TITLE: " + item.get("title", "") +
                "\nSNIPPET: " + item.get("snippet", "") +
                "\nURL: " + item.get("url", "")
            )
        messages.append({
            "role": "system",
            "content": (
                "The user explicitly requested web research. Use the following "
                "retrieved search results as evidence, distinguish facts from "
                "uncertainty, and do not claim the snippets prove more than they do:\n\n"
                + "\n\n".join(evidence)
            )
        })

    messages.append({"role": "user", "content": question[:12000]})

    payload = json.dumps({
        "model": AI_MODEL,
        "messages": messages,
        "temperature": 0.55,
        "max_tokens": 1800
    }).encode("utf-8")

    raw = fetch_text(
        AI_URL,
        timeout=45,
        headers={
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json"
        },
        data=payload
    )
    data = json.loads(raw)
    choices = data.get("choices", [])
    if not choices:
        raise RuntimeError("The AI service returned no answer.")
    answer = choices[0].get("message", {}).get("content", "")
    if isinstance(answer, list):
        answer = "\n".join(
            part.get("text", "") for part in answer if isinstance(part, dict)
        )
    answer = str(answer).strip()
    if not answer:
        raise RuntimeError("The AI service returned an empty answer.")
    return answer


# =========================================================
# TRANSLATION
# =========================================================

def translate_text(text, target, source="auto"):
    target_codes = {
        "english":"en","anglais":"en","en":"en",
        "french":"fr","français":"fr","francais":"fr","fr":"fr",
        "spanish":"es","español":"es","espagnol":"es","es":"es",
        "german":"de","allemand":"de","deutsch":"de","de":"de",
        "italian":"it","italien":"it","italiano":"it","it":"it",
        "portuguese":"pt","portugais":"pt","português":"pt","pt":"pt",
        "japanese":"ja","japonais":"ja","日本語":"ja","ja":"ja",
        "chinese":"zh-CN","chinois":"zh-CN","中文":"zh-CN",
        "arabic":"ar","arabe":"ar","العربية":"ar",
        "korean":"ko","coréen":"ko","한국어":"ko",
        "hindi":"hi","हिन्दी":"hi",
        "russian":"ru","russe":"ru","русский":"ru"
    }
    tgt = target_codes.get(target.lower().strip(), target.strip())
    src = "en" if source == "auto" else target_codes.get(source.lower().strip(), source.strip())
    query = urllib.parse.urlencode({"q": text[:450], "langpair": src + "|" + tgt})
    data = json.loads(fetch_text("https://api.mymemory.translated.net/get?" + query))
    translated = html.unescape(data.get("responseData", {}).get("translatedText", ""))
    if not translated or data.get("responseStatus") not in (200, "200"):
        raise ValueError("Translation service did not return a translation.")
    return translated


def extract_translation_request(question):
    patterns = [
        r"(?is)^\s*translate\s+(.+?)\s+(?:into|to|in)\s+([a-zA-ZÀ-ÿ\u4e00-\u9fff -]+)[.!?]*\s*$",
        r"(?is)^\s*traduis\s+(.+?)\s+(?:en|vers)\s+([a-zA-ZÀ-ÿ -]+)[.!?]*\s*$",
        r"(?is)^\s*traduce\s+(.+?)\s+(?:al|a|en)\s+([a-zA-ZÀ-ÿ -]+)[.!?]*\s*$"
    ]
    for pattern in patterns:
        match = re.match(pattern, question)
        if match:
            return match.group(1).strip(" '\""), match.group(2).strip(" .?!")
    return None


# =========================================================
# MATH
# =========================================================

def safe_calculate(expression):
    expression = expression.replace("×", "*").replace("÷", "/").replace("^", "**")
    expression = expression.replace(",", "")
    tree = ast.parse(expression, mode="eval")
    binary_ops = {
        ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.Pow: operator.pow, ast.Mod: operator.mod,
        ast.FloorDiv: operator.floordiv
    }
    unary_ops = {ast.UAdd: operator.pos, ast.USub: operator.neg}

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in binary_ops:
            left, right = visit(node.left), visit(node.right)
            if isinstance(node.op, ast.Pow) and abs(right) > 8:
                raise ValueError("Exponent is too large.")
            result = binary_ops[type(node.op)](left, right)
            if not math.isfinite(float(result)) or abs(result) > 1e100:
                raise ValueError("Result is too large.")
            return result
        if isinstance(node, ast.UnaryOp) and type(node.op) in unary_ops:
            return unary_ops[type(node.op)](visit(node.operand))
        raise ValueError("Unsupported arithmetic expression.")
    return visit(tree)


def math_answer(question):
    q = question.strip()
    eq = re.fullmatch(
        r"\s*(-?\d+(?:\.\d+)?)\s*\*?\s*x\s*([+-]\s*\d+(?:\.\d+)?)?\s*=\s*(-?\d+(?:\.\d+)?)\s*",
        q, re.I
    )
    if eq:
        a = float(eq.group(1))
        b = float((eq.group(2) or "0").replace(" ", ""))
        c = float(eq.group(3))
        if a == 0:
            return "This equation has no unique solution because the coefficient of x is 0.", []
        x = (c - b) / a
        return (
            f"Let's solve it step by step:\n\n{a:g}x {b:+g} = {c:g}\n"
            f"Subtract {b:g} from both sides: {a:g}x = {c-b:g}\n"
            f"Divide both sides by {a:g}: x = {x:g}\n\nAnswer: x = {x:g}", []
        )
    cleaned = re.sub(r"^(what is|what's|calculate|compute|evaluate)\s+", "", q, flags=re.I).strip().rstrip("?=")
    cleaned = cleaned.replace("²", "**2").replace("³", "**3")
    if not re.fullmatch(r"[\d\s.+\-*/()%^×÷,]+", cleaned):
        return None
    try:
        result = safe_calculate(cleaned)
        shown = str(int(result)) if isinstance(result, float) and result.is_integer() else f"{result:.10g}" if isinstance(result, float) else str(result)
        return f"{cleaned} = {shown}", []
    except ZeroDivisionError:
        return "You can't divide by zero.", []
    except Exception:
        return None


# =========================================================
# WEB SEARCH — ONLY WHEN THE USER ASKS FOR IT
# =========================================================

def wants_web_search(question):
    q = normalize(question)
    phrases = [
        "search the web", "search online", "look up", "find sources",
        "give me sources", "source links", "web search", "on the internet",
        "sur internet", "cherche sur le web", "recherche sur internet",
        "cherche des sources", "donne-moi des sources", "donne moi des sources",
        "dernières nouvelles", "dernieres nouvelles", "actualités", "actualites",
        "latest news", "current news", "today's news", "news today",
        "right now", "as of today", "latest information", "recent updates",
        "what happened today", "this week", "cette semaine", "aujourd'hui",
        "aujourd’hui", "en ce moment", "prix actuel", "current price"
    ]
    return any(p in q for p in phrases)


def web_search(question, limit=5):
    url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": question})
    page = fetch_text(url, timeout=15)
    blocks = re.findall(r'(?is)<div[^>]+class="result[^"]*"[^>]*>(.*?)</div>\s*</div>', page)
    results = []
    for block in blocks:
        link_match = re.search(r'(?is)<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', block)
        if not link_match:
            continue
        url_value = html.unescape(link_match.group(1))
        title = re.sub(r"<.*?>", "", html.unescape(link_match.group(2)))
        title = re.sub(r"\s+", " ", title).strip()
        snippet_match = re.search(r'(?is)class="result__snippet"[^>]*>(.*?)</', block)
        snippet = re.sub(r"<.*?>", "", html.unescape(snippet_match.group(1))) if snippet_match else ""
        snippet = re.sub(r"\s+", " ", snippet).strip()
        if "uddg=" in url_value:
            try:
                url_value = urllib.parse.parse_qs(urllib.parse.urlparse(url_value).query).get("uddg", [url_value])[0]
            except Exception:
                pass
        if url_value.startswith("http") and title:
            results.append({"title": title[:180], "url": url_value, "snippet": snippet[:500]})
        if len(results) >= limit:
            break
    return results


# =========================================================
# INTELLIGENT ANSWER ROUTER
# =========================================================

def answer_question(question, history):
    q = normalize(question)

    # Fast, reliable greetings and identity answers.
    greetings = {
        "hi", "hello", "hey", "heyy", "yo", "sup", "bonjour",
        "salut", "coucou", "allo", "allô", "bonsoir", "good morning",
        "good afternoon", "good evening"
    }
    if q in greetings:
        return ("Salut ! 💜 Qu'est-ce que tu veux faire aujourd'hui ?" if any(
            c in q for c in "àâçéèêëîïôûùüÿ"
        ) or q in {"bonjour", "salut", "coucou", "allo", "allô", "bonsoir"}
        else "Hey! 💜 What can I help you with today?"), []

    if q in {"thanks", "thank you", "thx", "ty", "thank u", "merci", "merci beaucoup"}:
        return ("De rien ! 💜" if q.startswith("merci") else "You're welcome! 💜"), []

    if q in {
        "who are you", "what are you", "what is your name", "whats your name",
        "what's your name", "ton nom", "quel est ton nom", "comment tu t'appelles",
        "qui es-tu", "qui es tu", "c'est quoi ton nom", "tu t'appelles comment"
    }:
        return "Je suis Nyvexia AI 💜, ton assistant conversationnel. Je peux discuter avec toi, expliquer des sujets, aider pour l'école, écrire des textes, résoudre des problèmes et chercher des informations.", []

    # Preserve dedicated translation and math tools.
    translation = extract_translation_request(question)
    if translation:
        try:
            translated = translate_text(translation[0], translation[1])
            return f"Translation into {translation[1]}:\n{translated}", []
        except Exception:
            # Let the AI translate if the external translation service is unavailable.
            pass

    math_result = math_answer(question)
    if math_result is not None:
        return math_result

    # Search only when the user explicitly asks for research or fresh information.
    results = []
    if wants_web_search(question):
        try:
            results = web_search(question, 5)
        except Exception:
            results = []

    # The AI handles ordinary questions, writing, explanations, and conversation.
    try:
        answer = groq_chat(question, history, results if results else None)
        links = [
            {"title": item["title"], "url": item["url"]}
            for item in results if item.get("url", "").startswith("http")
        ]
        if wants_web_search(question) and not results:
            answer += "\n\nNote: I couldn't retrieve web search results this time, so I answered using my existing knowledge."
        return answer, links

    except Exception as e:
        print("Nyvexia AI error:", repr(e))
        if "GROQ_API_KEY" in str(e):
            return (
                "⚙️ Nyvexia's AI brain isn't connected yet.\n\n"
                "To activate real conversations, add your GROQ_API_KEY in "
                "Render → your service → Environment, then redeploy."
            ), []
        return (
            "I couldn't reach my AI service just now. Please try again in a moment. "
            "If this keeps happening, check that the GROQ_API_KEY is valid in Render "
            "and that the service has redeployed."
        ), []


# =========================================================
# FLASK ROUTES — PRESERVE / AND /ASK
# =========================================================

@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_PAGE)


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        question = str(data.get("question", "")).strip()
        history = data.get("history", [])

        if not question:
            return jsonify({
                "answer": "Type a question first and I'll do my best to help.",
                "links": [],
                "history": history if isinstance(history, list) else []
            })

        if not isinstance(history, list):
            history = []

        history = [
            item for item in history[-12:]
            if isinstance(item, dict)
            and item.get("role") in ("user", "assistant")
            and isinstance(item.get("content"), str)
        ]

        answer, links = answer_question(question, history)

        updated_history = (
            history + [
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ]
        )[-12:]

        return jsonify({
            "answer": answer,
            "links": links,
            "history": updated_history
        })

    except Exception as e:
        print("Nyvexia /ask error:", repr(e))
        return jsonify({
            "answer": "Something went wrong while processing that message. Please try again.",
            "links": [],
            "history": []
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
