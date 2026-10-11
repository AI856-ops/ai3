
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

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nyvexia IA 🚀</title>

<style>
:root {
  --purple: #8B5CF6;
  --blue: #22D3EE;
  --white: #F8FAFF;
  --background: #101426;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: Arial, sans-serif;
  background:
    radial-gradient(ellipse at top left, #39216b55, transparent 45%),
    radial-gradient(ellipse at bottom right, #123e7955, transparent 45%),
    var(--background);
  color: var(--white);
  height: 100vh;
  overflow: hidden;
}

button, input { font: inherit; }

button {
  cursor: pointer;
  color: white;
  border: 1px solid #344568;
  background: #192440;
  border-radius: 10px;
  padding: 10px 12px;
}

button:hover {
  border-color: var(--blue);
  box-shadow: 0 0 12px #22D3EE22;
}

.app {
  display: flex;
  width: 100%;
  height: 100vh;
}

.sidebar {
  width: 270px;
  min-width: 230px;
  background: #0b1020ee;
  border-right: 1px solid #293656;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.brand {
  color: var(--purple);
  font-size: 22px;
  font-weight: bold;
  text-shadow: 0 0 16px #8B5CF655;
  padding: 8px 2px;
}

.new-chat {
  width: 100%;
  background: linear-gradient(135deg, #8B5CF6, #2563EB);
  border: none;
  font-weight: bold;
  padding: 13px;
}

.search {
  width: 100%;
  padding: 12px;
  background: #111a30;
  border: 1px solid #344568;
  color: white;
  border-radius: 10px;
  outline: none;
}

.search:focus, input:focus {
  border-color: var(--blue);
  box-shadow: 0 0 10px #22D3EE22;
}

.section-label {
  color: #9aaed0;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 5px;
}

#chatList {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chat-item {
  width: 100%;
  text-align: left;
  background: transparent;
  border: 1px solid transparent;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 11px;
  min-width: 0;
}

.chat-item.active {
  background: #29204c;
  border-color: #8B5CF677;
}

.chat-name {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  min-width: 0;
}

.empty-history {
  color: #8c9ab8;
  font-size: 13px;
  line-height: 1.5;
  padding: 10px 3px;
}

.sidebar-bottom {
  border-top: 1px solid #293656;
  padding-top: 12px;
  color: #91a1c1;
  font-size: 12px;
  line-height: 1.6;
}

.main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

header {
  padding: 15px 22px;
  text-align: center;
  background: #121b31dd;
  border-bottom: 1px solid #293656;
}

header h1 {
  margin: 0;
  color: var(--purple);
  text-shadow: 0 0 18px #8B5CF655;
  font-size: 25px;
}

header p {
  color: #a8b7d3;
  margin: 7px 0 0;
  font-size: 13px;
}

.toolbar {
  display: flex;
  gap: 8px;
  padding: 10px 18px;
  border-bottom: 1px solid #293656;
  align-items: center;
}

#currentTitle {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #dbeafe;
  font-size: 14px;
}

#renameButton {
  border-color: #8B5CF677;
}

#messages {
  flex: 1;
  overflow-y: auto;
  padding: 22px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  padding: 13px 16px;
  border-radius: 14px;
  max-width: 90%;
  line-height: 1.55;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.bot {
  background: #1b2943;
  border: 1px solid #8B5CF644;
  align-self: flex-start;
}

.user {
  background: #30245a;
  border: 1px solid var(--purple);
  align-self: flex-end;
}

.message-links {
  align-self: flex-start;
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding-left: 10px;
  max-width: 90%;
}

.message-links a {
  color: var(--blue);
  overflow-wrap: anywhere;
  text-decoration: none;
}

.message-links a:hover {
  text-decoration: underline;
}

#form {
  display: flex;
  gap: 10px;
  padding: 16px;
  border-top: 1px solid #293656;
  background: #10182b;
}

#question {
  flex: 1;
  min-width: 0;
  padding: 14px;
  border-radius: 10px;
  border: 1px solid #405574;
  background: #080d1b;
  color: white;
  font-size: 16px;
}

