from flask import Flask, request, jsonify, render_template_string
import urllib.request
import urllib.parse
import json
import html
import re
import ast
import operator
import random
import math

app = Flask(__name__)

HTML_PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nyvexia AI</title>
<style>
:root{--purple:#8B5CF6;--cyan:#22D3EE;--pink:#F472B6;--background:#101426;--panel:#151a30;--panel-light:#1b2139;--text:#F8FAFF;--muted:#9aa5c0;--border:rgba(180,190,230,.12)}
*{box-sizing:border-box}body{margin:0;height:100vh;overflow:hidden;color:var(--text);background:var(--background);font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}button,input,textarea{font:inherit}button{cursor:pointer}.app{display:flex;width:100%;height:100vh}
.sidebar{width:270px;flex-shrink:0;display:flex;flex-direction:column;padding:20px 14px;background:#0d1121;border-right:1px solid var(--border)}
.brand{display:flex;align-items:center;gap:11px;padding:4px 8px 24px}.logo{width:39px;height:39px;border-radius:13px;display:grid;place-items:center;background:linear-gradient(145deg,var(--purple),#5b5bd6 55%,#278fae);font-weight:800;font-size:19px;box-shadow:0 5px 18px rgba(139,92,246,.18)}.brand-name{font-size:17px;font-weight:750;letter-spacing:-.4px}.brand-sub{font-size:10px;color:var(--muted);letter-spacing:1.6px;margin-top:3px}
.new-chat{border:1px solid rgba(139,92,246,.36);background:rgba(139,92,246,.12);color:var(--text);border-radius:11px;padding:12px 13px;text-align:left}.new-chat:hover{background:rgba(139,92,246,.22);border-color:var(--purple)}
.search-wrap{margin:15px 0 17px}.search-wrap input{width:100%;padding:10px 12px;color:var(--text);background:#151a2d;border:1px solid var(--border);border-radius:10px;outline:none}.section-label{padding:0 8px 9px;color:#77829f;font-size:10px;font-weight:700;letter-spacing:1.5px}.chat-list{overflow-y:auto;flex:1}.chat-item{display:flex;align-items:center;gap:8px;padding:10px 9px;border-radius:9px;margin-bottom:3px;color:#bdc6dc;font-size:13px;cursor:pointer}.chat-item:hover{background:rgba(255,255,255,.045)}.chat-item.active{background:rgba(139,92,246,.15);color:white}.chat-title{flex:1;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.delete-chat{border:0;background:transparent;color:#8b94ad;padding:2px 4px}.sidebar-bottom{border-top:1px solid var(--border);margin-top:12px;padding:14px 7px 0;color:#7e8aa7;font-size:11px;line-height:1.6}.status-dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#34d399;margin-right:6px}
.main{min-width:0;flex:1;display:flex;flex-direction:column;position:relative}.topbar{height:68px;flex-shrink:0;display:flex;align-items:center;justify-content:space-between;padding:0 26px;border-bottom:1px solid var(--border);background:rgba(16,20,38,.86)}.current-title{font-size:13px;color:#d8def0;font-weight:600}.top-actions{display:flex;align-items:center;gap:8px}.small-btn{border:1px solid var(--border);background:#171c31;color:#d9e0f2;padding:8px 11px;border-radius:9px;font-size:12px}.small-btn:hover{border-color:rgba(139,92,246,.6)}.mobile-menu{display:none}
.messages{flex:1;overflow-y:auto;padding:32px 20px 28px;scroll-behavior:smooth}.message-list{width:100%;max-width:790px;margin:0 auto}.welcome{padding:8vh 0 26px;text-align:center}.welcome-mark{width:68px;height:68px;border-radius:22px;margin:0 auto 23px;display:grid;place-items:center;font-size:29px;font-weight:800;background:linear-gradient(145deg,rgba(139,92,246,.25),rgba(34,211,238,.1));border:1px solid rgba(139,92,246,.32);color:#d9d0ff}.welcome h1{font-size:clamp(28px,4vw,40px);letter-spacing:-1.6px;margin:0 0 12px}.welcome h1 span{background:linear-gradient(100deg,#b9a5ff,#73e6f2);-webkit-background-clip:text;background-clip:text;color:transparent}.welcome p{color:var(--muted);font-size:14px;line-height:1.7;max-width:470px;margin:0 auto}.suggestions{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;margin:28px auto 0;max-width:570px}.suggestion{padding:13px 14px;text-align:left;border-radius:12px;background:rgba(255,255,255,.025);border:1px solid var(--border);color:#d9e0f2;font-size:12px}.suggestion:hover{background:rgba(139,92,246,.09);border-color:rgba(139,92,246,.45)}.suggestion span{display:block;color:#8792af;font-size:11px;margin-top:5px}
.message{display:flex;gap:13px;margin:0 0 26px;align-items:flex-start}.avatar{flex-shrink:0;width:31px;height:31px;border-radius:10px;display:grid;place-items:center;font-size:12px;font-weight:800}.avatar.user{background:#303954;color:#e2e8f8}.avatar.bot{background:linear-gradient(145deg,var(--purple),#397cba);color:white}.message-body{min-width:0;flex:1;padding-top:4px}.message-name{font-size:11px;color:#8f9bb7;margin-bottom:8px;font-weight:650}.message-text{color:#e4e9f6;font-size:14px;line-height:1.8;white-space:pre-wrap;overflow-wrap:anywhere}.sources{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.source-link{font-size:11px;color:#bcb0ff;text-decoration:none;border:1px solid rgba(139,92,246,.24);border-radius:7px;padding:6px 9px;background:rgba(139,92,246,.07)}.source-link:hover{border-color:var(--purple)}
.composer-area{padding:8px 20px 18px;flex-shrink:0}.composer-wrap{max-width:790px;margin:0 auto}.composer{display:flex;align-items:flex-end;gap:9px;padding:10px;border-radius:16px;border:1px solid rgba(170,180,220,.19);background:#171c30;box-shadow:0 10px 35px rgba(0,0,0,.12)}.composer:focus-within{border-color:rgba(139,92,246,.65)}#question{flex:1;min-width:0;resize:none;max-height:140px;border:0;outline:none;background:transparent;color:var(--text);font-size:14px;line-height:1.55;padding:8px 5px}#question::placeholder{color:#7985a2}.icon-btn{width:37px;height:37px;flex-shrink:0;display:grid;place-items:center;border-radius:10px;background:transparent;border:1px solid transparent;color:#9aa6c3;font-size:16px}.icon-btn:hover,.icon-btn.active{background:rgba(34,211,238,.1);color:var(--cyan)}.send-btn{width:38px;height:38px;border:0;border-radius:11px;background:linear-gradient(135deg,var(--purple),#6475df);color:white;font-size:18px}.send-btn:disabled{opacity:.45;cursor:not-allowed}.disclaimer{text-align:center;color:#77829d;font-size:10px;margin-top:11px}.typing{display:inline-flex;gap:4px;padding:5px 0}.typing span{width:5px;height:5px;background:#a79aff;border-radius:50%;animation:pulse 1s infinite alternate}.typing span:nth-child(2){animation-delay:.2s}.typing span:nth-child(3){animation-delay:.4s}@keyframes pulse{from{opacity:.25;transform:translateY(0)}to{opacity:1;transform:translateY(-3px)}}.toast{position:fixed;bottom:92px;left:50%;transform:translateX(-50%);background:#222941;border:1px solid var(--border);color:#e9edfa;padding:10px 15px;border-radius:10px;font-size:12px;display:none;z-index:10;box-shadow:0 8px 30px #0004}
@media(max-width:720px){.sidebar{position:fixed;z-index:20;top:0;bottom:0;left:0;transform:translateX(-105%);transition:transform .22s ease;box-shadow:12px 0 40px #0005}.sidebar.open{transform:translateX(0)}.mobile-menu{display:inline-grid}.topbar{height:60px;padding:0 13px;gap:10px}.top-actions{gap:5px}.small-btn{padding:7px 8px;font-size:11px}.messages{padding:20px 14px}.welcome{padding-top:7vh}.suggestions{grid-template-columns:1fr;margin-top:22px}.composer-area{padding:6px 12px 12px}.message{gap:9px}}
</style>
</head>
<body>
<div class="app">
<aside class="sidebar" id="sidebar"><div class="brand"><div class="logo">N</div><div><div class="brand-name">NYVEXIA AI</div><div class="brand-sub">YOUR THINKING SPACE</div></div></div>
<button class="new-chat" id="newChat">＋ &nbsp; New conversation</button><div class="search-wrap"><input id="historySearch" placeholder="Search conversations..." autocomplete="off"></div><div class="section-label">YOUR CONVERSATIONS</div><div class="chat-list" id="chatList"></div><div class="sidebar-bottom"><span class="status-dot"></span>Nyvexia is ready<br>Chats are saved in this browser.</div></aside>
<main class="main"><header class="topbar"><div style="display:flex;align-items:center;gap:10px;min-width:0"><button class="small-btn mobile-menu" id="menuBtn">☰</button><div class="current-title" id="currentTitle">New conversation</div></div><div class="top-actions"><button class="small-btn" id="renameBtn">Rename</button><button class="small-btn" id="voiceToggle">Voice: Off</button></div></header>
<section class="messages" id="messages"><div class="message-list" id="messageList"></div></section>
<div class="composer-area"><div class="composer-wrap"><form class="composer" id="form"><button class="icon-btn" type="button" id="micBtn" title="Speak your message">♩</button><textarea id="question" rows="1" placeholder="Ask Nyvexia anything..." autocomplete="off"></textarea><button class="send-btn" id="send" type="submit">↑</button></form><div class="disclaimer">Nyvexia can search the web, calculate, and translate. Verify important information.</div></div></div></main></div><div class="toast" id="toast"></div>
<script>
const STORAGE_KEY="nyvexia_galaxy_chats_v1",VOICE_KEY="nyvexia_voice_enabled_v1";
const welcomeMessage={who:"bot",text:"Hey! Welcome to Nyvexia AI. Ask me a question, search the web, solve a math problem, or translate between languages.",links:[]};
let chats=[],activeId=null,busy=false,voiceEnabled=localStorage.getItem(VOICE_KEY)==="true",recognition=null,toastTimer=null;
const $=id=>document.getElementById(id),messagesBox=$("messages"),messageList=$("messageList"),questionBox=$("question"),sendButton=$("send");
function makeChat(){return{id:(crypto.randomUUID?crypto.randomUUID():String(Date.now())+Math.random()),title:"New conversation",messages:[{...welcomeMessage}],apiHistory:[],created:Date.now()}}
function loadChats(){try{const saved=JSON.parse(localStorage.getItem(STORAGE_KEY)||"[]");if(Array.isArray(saved))chats=saved.filter(c=>c&&c.id&&Array.isArray(c.messages)).map(c=>({id:c.id,title:c.title||"New conversation",messages:c.messages,apiHistory:Array.isArray(c.apiHistory)?c.apiHistory:[],created:c.created||Date.now()}))}catch(e){chats=[]}if(!chats.length)chats=[makeChat()];activeId=chats[0].id;saveChats()}
function saveChats(){try{localStorage.setItem(STORAGE_KEY,JSON.stringify(chats))}catch(e){showToast("Could not save chats in this browser.")}}
function activeChat(){return chats.find(c=>c.id===activeId)||chats[0]}
function showToast(text){const el=$("toast");el.textContent=text;el.style.display="block";clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.style.display="none",2600)}
function renderChats(){const term=$("historySearch").value.trim().toLowerCase(),list=$("chatList");list.innerHTML="";const filtered=[...chats].sort((a,b)=>(b.created||0)-(a.created||0)).filter(c=>!term||c.title.toLowerCase().includes(term)||c.messages.some(m=>String(m.text||"").toLowerCase().includes(term)));if(!filtered.length){list.textContent="No matching conversations.";return}filtered.forEach(chat=>{const item=document.createElement("div");item.className="chat-item"+(chat.id===activeId?" active":"");const title=document.createElement("span");title.className="chat-title";title.textContent=chat.title;const del=document.createElement("button");del.className="delete-chat";del.textContent="×";del.title="Delete conversation";del.onclick=e=>{e.stopPropagation();deleteChat(chat.id)};item.append(title,del);item.onclick=()=>{activeId=chat.id;renderAll();if(innerWidth<=720)$("sidebar").classList.remove("open")};list.append(item)})}
function welcomeHTML(){return `<div class="welcome"><div class="welcome-mark">N</div><h1>Meet <span>Nyvexia AI.</span></h1><p>A space to ask questions, discover ideas, and explore what you're curious about.</p><div class="suggestions"><button class="suggestion" data-prompt="Explain artificial intelligence in simple terms">Explain a big idea<span>Understand a topic</span></button><button class="suggestion" data-prompt="What is the latest news about space?">Search the web<span>Find current information</span></button><button class="suggestion" data-prompt="Solve 3x + 7 = 22 and show the steps">Solve a math problem<span>Get steps, not just an answer</span></button><button class="suggestion" data-prompt="Translate 'How are you today?' into French, Spanish, and Japanese">Translate a sentence<span>Try different languages</span></button></div></div>`}
function renderMessages(){const chat=activeChat();if(!chat)return;$("currentTitle").textContent=chat.title;messageList.innerHTML="";if(chat.messages.length===1&&chat.messages[0].text===welcomeMessage.text){messageList.innerHTML=welcomeHTML();messageList.querySelectorAll("[data-prompt]").forEach(b=>b.onclick=()=>{questionBox.value=b.dataset.prompt;questionBox.focus();resizeInput()});return}chat.messages.forEach(msg=>{const row=document.createElement("div");row.className="message";const av=document.createElement("div");av.className="avatar "+(msg.who==="user"?"user":"bot");av.textContent=msg.who==="user"?"Y":"N";const body=document.createElement("div");body.className="message-body";const name=document.createElement("div");name.className="message-name";name.textContent=msg.who==="user"?"You":"Nyvexia AI";const content=document.createElement("div");content.className="message-text";content.textContent=msg.text||"";body.append(name,content);if(msg.who!=="user"&&Array.isArray(msg.links)&&msg.links.length){const links=document.createElement("div");links.className="sources";msg.links.forEach(link=>{if(!link.url||!/^https?:\/\//i.test(link.url))return;const a=document.createElement("a");a.className="source-link";a.href=link.url;a.target="_blank";a.rel="noopener noreferrer";a.textContent=link.title||"Source";links.append(a)});body.append(links)}row.append(av,body);messageList.append(row)});if(busy){const row=document.createElement("div");row.className="message";row.innerHTML='<div class="avatar bot">N</div><div class="message-body"><div class="message-name">Nyvexia AI</div><div class="typing"><span></span><span></span><span></span></div></div>';messageList.append(row)}}
function renderAll(){renderChats();renderMessages();saveChats();messagesBox.scrollTop=messagesBox.scrollHeight;$("voiceToggle").textContent="Voice: "+(voiceEnabled?"On":"Off")}
function createNewChat(){const c=makeChat();chats.unshift(c);activeId=c.id;questionBox.value="";renderAll();questionBox.focus();if(innerWidth<=720)$("sidebar").classList.remove("open")}
function deleteChat(id){const c=chats.find(x=>x.id===id);if(!c||!confirm('Delete "'+c.title+'"?'))return;chats=chats.filter(x=>x.id!==id);if(!chats.length)chats=[makeChat()];if(activeId===id)activeId=chats[0].id;renderAll()}
function renameChat(){const c=activeChat(),v=prompt("Rename this conversation:",c.title);if(v===null)return;const n=v.trim().slice(0,70);if(!n)return showToast("The title can't be empty.");c.title=n;renderAll()}
function autoTitle(c,t){if(c.title==="New conversation"){t=t.replace(/\s+/g," ").trim();c.title=t.length>34?t.slice(0,31)+"...":t}}
function resizeInput(){questionBox.style.height="auto";questionBox.style.height=Math.min(questionBox.scrollHeight,140)+"px"}
async function sendMessage(override){if(busy)return;const question=(typeof override==="string"?override:questionBox.value).trim();if(!question)return;const chat=activeChat();questionBox.value="";resizeInput();autoTitle(chat,question);chat.messages.push({who:"user",text:question,links:[]});busy=true;sendButton.disabled=true;renderAll();try{const response=await fetch("/ask",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({question,history:chat.apiHistory})});const data=await response.json();if(!response.ok)throw Error(data.error||"Request failed");chat.messages.push({who:"bot",text:data.answer||"Sorry, I couldn't find an answer.",links:Array.isArray(data.links)?data.links:[]});if(Array.isArray(data.history))chat.apiHistory=data.history;saveChats();renderAll();if(voiceEnabled)speak(data.answer||"")}catch(e){chat.messages.push({who:"bot",text:"I couldn't reach the answer service. Please try again in a moment.",links:[]});renderAll();showToast("Connection problem. Try again.")}finally{busy=false;sendButton.disabled=false;renderAll();questionBox.focus()}}
function speak(text){if(!("speechSynthesis"in window))return showToast("Spoken replies aren't supported in this browser.");speechSynthesis.cancel();const u=new SpeechSynthesisUtterance(text);u.lang=detectSpeechLanguage(text);speechSynthesis.speak(u)}
function detectSpeechLanguage(t){if(/[ñ¿¡áéíóú]/i.test(t))return"es-ES";if(/[àâçéèêëîïôûùüÿœ]/i.test(t))return"fr-FR";return"en-US"}
function toggleVoice(){voiceEnabled=!voiceEnabled;localStorage.setItem(VOICE_KEY,String(voiceEnabled));if(!voiceEnabled&&speechSynthesis)speechSynthesis.cancel();renderAll();showToast(voiceEnabled?"Spoken replies enabled.":"Spoken replies disabled.")}
function startMic(){const SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR)return showToast("Voice input works in supported browsers such as Chrome or Edge.");if(recognition){recognition.stop();recognition=null;$("micBtn").classList.remove("active");return}recognition=new SR();recognition.lang="en-US";recognition.continuous=false;recognition.interimResults=true;$("micBtn").classList.add("active");let finalText="";recognition.onresult=e=>{let interim="";for(let i=e.resultIndex;i<e.results.length;i++){const t=e.results[i][0].transcript;if(e.results[i].isFinal)finalText+=t;else interim+=t}questionBox.value=(finalText+" "+interim).trim();resizeInput()};recognition.onerror=e=>showToast(e.error==="not-allowed"?"Allow microphone access in your browser settings.":"Couldn't hear that. Try again.");recognition.onend=()=>{$("micBtn").classList.remove("active");recognition=null};try{recognition.start()}catch(e){recognition=null;$("micBtn").classList.remove("active");showToast("Microphone couldn't start. Try again.")}}
$("form").addEventListener("submit",e=>{e.preventDefault();sendMessage()});questionBox.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();sendMessage()}});questionBox.addEventListener("input",resizeInput);$("newChat").onclick=createNewChat;$("renameBtn").onclick=renameChat;$("voiceToggle").onclick=toggleVoice;$("micBtn").onclick=startMic;$("historySearch").oninput=renderChats;$("menuBtn").onclick=()=>$("sidebar").classList.toggle("open");loadChats();renderAll();
</script></body></html>
"""

def fetch_text(url, timeout=12, headers=None):
    default_headers = {"User-Agent": "NyvexiaAI/5.0 (personal educational assistant)"}
    if headers:
        default_headers.update(headers)
    req = urllib.request.Request(url, headers=default_headers)
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return response.read().decode("utf-8", errors="replace")


def normalize(text):
    return re.sub(r"\s+", " ", str(text or "").lower().strip()).rstrip("?!., ")


def translate_text(text, target, source="auto"):
    """Use MyMemory's public translation endpoint; it has request limits."""
    target_codes = {
        "english":"en", "anglais":"en", "en":"en",
        "french":"fr", "français":"fr", "francais":"fr", "fr":"fr",
        "spanish":"es", "español":"es", "espagnol":"es", "es":"es",
        "german":"de", "allemand":"de", "deutsch":"de", "de":"de",
        "italian":"it", "italien":"it", "italiano":"it", "it":"it",
        "portuguese":"pt", "portugais":"pt", "português":"pt", "pt":"pt",
        "japanese":"ja", "japonais":"ja", "日本語":"ja", "ja":"ja",
        "chinese":"zh-CN", "chinois":"zh-CN", "中文":"zh-CN",
        "arabic":"ar", "arabe":"ar", "العربية":"ar",
        "korean":"ko", "coréen":"ko", "한국어":"ko",
        "hindi":"hi", "हिन्दी":"hi", "russian":"ru", "russe":"ru", "русский":"ru"
    }
    tgt = target_codes.get(target.lower().strip(), target.strip())
    src = "en" if source == "auto" else target_codes.get(source.lower().strip(), source.strip())
    query = urllib.parse.urlencode({"q": text[:450], "langpair": src + "|" + tgt})
    data = json.loads(fetch_text("https://api.mymemory.translated.net/get?" + query, timeout=15))
    translated = data.get("responseData", {}).get("translatedText", "")
    translated = html.unescape(translated)
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


def safe_calculate(expression):
    """Safely evaluate arithmetic expressions without eval()."""
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

    # Handle simple linear equations such as 3x + 7 = 22.
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
            f"Let's solve it step by step:\n\n"
            f"{a:g}x {b:+g} = {c:g}\n"
            f"Subtract {b:g} from both sides: {a:g}x = {c-b:g}\n"
            f"Divide both sides by {a:g}: x = {x:g}\n\n"
            f"Answer: x = {x:g}",
            []
        )

    cleaned = re.sub(r"^(what is|what's|calculate|compute|evaluate|solve)\s+", "", q, flags=re.I).strip().rstrip("?=")
    cleaned = cleaned.replace("²", "**2").replace("³", "**3")

    if not re.fullmatch(r"[\d\s.+\-*/()%^×÷,]+", cleaned):
        return None

    try:
        result = safe_calculate(cleaned)
        if isinstance(result, float):
            shown = str(int(result)) if result.is_integer() else f"{result:.10g}"
        else:
            shown = str(result)
        return f"{cleaned} = {shown}", []
    except ZeroDivisionError:
        return "You can't divide by zero.", []
    except Exception:
        return None


def web_search(question, limit=5):
    """Search DuckDuckGo's public HTML results; no API key required."""
    url = "https://html.duckduckgo.com/html/?" + urllib.parse.urlencode({"q": question})
    page = fetch_text(url, timeout=15)

    blocks = re.findall(
        r'(?is)<div[^>]+class="result[^"]*"[^>]*>(.*?)</div>\s*</div>',
        page
    )
    results = []

    for block in blocks:
        link_match = re.search(
            r'(?is)<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
            block
        )
        if not link_match:
            continue

        url_value = html.unescape(link_match.group(1))
        title = re.sub(r"<.*?>", "", html.unescape(link_match.group(2)))
        title = re.sub(r"\s+", " ", title).strip()

        snippet_match = re.search(
            r'(?is)class="result__snippet"[^>]*>(.*?)</',
            block
        )
        snippet = re.sub(
            r"<.*?>", "", html.unescape(snippet_match.group(1))
        ) if snippet_match else ""
        snippet = re.sub(r"\s+", " ", snippet).strip()

        if "uddg=" in url_value:
            try:
                url_value = urllib.parse.parse_qs(
                    urllib.parse.urlparse(url_value).query
                ).get("uddg", [url_value])[0]
            except Exception:
                pass

        if url_value.startswith("http") and title:
            results.append({
                "title": title[:180],
                "url": url_value,
                "snippet": snippet[:500]
            })

        if len(results) >= limit:
            break

    return results


def wikipedia_search(question):
    api = "https://en.wikipedia.org/w/api.php?"
    search_url = api + urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "format": "json",
        "utf8": 1,
        "srsearch": question,
        "srlimit": 4
    })
    data = json.loads(fetch_text(search_url))
    results = data.get("query", {}).get("search", [])
    links = []
    pieces = []

    for item in results[:3]:
        title = item.get("title", "")
        if not title:
            continue
        page_url = "https://en.wikipedia.org/wiki/" + urllib.parse.quote(
            title.replace(" ", "_"), safe="()_,-"
        )
        links.append({"title": title + " — Wikipedia", "url": page_url})
        snippet = re.sub(
            r"<.*?>", "", html.unescape(item.get("snippet", ""))
        )
        if snippet:
            pieces.append(title + ": " + snippet)

    return ("\n\n".join(pieces) if pieces else ""), links


def answer_question(question, history):
    q = normalize(question)

    if q in {"hi", "hello", "hey", "heyy", "yo", "sup",
             "good morning", "good afternoon", "good evening"}:
        return random.choice([
            "Hey! What's on your mind?",
            "Heyyy! What should we explore today?",
            "Hi! Ask me anything and let's figure it out."
        ]), []

    if q in {"thanks", "thank you", "thx", "ty", "thank u"}:
        return "You're welcome! 💜", []

    if q in {"who are you", "what are you", "what is your name", "whats your name"}:
        return (
            "I'm Nyvexia AI. I can search the web, help with calculations, "
            "and translate text between many languages. I can still make "
            "mistakes, so verify important information."
        ), []

    if q in {"what can you do", "help me"}:
        return (
            "I can search the web for current information, solve many "
            "arithmetic problems and simple linear equations, translate "
            "text, and answer in several languages. Try: “What happened "
            "in space exploration this week?”, “Solve 3x + 7 = 22”, or "
            "“Translate hello to French.”"
        ), []

    translation = extract_translation_request(question)
    if translation:
        text, target = translation
        try:
            translated = translate_text(text, target)
            return (
                f"Translation into {target}:\n{translated}\n\n"
                "Note: automatic translations can miss context or nuance."
            ), []
        except Exception:
            return "I couldn't reach the translation service right now. Please try again in a moment.", []

    say_match = re.match(
        r"(?is)^\s*(?:how do you say|how to say)\s+(.+?)\s+in\s+([a-zA-ZÀ-ÿ -]+)[?!.]*\s*$",
        question
    )
    if say_match:
        try:
            return translate_text(
                say_match.group(1).strip(" '\""),
                say_match.group(2).strip()
            ), []
        except Exception:
            pass

    math_result = math_answer(question)
    if math_result is not None:
        return math_result

    # Search the wider web first instead of relying only on Wikipedia.
    try:
        results = web_search(question, 5)
    except Exception:
        results = []

    if results:
        answer_lines = ["I searched the web. Here are some relevant results:"]
        links = []

        for item in results[:4]:
            line = "• " + item["title"]
            if item["snippet"]:
                line += "\n  " + item["snippet"]
            answer_lines.append(line)
            links.append({
                "title": item["title"],
                "url": item["url"]
            })

        answer_lines.append(
            "\nThese are search-result excerpts, not a fully verified "
            "summary. Open the source links to check the details."
        )
        return "\n\n".join(answer_lines), links

    # Fall back to Wikipedia if the wider web search fails.
    try:
        answer, links = wikipedia_search(question)
        if answer:
            return (
                answer + "\n\nI couldn't retrieve broader web results, "
                "so this fallback uses Wikipedia search excerpts."
            ), links
    except Exception:
        pass

    return (
        "I couldn't retrieve web results right now. Please try again, "
        "or rephrase your question. Math expressions and translation "
        "requests can still work when their services are available."
    ), []


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
            item for item in history[-10:]
            if isinstance(item, dict)
            and item.get("role") in ("user", "assistant")
            and isinstance(item.get("content"), str)
        ]

        answer, links = answer_question(question, history)

        updated_history = (
            history
            + [
                {"role": "user", "content": question},
                {"role": "assistant", "content": answer}
            ]
        )[-10:]

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
