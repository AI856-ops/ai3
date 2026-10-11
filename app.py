from flask import Flask, request, jsonify, render_template_string
import urllib.request
import urllib.parse
import json
import html
import re
import random
import uuid

app = Flask(__name__)

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nyvexia IA</title>
<style>
:root {
  --purple: #8B5CF6;
  --cyan: #22D3EE;
  --pink: #F472B6;
  --background: #101426;
  --panel: #151a30;
  --panel-light: #1b2139;
  --text: #F8FAFF;
  --muted: #9aa5c0;
  --border: rgba(180,190,230,.12);
}
* { box-sizing: border-box; }
body {
  margin: 0;
  height: 100vh;
  overflow: hidden;
  color: var(--text);
  background: var(--background);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
button, input { font: inherit; }
button { cursor: pointer; }
.app { display: flex; width: 100%; height: 100vh; }
.sidebar {
  width: 270px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  padding: 20px 14px;
  background: #0d1121;
  border-right: 1px solid var(--border);
}
.brand { display: flex; align-items: center; gap: 11px; padding: 4px 8px 24px; }
.logo {
  width: 39px; height: 39px; border-radius: 13px;
  display: grid; place-items: center;
  background: linear-gradient(145deg, var(--purple), #5b5bd6 55%, #278fae);
  font-weight: 800; font-size: 19px;
  box-shadow: 0 5px 18px rgba(139,92,246,.18);
}
.brand-name { font-size: 17px; font-weight: 750; letter-spacing: -.4px; }
.brand-sub { font-size: 10px; color: var(--muted); letter-spacing: 1.6px; margin-top: 3px; }
.new-chat {
  border: 1px solid rgba(139,92,246,.36);
  background: rgba(139,92,246,.12);
  color: var(--text);
  border-radius: 11px;
  padding: 12px 13px;
  text-align: left;
  transition: .18s ease;
}
.new-chat:hover { background: rgba(139,92,246,.22); border-color: var(--purple); }
.search-wrap { margin: 15px 0 17px; position: relative; }
.search-wrap input {
  width: 100%; padding: 10px 12px 10px 34px;
  color: var(--text); background: #151a2d;
  border: 1px solid var(--border); border-radius: 10px; outline: none;
}
.search-wrap input:focus { border-color: rgba(139,92,246,.7); }
.search-icon { position: absolute; left: 12px; top: 10px; color: var(--muted); }
.section-label {
  padding: 0 8px 9px; color: #77829f;
  font-size: 10px; font-weight: 700; letter-spacing: 1.5px;
}
.chat-list { overflow-y: auto; flex: 1; }
.chat-item {
  display: flex; align-items: center; gap: 8px;
  padding: 10px 9px; border-radius: 9px; margin-bottom: 3px;
  color: #bdc6dc; font-size: 13px; cursor: pointer;
}
.chat-item:hover { background: rgba(255,255,255,.045); }
.chat-item.active { background: rgba(139,92,246,.15); color: white; }
.chat-title { flex: 1; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.chat-icon { color: #8994b2; font-size: 14px; }
.delete-chat { border: 0; background: transparent; color: #8b94ad; padding: 2px 4px; opacity: 0; }
.chat-item:hover .delete-chat { opacity: 1; }
.delete-chat:hover { color: #fb7185; }
.sidebar-bottom {
  border-top: 1px solid var(--border); margin-top: 12px; padding: 14px 7px 0;
  color: #7e8aa7; font-size: 11px; line-height: 1.6;
}
.status-dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #34d399; margin-right: 6px; }
.main { min-width: 0; flex: 1; display: flex; flex-direction: column; position: relative; }
.topbar {
  height: 68px; flex-shrink: 0; display: flex; align-items: center;
  justify-content: space-between; padding: 0 26px;
  border-bottom: 1px solid var(--border); background: rgba(16,20,38,.86);
}
.current-title { font-size: 13px; color: #d8def0; font-weight: 600; }
.top-actions { display: flex; align-items: center; gap: 8px; }
.small-btn {
  border: 1px solid var(--border); background: #171c31; color: #d9e0f2;
  padding: 8px 11px; border-radius: 9px; font-size: 12px;
}
.small-btn:hover { border-color: rgba(139,92,246,.6); }
.mobile-menu { display: none; }
.messages {
  flex: 1; overflow-y: auto; padding: 32px 20px 28px;
  scroll-behavior: smooth;
}
.message-list { width: 100%; max-width: 790px; margin: 0 auto; }
.welcome { padding: 8vh 0 26px; text-align: center; }
.welcome-mark {
  width: 68px; height: 68px; border-radius: 22px; margin: 0 auto 23px;
  display: grid; place-items: center; font-size: 29px; font-weight: 800;
  background: linear-gradient(145deg, rgba(139,92,246,.25), rgba(34,211,238,.1));
  border: 1px solid rgba(139,92,246,.32); color: #d9d0ff;
}
.welcome h1 { font-size: clamp(28px,4vw,40px); letter-spacing: -1.6px; margin: 0 0 12px; }
.welcome h1 span {
  background: linear-gradient(100deg, #b9a5ff, #73e6f2);
  -webkit-background-clip: text; background-clip: text; color: transparent;
}
.welcome p { color: var(--muted); font-size: 14px; line-height: 1.7; max-width: 440px; margin: 0 auto; }
.suggestions {
  display: grid; grid-template-columns: repeat(2,minmax(0,1fr));
  gap: 10px; margin: 28px auto 0; max-width: 570px;
}
.suggestion {
  padding: 13px 14px; text-align: left; border-radius: 12px;
  background: rgba(255,255,255,.025); border: 1px solid var(--border);
  color: #d9e0f2; font-size: 12px; transition: .18s ease;
}
.suggestion:hover { background: rgba(139,92,246,.09); border-color: rgba(139,92,246,.45); }
.suggestion span { display: block; color: #8792af; font-size: 11px; margin-top: 5px; }
.message { display: flex; gap: 13px; margin: 0 0 26px; align-items: flex-start; }
.avatar {
  flex-shrink: 0; width: 31px; height: 31px; border-radius: 10px;
  display: grid; place-items: center; font-size: 12px; font-weight: 800;
}
.avatar.user { background: #303954; color: #e2e8f8; }
.avatar.bot { background: linear-gradient(145deg, var(--purple), #397cba); color: white; }
.message-body { min-width: 0; flex: 1; padding-top: 4px; }
.message-name { font-size: 11px; color: #8f9bb7; margin-bottom: 8px; font-weight: 650; }
.message-text { color: #e4e9f6; font-size: 14px; line-height: 1.8; white-space: pre-wrap; overflow-wrap: anywhere; }
.message-text a { color: #7ddcf0; }
.sources { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 12px; }
.source-link {
  font-size: 11px; color: #bcb0ff; text-decoration: none;
  border: 1px solid rgba(139,92,246,.24); border-radius: 7px;
  padding: 6px 9px; background: rgba(139,92,246,.07);
}
.source-link:hover { border-color: var(--purple); }
.composer-area { padding: 8px 20px 18px; flex-shrink: 0; }
.composer-wrap { max-width: 790px; margin: 0 auto; }
.composer {
  display: flex; align-items: flex-end; gap: 9px; padding: 10px;
  border-radius: 16px; border: 1px solid rgba(170,180,220,.19);
  background: #171c30; box-shadow: 0 10px 35px rgba(0,0,0,.12);
}
.composer:focus-within { border-color: rgba(139,92,246,.65); }
#question {
  flex: 1; min-width: 0; resize: none; max-height: 140px;
  border: 0; outline: none; background: transparent; color: var(--text);
  font-size: 14px; line-height: 1.55; padding: 8px 5px;
}
#question::placeholder { color: #7985a2; }
.icon-btn {
  width: 37px; height: 37px; flex-shrink: 0; display: grid; place-items: center;
  border-radius: 10px; background: transparent; border: 1px solid transparent;
  color: #9aa6c3; font-size: 16px;
}
.icon-btn:hover { background: rgba(255,255,255,.06); color: white; }
.icon-btn.active { color: var(--cyan); background: rgba(34,211,238,.1); }
.send-btn {
  width: 38px; height: 38px; border: 0; border-radius: 11px;
  background: linear-gradient(135deg, var(--purple), #6475df);
  color: white; font-size: 18px; transition: .18s ease;
}
.send-btn:hover { filter: brightness(1.12); transform: translateY(-1px); }
.send-btn:disabled { opacity: .45; cursor: not-allowed; transform: none; }
.disclaimer { text-align: center; color: #77829d; font-size: 10px; margin-top: 11px; }
.typing { display: inline-flex; gap: 4px; padding: 5px 0; }
.typing span { width: 5px; height: 5px; background: #a79aff; border-radius: 50%; animation: pulse 1s infinite alternate; }
.typing span:nth-child(2) { animation-delay: .2s; }
.typing span:nth-child(3) { animation-delay: .4s; }
@keyframes pulse { from { opacity: .25; transform: translateY(0); } to { opacity: 1; transform: translateY(-3px); } }
.toast {
  position: fixed; bottom: 92px; left: 50%; transform: translateX(-50%);
  background: #222941; border: 1px solid var(--border); color: #e9edfa;
  padding: 10px 15px; border-radius: 10px; font-size: 12px;
  display: none; z-index: 10; box-shadow: 0 8px 30px #0004;
}
@media (max-width: 720px) {
  .sidebar { position: fixed; z-index: 20; top: 0; bottom: 0; left: 0; transform: translateX(-105%); transition: transform .22s ease; box-shadow: 12px 0 40px #0005; }
  .sidebar.open { transform: translateX(0); }
  .mobile-menu { display: inline-grid; }
  .topbar { height: 60px; padding: 0 13px; gap: 10px; }
  .top-actions { gap: 5px; }
  .small-btn { padding: 7px 8px; font-size: 11px; }
  .messages { padding: 20px 14px; }
  .welcome { padding-top: 7vh; }
  .suggestions { grid-template-columns: 1fr; margin-top: 22px; }
  .composer-area { padding: 6px 12px 12px; }
  .message { gap: 9px; }
}
</style>
</head>
<body>
<div class="app">
  <aside class="sidebar" id="sidebar">
    <div class="brand">
      <div class="logo">N</div>
      <div><div class="brand-name">NYVEXIA IA</div><div class="brand-sub">YOUR THINKING SPACE</div></div>
    </div>
    <button class="new-chat" id="newChat">＋ &nbsp; New conversation</button>
    <div class="search-wrap">
      <span class="search-icon">⌕</span>
      <input id="historySearch" type="text" placeholder="Search conversations..." autocomplete="off">
    </div>
    <div class="section-label">YOUR CONVERSATIONS</div>
    <div class="chat-list" id="chatList"></div>
    <div class="sidebar-bottom"><span class="status-dot"></span>Nyvexia is ready<br>Chats are saved in this browser.</div>
  </aside>

  <main class="main">
    <header class="topbar">
      <div style="display:flex;align-items:center;gap:10px;min-width:0">
        <button class="small-btn mobile-menu" id="menuBtn" aria-label="Open menu">☰</button>
        <div class="current-title" id="currentTitle">New conversation</div>
      </div>
      <div class="top-actions">
        <button class="small-btn" id="renameBtn">Rename</button>
        <button class="small-btn" id="voiceToggle" title="Toggle spoken replies">Voice: Off</button>
      </div>
    </header>

    <section class="messages" id="messages">
      <div class="message-list" id="messageList"></div>
    </section>

    <div class="composer-area">
      <div class="composer-wrap">
        <form class="composer" id="form">
          <button class="icon-btn" type="button" id="micBtn" title="Speak your message" aria-label="Use microphone">♩</button>
          <textarea id="question" rows="1" placeholder="Ask Nyvexia anything..." autocomplete="off"></textarea>
          <button class="send-btn" id="send" type="submit" aria-label="Send message">↑</button>
        </form>
        <div class="disclaimer">Nyvexia uses Wikipedia for many factual answers. Always double-check important information.</div>
      </div>
    </div>
  </main>
</div>
<div class="toast" id="toast"></div>

<script>
const STORAGE_KEY = "nyvexia_galaxy_chats_v1";
const VOICE_KEY = "nyvexia_voice_enabled_v1";
const welcomeMessage = {
  who: "bot",
  text: "Hey! Welcome to Nyvexia IA. Ask me a question, explore a topic, or just chat with me.",
  links: []
};

let chats = [];
let activeId = null;
let busy = false;
let voiceEnabled = localStorage.getItem(VOICE_KEY) === "true";
let recognition = null;
let toastTimer = null;

const $ = id => document.getElementById(id);
const messagesBox = $("messages");
const messageList = $("messageList");
const questionBox = $("question");
const sendButton = $("send");

function makeChat() {
  return {
    id: (crypto.randomUUID ? crypto.randomUUID() : String(Date.now()) + Math.random()),
    title: "New conversation",
    messages: [{...welcomeMessage}],
    apiHistory: [],
    created: Date.now()
  };
}

function loadChats() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    if (Array.isArray(saved)) {
      chats = saved.filter(c => c && c.id && Array.isArray(c.messages)).map(c => ({
        id: c.id,
        title: c.title || "New conversation",
        messages: c.messages,
        apiHistory: Array.isArray(c.apiHistory) ? c.apiHistory : [],
        created: c.created || Date.now()
      }));
    }
  } catch (e) {
    chats = [];
  }
  if (!chats.length) chats = [makeChat()];
  activeId = chats[0].id;
  saveChats();
}

function saveChats() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(chats));
  } catch (e) {
    showToast("Could not save chats in this browser.");
  }
}

function activeChat() {
  return chats.find(c => c.id === activeId) || chats[0];
}

function showToast(text) {
  const el = $("toast");
  el.textContent = text;
  el.style.display = "block";
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { el.style.display = "none"; }, 2600);
}

function escapeHTML(text) {
  return String(text).replace(/[&<>"']/g, ch => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  }[ch]));
}

function renderChats() {
  const term = $("historySearch").value.trim().toLowerCase();
  const list = $("chatList");
  list.innerHTML = "";
  const filtered = [...chats].sort((a,b) => (b.created || 0) - (a.created || 0)).filter(chat => {
    if (!term) return true;
    return chat.title.toLowerCase().includes(term) ||
      chat.messages.some(m => String(m.text || "").toLowerCase().includes(term));
  });

  if (!filtered.length) {
    list.innerHTML = '<div style="padding:12px 8px;color:#7e8aa7;font-size:12px">No matching conversations.</div>';
    return;
  }

  filtered.forEach(chat => {
    const item = document.createElement("div");
    item.className = "chat-item" + (chat.id === activeId ? " active" : "");
    const title = document.createElement("span");
    title.className = "chat-title";
    title.textContent = chat.title || "New conversation";
    const icon = document.createElement("span");
    icon.className = "chat-icon";
    icon.textContent = "◷";
    const del = document.createElement("button");
    del.className = "delete-chat";
    del.type = "button";
    del.title = "Delete conversation";
    del.textContent = "×";
    del.addEventListener("click", e => {
      e.stopPropagation();
      deleteChat(chat.id);
    });
    item.append(icon, title, del);
    item.addEventListener("click", () => {
      activeId = chat.id;
      renderAll();
      if (window.innerWidth <= 720) $("sidebar").classList.remove("open");
    });
    list.appendChild(item);
  });
}

function welcomeHTML() {
  return `
    <div class="welcome">
      <div class="welcome-mark">N</div>
      <h1>Meet <span>Nyvexia IA.</span></h1>
      <p>A space to ask questions, discover ideas, and explore what you're curious about.</p>
      <div class="suggestions">
        <button class="suggestion" data-prompt="What is artificial intelligence?">Explain a big idea<span>Understand AI in simple terms</span></button>
        <button class="suggestion" data-prompt="What is the capital of Italy?">Find a quick answer<span>Get a fact about the world</span></button>
        <button class="suggestion" data-prompt="Tell me an interesting space fact.">Explore something new<span>Discover a fact about space</span></button>
        <button class="suggestion" data-prompt="Give me a fun math challenge.">Challenge yourself<span>Try a little brain teaser</span></button>
      </div>
    </div>`;
}

function renderMessages() {
  const chat = activeChat();
  if (!chat) return;
  $("currentTitle").textContent = chat.title || "New conversation";
  messageList.innerHTML = "";

  const onlyWelcome = chat.messages.length === 1 &&
    chat.messages[0].who === "bot" &&
    chat.messages[0].text === welcomeMessage.text;

  if (onlyWelcome) {
    messageList.innerHTML = welcomeHTML();
    messageList.querySelectorAll("[data-prompt]").forEach(btn => {
      btn.addEventListener("click", () => {
        questionBox.value = btn.getAttribute("data-prompt");
        questionBox.focus();
        resizeInput();
      });
    });
    return;
  }

  chat.messages.forEach(msg => {
    const row = document.createElement("div");
    row.className = "message";
    const avatar = document.createElement("div");
    avatar.className = "avatar " + (msg.who === "user" ? "user" : "bot");
    avatar.textContent = msg.who === "user" ? "Y" : "N";
    const body = document.createElement("div");
    body.className = "message-body";
    const name = document.createElement("div");
    name.className = "message-name";
    name.textContent = msg.who === "user" ? "You" : "Nyvexia";
    const content = document.createElement("div");
    content.className = "message-text";
    content.textContent = msg.text || "";
    body.append(name, content);

    if (msg.who !== "user" && Array.isArray(msg.links) && msg.links.length) {
      const links = document.createElement("div");
      links.className = "sources";
      msg.links.forEach(link => {
        if (!link || !link.url || !/^https?:\/\//i.test(link.url)) return;
        const a = document.createElement("a");
        a.className = "source-link";
        a.href = link.url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = link.title || "Source";
        links.appendChild(a);
      });
      body.appendChild(links);
    }
    row.append(avatar, body);
    messageList.appendChild(row);
  });

  if (busy) {
    const row = document.createElement("div");
    row.className = "message";
    row.innerHTML = '<div class="avatar bot">N</div><div class="message-body"><div class="message-name">Nyvexia</div><div class="typing"><span></span><span></span><span></span></div></div>';
    messageList.appendChild(row);
  }
}

function renderAll() {
  renderChats();
  renderMessages();
  saveChats();
  messagesBox.scrollTop = messagesBox.scrollHeight;
  $("voiceToggle").textContent = "Voice: " + (voiceEnabled ? "On" : "Off");
  $("voiceToggle").classList.toggle("active", voiceEnabled);
}

function createNewChat() {
  const chat = makeChat();
  chats.unshift(chat);
  activeId = chat.id;
  questionBox.value = "";
  renderAll();
  questionBox.focus();
  if (window.innerWidth <= 720) $("sidebar").classList.remove("open");
}

function deleteChat(id) {
  const chat = chats.find(c => c.id === id);
  if (!chat) return;
  if (!confirm('Delete "' + (chat.title || "New conversation") + '"?')) return;
  chats = chats.filter(c => c.id !== id);
  if (!chats.length) chats.push(makeChat());
  if (activeId === id) activeId = chats[0].id;
  renderAll();
}

function renameChat() {
  const chat = activeChat();
  if (!chat) return;
  const next = prompt("Rename this conversation:", chat.title || "New conversation");
  if (next === null) return;
  const cleaned = next.trim().slice(0, 70);
  if (!cleaned) {
    showToast("The title can't be empty.");
    return;
  }
  chat.title = cleaned;
  renderAll();
}

function autoTitle(chat, text) {
  if (!chat || chat.title !== "New conversation") return;
  const cleaned = text.replace(/\s+/g, " ").trim();
  chat.title = cleaned.length > 34 ? cleaned.slice(0, 31) + "..." : cleaned;
}

function addMessage(who, text, links = []) {
  const chat = activeChat();
  chat.messages.push({who, text, links});
  saveChats();
  renderAll();
}

function resizeInput() {
  questionBox.style.height = "auto";
  questionBox.style.height = Math.min(questionBox.scrollHeight, 140) + "px";
}

async function sendMessage(textOverride) {
  if (busy) return;
  const question = (typeof textOverride === "string" ? textOverride : questionBox.value).trim();
  if (!question) return;
  const chat = activeChat();
  if (!chat) return;

  questionBox.value = "";
  resizeInput();
  autoTitle(chat, question);
  addMessage("user", question);
  busy = true;
  sendButton.disabled = true;
  renderAll();

  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        question: question,
        history: chat.apiHistory
      })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Request failed");
    const answer = data.answer || "Sorry, I couldn't find an answer.";
    const links = Array.isArray(data.links) ? data.links : [];
    if (Array.isArray(data.history)) chat.apiHistory = data.history;
    chat.messages.push({who: "bot", text: answer, links});
    saveChats();
    renderAll();
    if (voiceEnabled) speak(answer);
  } catch (error) {
    const message = "I couldn't reach my answer service right now. Please try again in a moment.";
    chat.messages.push({who: "bot", text: message, links: []});
    saveChats();
    renderAll();
    showToast("Connection problem. Try again.");
  } finally {
    busy = false;
    sendButton.disabled = false;
    renderAll();
    questionBox.focus();
  }
}

function speak(text) {
  if (!("speechSynthesis" in window)) {
    showToast("Spoken replies aren't supported in this browser.");
    return;
  }
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = "en-US";
  utterance.rate = 1;
  window.speechSynthesis.speak(utterance);
}

function toggleVoice() {
  voiceEnabled = !voiceEnabled;
  localStorage.setItem(VOICE_KEY, String(voiceEnabled));
  if (!voiceEnabled && window.speechSynthesis) window.speechSynthesis.cancel();
  $("voiceToggle").textContent = "Voice: " + (voiceEnabled ? "On" : "Off");
  $("voiceToggle").classList.toggle("active", voiceEnabled);
  showToast(voiceEnabled ? "Spoken replies enabled." : "Spoken replies disabled.");
}

function startMic() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    showToast("Voice input works in supported browsers such as Chrome or Edge.");
    return;
  }
  if (recognition) {
    recognition.stop();
    recognition = null;
    $("micBtn").classList.remove("active");
    return;
  }
  if (window.speechSynthesis) window.speechSynthesis.cancel();

  recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.continuous = false;
  recognition.interimResults = true;
  $("micBtn").classList.add("active");
  let finalText = "";

  recognition.onresult = event => {
    let interim = "";
    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) finalText += transcript;
      else interim += transcript;
    }
    questionBox.value = (finalText + " " + interim).trim();
    resizeInput();
  };
  recognition.onerror = event => {
    if (event.error === "not-allowed") showToast("Allow microphone access in your browser settings.");
    else showToast("Couldn't hear that. Please try again.");
  };
  recognition.onend = () => {
    $("micBtn").classList.remove("active");
    recognition = null;
    resizeInput();
  };
  try {
    recognition.start();
  } catch (e) {
    $("micBtn").classList.remove("active");
    recognition = null;
    showToast("Microphone couldn't start. Try again.");
  }
}

$("form").addEventListener("submit", event => {
  event.preventDefault();
  sendMessage();
});
questionBox.addEventListener("keydown", event => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    sendMessage();
  }
});
questionBox.addEventListener("input", resizeInput);
$("newChat").addEventListener("click", createNewChat);
$("renameBtn").addEventListener("click", renameChat);
$("voiceToggle").addEventListener("click", toggleVoice);
$("micBtn").addEventListener("click", startMic);
$("historySearch").addEventListener("input", renderChats);
$("menuBtn").addEventListener("click", () => $("sidebar").classList.toggle("open"));

loadChats();
renderAll();
</script>
</body>
</html>
"""


def get_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NyvexiaIA/4.0 (educational chatbot)"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize(text):
    text = str(text or "").lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text.rstrip("?!., ")


def make_wiki_url(title):
    return "https://en.wikipedia.org/wiki/" + urllib.parse.quote(
        str(title).replace(" ", "_"), safe="()_,-"
    )


def get_capital_answer(question):
    q = normalize(question)
    patterns = [
        r"(?:what is|what's|tell me|give me)\s+(?:the\s+)?capital\s+of\s+(.+)",
        r"capital\s+of\s+(.+)",
        r"what\s+is\s+(.+?)[’']?s\s+capital"
    ]

    country = None
    for pattern in patterns:
        match = re.search(pattern, q)
        if match:
            country = match.group(1).strip()
            country = re.sub(r"\?+$", "", country).strip()
            country = re.sub(r"^(?:the)\s+", "", country)
            country = re.sub(r"\s+please$", "", country)
            break

    if not country:
        return None

    aliases = {
        "italie": ("Italy", "Rome"),
        "italy": ("Italy", "Rome"),
        "france": ("France", "Paris"),
        "spain": ("Spain", "Madrid"),
        "espagne": ("Spain", "Madrid"),
        "canada": ("Canada", "Ottawa"),
        "united states": ("United States", "Washington, D.C."),
        "usa": ("United States", "Washington, D.C."),
        "america": ("United States", "Washington, D.C."),
        "united kingdom": ("United Kingdom", "London"),
        "uk": ("United Kingdom", "London"),
        "england": ("England", "London"),
        "japan": ("Japan", "Tokyo"),
        "china": ("China", "Beijing"),
        "germany": ("Germany", "Berlin"),
        "allemagne": ("Germany", "Berlin"),
        "mexico": ("Mexico", "Mexico City"),
        "mexique": ("Mexico", "Mexico City"),
        "brazil": ("Brazil", "Brasília"),
        "brésil": ("Brazil", "Brasília"),
        "india": ("India", "New Delhi"),
        "australia": ("Australia", "Canberra"),
        "russia": ("Russia", "Moscow"),
        "south korea": ("South Korea", "Seoul"),
        "north korea": ("North Korea", "Pyongyang"),
        "egypt": ("Egypt", "Cairo"),
        "morocco": ("Morocco", "Rabat"),
        "maroc": ("Morocco", "Rabat"),
        "argentina": ("Argentina", "Buenos Aires"),
        "switzerland": ("Switzerland", "Bern"),
        "sweden": ("Sweden", "Stockholm"),
        "norway": ("Norway", "Oslo"),
        "finland": ("Finland", "Helsinki"),
        "greece": ("Greece", "Athens"),
        "portugal": ("Portugal", "Lisbon"),
        "ukraine": ("Ukraine", "Kyiv"),
        "turkey": ("Turkey", "Ankara"),
        "turquie": ("Turkey", "Ankara"),
        "saudi arabia": ("Saudi Arabia", "Riyadh"),
        "new zealand": ("New Zealand", "Wellington"),
        "thailand": ("Thailand", "Bangkok"),
        "indonesia": ("Indonesia", "Jakarta"),
        "pakistan": ("Pakistan", "Islamabad"),
        "nigeria": ("Nigeria", "Abuja"),
        "kenya": ("Kenya", "Nairobi"),
        "ireland": ("Ireland", "Dublin"),
        "iceland": ("Iceland", "Reykjavík"),
        "belgium": ("Belgium", "Brussels"),
        "netherlands": ("Netherlands", "Amsterdam"),
        "the netherlands": ("Netherlands", "Amsterdam"),
        "austria": ("Austria", "Vienna"),
        "poland": ("Poland", "Warsaw"),
        "cuba": ("Cuba", "Havana"),
        "colombia": ("Colombia", "Bogotá"),
        "chile": ("Chile", "Santiago"),
        "peru": ("Peru", "Lima"),
        "jamaica": ("Jamaica", "Kingston"),
        "haiti": ("Haiti", "Port-au-Prince"),
        "dominican republic": ("Dominican Republic", "Santo Domingo"),
        "costa rica": ("Costa Rica", "San José"),
        "vietnam": ("Vietnam", "Hanoi"),
        "nepal": ("Nepal", "Kathmandu"),
        "bangladesh": ("Bangladesh", "Dhaka"),
        "iran": ("Iran", "Tehran"),
        "iraq": ("Iraq", "Baghdad"),
        "israel": ("Israel", "Jerusalem"),
        "lebanon": ("Lebanon", "Beirut"),
        "singapore": ("Singapore", "Singapore"),
        "luxembourg": ("Luxembourg", "Luxembourg"),
        "monaco": ("Monaco", "Monaco"),
        "qatar": ("Qatar", "Doha"),
        "united arab emirates": ("United Arab Emirates", "Abu Dhabi"),
    }

    country = country.strip(" '\"")
    if country in aliases:
        official, capital = aliases[country]
        return (
            "The capital of " + official + " is " + capital + ".",
            [{"title": official + " — Wikipedia", "url": make_wiki_url(official)}]
        )
    return None


def calculate(question):
    q = normalize(question)
    q = q.replace("what is ", "").replace("calculate ", "").replace("solve ", "")
    q = q.replace("×", "*").replace("÷", "/").replace("^", "**")

    match = re.fullmatch(
        r"(-?\d+(?:\.\d+)?)\s*([+\-*/])\s*(-?\d+(?:\.\d+)?)",
        q
    )
    if not match:
        return None

    a = float(match.group(1))
    op = match.group(2)
    b = float(match.group(3))

    try:
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        else:
            if b == 0:
                return "You can't divide by zero."
            result = a / b

        if result.is_integer():
            result = int(result)
        return "The answer is " + str(result) + "."
    except Exception:
        return None


def chat_reply(question, history):
    q = normalize(question)

    if re.search(r"\b(hi|hello|hey|heyy|yo|sup|good morning|good afternoon|good evening)\b", q):
        return random.choice([
            "Hey! What's on your mind?",
            "Heyyy! I'm here. What do you want to explore?",
            "Hi! Ask me anything and let's figure it out.",
            "Yo! What are we talking about today?"
        ]), []

    if q in ["how are you", "how are you doing", "how r u", "wyd"]:
        return "I'm doing great and ready to help! What about you?", []

    if q in ["who are you", "what are you", "what is your name", "whats your name"]:
        return "I'm Nyvexia IA, your AI-style chat assistant. I can chat, do simple calculations, and look up information using Wikipedia. I'm not a full large language model, so some answers may be limited.", []

    if q in ["thanks", "thank you", "thx", "ty", "thank u"]:
        return random.choice([
            "You're welcome! Happy to help.",
            "Anytime! What else you got?",
            "No problem at all!"
        ]), []

    if q in ["bye", "goodbye", "see you", "cya", "good night"]:
        return "See you later! Come back whenever you want to explore something.", []

    if q in ["lol", "lmao", "haha", "hahaha", "😂", "😭"]:
        return "😂 What's so funny? Tell me!", []

    if q in ["ok", "okay", "k", "alright", "cool"]:
        return "Alright! I'm here if you need anything.", []

    if q in ["are you real", "are you human", "are you a human"]:
        return "I'm software, not a human. I can still help you find information and chat with you, though.", []

    if q in ["i love you", "love you"]:
        return "Aww, that's sweet! 💜 I'm glad you're here.", []

    if q in ["im sad", "i am sad", "i feel sad", "im bored", "i am bored"]:
        return "I'm here with you. Want to tell me what's going on, or should we find something fun to do?", []

    if q in ["tell me a joke", "make me laugh", "joke"]:
        return "Why did the computer go to the doctor? Because it had a virus. 😄", []

    if "what can you do" in q or "help me" == q:
        return "I can chat with you, answer some common questions, solve basic arithmetic, and search Wikipedia for factual information. I can make mistakes, so verify important details.", []

    if q.startswith("what is ") and len(q) > 8:
        subject = q[8:].strip()
        if subject in ["1+1", "2+2", "2+2?"]:
            return "2 + 2 = 4.", []

    result = calculate(question)
    if result is not None:
        return result, []

    return None, []


def wikipedia_search(question, history):
    original_question = question.strip()
    search_question = original_question

    q = normalize(original_question)
    followup_patterns = [
        "tell me more", "more information", "more info", "explain more",
        "go on", "continue", "what else", "and then", "why is that",
        "can you explain that", "elaborate"
    ]

    if any(q == phrase or q.startswith(phrase + " ") for phrase in followup_patterns):
        for item in reversed(history or []):
            if isinstance(item, dict) and item.get("role") == "user":
                previous = item.get("content", "").strip()
                if previous:
                    search_question = previous
                    break

    capital_answer = get_capital_answer(search_question)
    if capital_answer:
        return capital_answer

    search_url = (
        WIKIPEDIA_API + "?action=query&list=search&format=json&utf8=1&"
        + urllib.parse.urlencode({"srsearch": search_question, "srlimit": 5})
    )
    search_data = get_json(search_url)
    results = search_data.get("query", {}).get("search", [])

    if not results:
        return (
            "I couldn't find a clear Wikipedia result for that question. "
            "Try asking it in a different way or use a more specific topic.",
            []
        )

    chosen = results[0]
    title = chosen.get("title", "")
    page_url = make_wiki_url(title)

    summary_url = (
        WIKIPEDIA_API + "?action=query&prop=extracts&format=json&utf8=1&"
        + urllib.parse.urlencode({
            "titles": title,
            "explaintext": 1,
            "exintro": 1,
            "exchars": 3500
        })
    )
    summary_data = get_json(summary_url)
    pages = summary_data.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    extract = page.get("extract", "").strip()

    if not extract:
        extract = html.unescape(chosen.get("snippet", ""))
        extract = re.sub(r"<.*?>", "", extract)

    extract = re.sub(r"\s+", " ", extract).strip()

    if extract:
        sentences = re.split(r"(?<=[.!?])\s+", extract)
        summary = " ".join(sentences[:5]).strip()
    else:
        summary = "I found a Wikipedia article about " + title + "."

    if any(phrase in q for phrase in [
        "tell me more", "more information", "more info", "explain more",
        "elaborate", "go on", "continue"
    ]) and len(summary) < 250:
        summary = extract[:1800] if extract else summary

    answer = summary
    if search_question != original_question:
        answer = "Here's more information about " + title + ":\n\n" + answer

    links = [{"title": title + " — Wikipedia", "url": page_url}]

    for item in results[1:3]:
        other_title = item.get("title", "")
        if other_title and other_title != title:
            links.append({
                "title": other_title,
                "url": make_wiki_url(other_title)
            })

    return answer, links


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

        # Keep only a manageable amount of recent conversation context.
        history = [
            item for item in history[-12:]
            if isinstance(item, dict)
            and item.get("role") in ("user", "assistant")
            and isinstance(item.get("content"), str)
        ]

        answer, links = chat_reply(question, history)

        if answer is None:
            try:
                answer, links = wikipedia_search(question, history)
            except Exception:
                answer = (
                    "I couldn't connect to Wikipedia right now. "
                    "Please try again in a moment, or rephrase your question."
                )
                links = []

        updated_history = history + [
            {"role": "user", "content": question},
            {"role": "assistant", "content": answer}
        ]
        updated_history = updated_history[-12:]

        return jsonify({
            "answer": answer,
            "links": links,
            "history": updated_history
        })

    except Exception:
        return jsonify({
            "answer": "Something went wrong while processing that message. Please try again.",
            "links": [],
            "history": []
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