#send {
  padding: 0 20px;
  border: none;
  background: linear-gradient(135deg, var(--purple), #2563EB);
  font-weight: bold;
}

button:disabled { opacity: .55; cursor: wait; }

@media(max-width: 650px) {
  .sidebar {
    width: 190px;
    min-width: 160px;
    padding: 10px;
  }

  .brand { font-size: 17px; }

  header { padding: 13px 8px; }
  header h1 { font-size: 21px; }

  #messages { padding: 12px; }
  #form { padding: 10px; gap: 6px; }

  #send { padding: 0 12px; }
  .toolbar { padding: 9px; gap: 5px; }
  #renameButton { padding: 9px 7px; }
}

@media(max-width: 420px) {
  .sidebar {
    width: 125px;
    min-width: 125px;
    padding: 7px;
  }

  .brand { font-size: 14px; }
  .new-chat { padding: 9px 5px; font-size: 12px; }
  .search { padding: 9px 5px; font-size: 12px; }
  .chat-item { padding: 8px 5px; font-size: 12px; }
  .section-label { font-size: 10px; }
  .sidebar-bottom { font-size: 10px; }
  #currentTitle { font-size: 12px; }
}
</style>
</head>

<body>
<div class="app">

  <aside class="sidebar">
    <div class="brand">🌌 NYVEXIA</div>

    <button class="new-chat" id="newChat">＋ New Chat</button>

    <input
      id="historySearch"
      class="search"
      type="search"
      placeholder="🔎 Search history..."
      autocomplete="off"
    >

    <div class="section-label">Your conversations</div>
    <div id="chatList"></div>

    <div class="sidebar-bottom">
      💜 Galaxy mode<br>
      Your chats are saved in this browser.
    </div>
  </aside>

  <main class="main">
    <header>
      <h1>NYVEXIA IA 🚀</h1>
      <p>Your digital buddy • Powered by Wikipedia</p>
    </header>

    <div class="toolbar">
      <div id="currentTitle">New conversation</div>
      <button id="renameButton" type="button">✏️ Rename</button>
    </div>

    <div id="messages"></div>

    <form id="form">
      <input
        id="question"
        placeholder="Talk to Nyvexia..."
        autocomplete="off"
        maxlength="500"
        required
      >
      <button id="send" type="submit">SEND 🚀</button>
    </form>
  </main>

</div>

<script>
const STORAGE_KEY = "nyvexia_galaxy_chats_v1";

const messages = document.getElementById("messages");
const form = document.getElementById("form");
const input = document.getElementById("question");
const send = document.getElementById("send");
const chatList = document.getElementById("chatList");
const historySearch = document.getElementById("historySearch");
const currentTitle = document.getElementById("currentTitle");
const renameButton = document.getElementById("renameButton");

const welcomeMessage = {
    who: "bot",
    text: "Heyyy! 👋 Welcome to Nyvexia IA!\\nAsk questions or just talk to me. I'm listening! 💜🚀",
    links: []
};

let chats = [];
let activeChatId = null;
let busy = false;

function makeId() {
    return Date.now().toString(36) +
        Math.random().toString(36).slice(2, 9);
}

function saveChats() {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(chats));
    } catch (error) {
        console.error("Could not save chat history:", error);
    }
}

function getActiveChat() {
    return chats.find(chat => chat.id === activeChatId);
}

function createChat() {
    const chat = {
        id: makeId(),
        title: "New conversation",
        messages: [{...welcomeMessage}],
        apiHistory: []
    };

    chats.unshift(chat);
    activeChatId = chat.id;

    saveChats();
    renderChatList();
    renderMessages();
    input.focus();
}

function renderChatList() {
    const term = historySearch.value.trim().toLowerCase();
    chatList.replaceChildren();

    const filtered = chats.filter(chat => {
        const titleMatches = chat.title.toLowerCase().includes(term);
        const messageMatches = chat.messages.some(message =>
            String(message.text || "").toLowerCase().includes(term)
        );

        return titleMatches || messageMatches;
    });

    if (filtered.length === 0) {
        const empty = document.createElement("div");
        empty.className = "empty-history";
        empty.textContent = term
            ? "No conversations match your search."
            : "No conversations yet. Start a new chat!";
        chatList.appendChild(empty);
        return;
    }

    filtered.forEach(chat => {
        const button = document.createElement("button");
        button.type = "button";
        button.className = "chat-item" +
            (chat.id === activeChatId ? " active" : "");

        const icon = document.createElement("span");
        icon.textContent = "💬";

        const name = document.createElement("span");
        name.className = "chat-name";
        name.textContent = chat.title;

        button.append(icon, name);
        button.title = chat.title;

        button.addEventListener("click", () => {
            activeChatId = chat.id;
            renderChatList();
            renderMessages();
        });

        chatList.appendChild(button);
    });
}

function renderMessages() {
    const chat = getActiveChat();
    messages.replaceChildren();

    if (!chat) {
        currentTitle.textContent = "New conversation";
        return;
    }

    currentTitle.textContent = chat.title;

    chat.messages.forEach(message => {
        addMessageToScreen(message, false);
    });

    messages.scrollTop = messages.scrollHeight;
}

function addMessageToScreen(message, scroll = true) {
    const box = document.createElement("div");
    box.className = "message " + message.who;
    box.textContent = message.text;
    messages.appendChild(box);

    if (message.links && message.links.length) {
        const linkBox = document.createElement("div");
        linkBox.className = "message-links";

        message.links.forEach(link => {
            const a = document.createElement("a");
            a.href = link.url;
            a.target = "_blank";
            a.rel = "noopener noreferrer";
            a.textContent = "🔗 " + link.title;
            linkBox.appendChild(a);
        });

        messages.appendChild(linkBox);
    }

    if (scroll) {
        messages.scrollTop = messages.scrollHeight;
    }
}

function addMessage(text, who, links = []) {
    const chat = getActiveChat();
    if (!chat) return;

    const message = {text, who, links};
    chat.messages.push(message);

    addMessageToScreen(message);
    saveChats();
}

function renameChat() {
    const chat = getActiveChat();
    if (!chat) return;

    const answer = prompt("What do you want to name this conversation?", chat.title);

    if (answer === null) return;

    const newTitle = answer.trim().slice(0, 70);

    if (!newTitle) {
        alert("The conversation name cannot be empty.");
        return;
    }

    chat.title = newTitle;
    saveChats();
    renderChatList();
    renderMessages();
}

document.getElementById("newChat").addEventListener("click", createChat);
renameButton.addEventListener("click", renameChat);

historySearch.addEventListener("input", renderChatList);

form.addEventListener("submit", async event => {
    event.preventDefault();

    const question = input.value.trim();
    const chat = getActiveChat();

    if (!question || !chat || busy) return;

    busy = true;

    addMessage(question, "user");

    // Give a new conversation a useful title automatically.
    if (
        chat.title === "New conversation" &&
        question.length > 0
    ) {
        chat.title = question.slice(0, 35) +
            (question.length > 35 ? "..." : "");
        currentTitle.textContent = chat.title;
        renderChatList();
        saveChats();
    }

    input.value = "";
    send.disabled = true;
    send.textContent = "THINKING...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                question: question,
                history: chat.apiHistory
            })
        });

        if (!response.ok) {
            throw new Error("Server returned an error");
        }

        const data = await response.json();

        // Keep each conversation's context separate.
        chat.apiHistory = data.history || chat.apiHistory;

        addMessage(
            data.answer || "I'm not sure how to answer that yet.",
            "bot",
            data.links || []
        );

    } catch (error) {
        addMessage(
            "Oops! I couldn't connect right now. Please try again! 😭",
            "bot"
        );
    } finally {
        busy = false;
        send.disabled = false;
        send.textContent = "SEND 🚀";
        input.focus();
    }
});

function loadChats() {
    try {
        const saved = localStorage.getItem(STORAGE_KEY);
        const parsed = saved ? JSON.parse(saved) : [];

        if (Array.isArray(parsed)) {
            chats = parsed.filter(chat =>
                chat &&
                typeof chat.id === "string" &&
                typeof chat.title === "string" &&
                Array.isArray(chat.messages)
            );
        }
    } catch (error) {
        chats = [];
    }

    if (chats.length === 0) {
        createChat();
    } else {
        activeChatId = chats[0].id;
        renderChatList();
        renderMessages();
    }
}

loadChats();
</script>
</body>
</html>
"""


def get_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NyvexiaIA/3.0 (chat application)"}
    )
    with urllib.request.urlopen(req, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[?!.,]+", "", text)
    return re.sub(r"\s+", " ", text)


def calculate(question):
    q = normalize(question)
    q = re.sub(r"^(what is|calculate)\s+", "", q)
    q = q.replace(" x ", " * ")

    match = re.fullmatch(
        r"(-?\d+(?:\.\d+)?)\s*([+*/-])\s*(-?\d+(?:\.\d+)?)",
        q
    )

    if not match:
        return None

    a = float(match.group(1))
    op = match.group(2)
    b = float(match.group(3))

    if op == "/" and b == 0:
        return "You can't divide by zero!"

    result = {
        "+": lambda: a + b,
        "-": lambda: a - b,
        "*": lambda: a * b,
        "/": lambda: a / b
    }[op]()

    if result == int(result):
        result = int(result)

    return "The answer is " + str(result) + "! 🧠"


def chat_reply(question, history):
    q = normalize(question)
    lower = question.lower().strip()

    greetings = {
        "hi", "hello", "hey", "heyy", "heyyy", "hii", "hiii",
        "yo", "sup", "wassup", "what's up", "whats up",
        "hello nyvexia", "hi nyvexia", "good morning",
        "good afternoon", "good evening"
    }

    if q in greetings:
        return random.choice([
            "Heyyy! 😎 What's up?",
            "Hiii! 👋 How's your day going?",
            "Yo! 🔥 What are we talking about today?",
            "Hellooo! 🚀 I'm here!"
        ]), []

    if q in {"how are you", "how are you doing", "hows it going"}:
        return "I'm doing great! 😎 How about you?", []

    if q in {
        "who are you", "what are you", "what is your name",
        "whats your name"
    }:
        return "I'm Nyvexia IA! 🚀 Your digital buddy. I can chat and look up information on Wikipedia.", []

    if q in {"thanks", "thank you", "thx", "ty", "thank you so much"}:
        return random.choice([
            "Anytime! 😎",
            "You're welcome! 💜",
            "No problem! Happy to help!"
        ]), []

    if q in {"bye", "goodbye", "see ya", "see you later"}:
        return "Byeeee! 👋 Come back anytime!", []

    if q in {"ok", "okay", "alright", "sure", "got it"}:
        return "Got you! 😎", []

    if re.fullmatch(r"(lol+|lmao+|haha+|hehe+|😂+|😭+)", q):
        return random.choice([
            "LMAOOO 😭😂",
            "BROOO 💀",
            "😂😂 I'm listening!"
        ]), []

    result = calculate(question)
    if result is not None:
        return result, []

    if re.search(
        r"\b(i am|i'm|im) (bored|tired|sad|happy|excited|angry|confused)\b",
        lower
    ):
        if "bored" in lower:
            return "Boredom alert 😭 Want to chat, hear a fun fact, or play a game?", []
        if "tired" in lower:
            return "Sounds like you've had a long day. 😴 Want to talk about it?", []
        if any(word in lower for word in ("sad", "angry", "confused")):
            return "I'm here to listen. 💜 What happened?", []
        return "YOOO, that's awesome! 🔥 What happened?", []

    if lower.startswith(("guess what", "you know what")):
        return "WHATTT? 👀 Tell me!", []

    previous_question = ""
    previous_answer = ""

    if history:
        last = history[-1]
        if isinstance(last, dict):
            previous_question = str(last.get("question", ""))
            previous_answer = str(last.get("answer", ""))

    followups = {
        "tell me more", "explain more", "why", "why is that",
        "how so", "what do you mean", "continue"
    }

    if q in followups and previous_answer:
        return None, []

    if q in {"what about him", "what about her", "what about it"}:
        if previous_question:
            return None, []

    statement_starts = (
        "i feel ", "i think ", "i want ", "i need ", "i like ",
        "i love ", "i hate ", "i wish ", "i have ", "i got ",
        "i went ", "i saw ", "my day ", "today i ", "my friend ",
        "my life ", "i'm ", "im "
    )

    if lower.startswith(statement_starts):
        if any(phrase in lower for phrase in (
            "i want to know", "i need to know", "i want to learn",
            "i need help", "i think what"
        )):
            return None, []

        return random.choice([
            "I'm listening! 👀 Tell me more.",
            "Oh really? 💜 What happened?",
            "I hear you. Go on, I'm listening!"
        ]), []

    question_starts = (
        "what ", "what's ", "whats ", "who ", "where ", "when ",
        "why ", "how ", "which ", "can you ", "could you ",
        "do you ", "does ", "did ", "is ", "are ", "was ", "were ",
        "will ", "would ", "should ", "explain ", "tell me ",
        "define ", "search for ", "find "
    )

    if lower.startswith(question_starts) or lower.endswith("?"):
        return None, []

    if len(q.split()) <= 5:
        return random.choice([
            "I hear you 😎 Tell me a little more!",
            "Oh really? 👀 Go on!",
            "I'm listening! 💜"
        ]), []

    return None, []


def wikipedia_search(question, history):
    q = normalize(question)
    search_question = question.strip()

    if history:
        last = history[-1]
        if isinstance(last, dict):
            previous_question = str(last.get("question", "")).strip()

            if q in {
                "tell me more", "explain more", "why",
                "why is that", "how so", "what do you mean",
                "continue", "what about him", "what about her",
                "what about it"
            } and previous_question:
                search_question = previous_question

    search_query = re.sub(
        r"^(what is|what are|who is|who was|who are|where is|"
        r"where are|when did|when was|when is|why is|why are|"
        r"how does|how do|how did|explain|tell me about|"
        r"define|search for|find)\s+",
        "",
        search_question,
        flags=re.IGNORECASE
    ).strip(" ?.!")

    capital_match = re.search(r"capital of (?:the )?(.+)", q)

    if capital_match:
        country = capital_match.group(1).strip()
        country = re.sub(
            r"\b(please|thanks|thank you)\b", "", country
        ).strip()
        search_query = country + " capital"

    params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": search_query or search_question,
        "format": "json",
        "srlimit": 5
    })

    data = get_json(WIKIPEDIA_API + "?" + params)
    results = data.get("query", {}).get("search", [])

    if not results:
        return "I couldn't find a useful Wikipedia page for that. Try asking another way! 💜", []

    title = results[0]["title"]

    details_params = urllib.parse.urlencode({
        "action": "query",
        "prop": "extracts",
        "explaintext": 1,
        "exintro": 1,
        "exchars": 2200,
        "titles": title,
        "format": "json"
    })

    details = get_json(WIKIPEDIA_API + "?" + details_params)
    pages = details.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})

    extract = re.sub(
        r"\s+", " ",
        html.unescape(page.get("extract", ""))
    ).strip()

    if not extract:
        answer = "I found a Wikipedia page, but it has no summary available."
    else:
        sentences = re.split(r"(?<=[.!?])\s+", extract)
        answer = " ".join(sentences[:3])

    links = []

    for item in results[:3]:
        article = urllib.parse.quote(
            item["title"].replace(" ", "_")
        )
        links.append({
            "title": item["title"],
            "url": "https://en.wikipedia.org/wiki/" + article
        })

    return answer, links


@app.route("/")
def home():
    return render_template_string(HTML_PAGE)


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()[:500]

    if not question:
        return jsonify({
            "answer": "Type something and let's chat! 😎",
            "links": [],
            "history": []
        })

    history = data.get("history", [])

    if not isinstance(history, list):
        history = []

    history = [
        item for item in history[-10:]
        if isinstance(item, dict)
    ]

    try:
        answer, links = chat_reply(question, history)

        if answer is None:
            answer, links = wikipedia_search(question, history)

        history.append({
            "question": question,
            "answer": answer
        })

        return jsonify({
            "answer": answer,
            "links": links,
            "history": history[-10:]
        })

    except Exception:
        return jsonify({
            "answer": "I couldn't reach Wikipedia right now. Please try again! 😭",
            "links": [],
            "history": history[-10:]
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
