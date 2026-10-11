from flask import Flask, request, jsonify, render_template_string
import urllib.request
import urllib.parse
import json
import html
import re
import random

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
  --cyan: #22D3EE;
  --pink: #F472B6;
  --background: #101426;
}
* { box-sizing: border-box; }
body {
  margin: 0; font-family: Arial, sans-serif;
  background: var(--background); color: white;
  min-height: 100vh; display: flex;
  justify-content: center; align-items: center;
}
.chat {
  width: 100%; max-width: 850px; height: 95vh;
  display: flex; flex-direction: column;
  background: #10182b; border: 1px solid #263958;
  border-radius: 18px; overflow: hidden;
}
header {
  padding: 22px; text-align: center;
  background: #151f38; border-bottom: 1px solid #263958;
}
header h1 {
  margin: 0; color: var(--purple);
  text-shadow: 0 0 18px #8B5CF655;
}
header p { color: #a8b7d3; margin-bottom: 0; }
#messages {
  flex: 1; overflow-y: auto; padding: 22px;
  display: flex; flex-direction: column; gap: 15px;
}
.message {
  padding: 13px 16px; border-radius: 14px;
  max-width: 90%; line-height: 1.5;
  white-space: pre-wrap; overflow-wrap: anywhere;
}
.bot {
  background: #1b2943; border: 1px solid #8B5CF633;
  align-self: flex-start;
}
.user {
  background: #31245c; border: 1px solid var(--purple);
  align-self: flex-end;
}
#form {
  display: flex; gap: 10px; padding: 16px;
  border-top: 1px solid #263958;
}
input {
  flex: 1; min-width: 0; padding: 14px;
  border-radius: 10px; border: 1px solid #405574;
  background: #080d1b; color: white; font-size: 16px;
}
input:focus {
  outline: none; border-color: var(--cyan);
  box-shadow: 0 0 10px #22D3EE33;
}
button {
  padding: 0 20px; border: 0; border-radius: 10px;
  background: linear-gradient(135deg, var(--purple), var(--pink));
  color: white; font-weight: bold; cursor: pointer;
}
button:disabled { opacity: .5; }
a { color: var(--cyan); }
@media(max-width: 550px) {
  .chat { height: 100vh; border-radius: 0; }
  header { padding: 16px; }
  #messages { padding: 14px; }
  #form { padding: 10px; }
  button { padding: 0 13px; }
}
</style>
</head>
<body>
<div class="chat">
<header>
<h1>NYVEXIA IA 🚀</h1>
<p>Your digital buddy • Powered by Wikipedia</p>
</header>

<div id="messages">
<div class="message bot">Heyyy! 👋 Welcome to Nyvexia IA!
Ask questions or just talk to me. I'm listening! 🔥</div>
</div>

<form id="form">
<input id="question" placeholder="Talk to Nyvexia..." autocomplete="off" required>
<button id="send" type="submit">SEND 🚀</button>
</form>
</div>

<script>
const messages = document.getElementById("messages");
const form = document.getElementById("form");
const input = document.getElementById("question");
const send = document.getElementById("send");

let history = [];

function addMessage(text, who, links = []) {
    const box = document.createElement("div");
    box.className = "message " + who;
    box.textContent = text;
    messages.appendChild(box);

    links.forEach(link => {
        const a = document.createElement("a");
        a.href = link.url;
        a.target = "_blank";
        a.rel = "noopener noreferrer";
        a.textContent = "🔗 " + link.title;
        a.style.display = "block";
        a.style.margin = "5px 0 5px 12px";
        messages.appendChild(a);
    });

    messages.scrollTop = messages.scrollHeight;
}

form.addEventListener("submit", async event => {
    event.preventDefault();

    const question = input.value.trim();
    if (!question) return;

    addMessage(question, "user");
    input.value = "";
    send.disabled = true;
    send.textContent = "THINKING...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                question: question,
                history: history
            })
        });

        if (!response.ok) {
            throw new Error("Server returned an error");
        }

        const data = await response.json();

        history = data.history || history;

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
    }

    send.disabled = false;
    send.textContent = "SEND 🚀";
    input.focus();
});
</script>
</body>
</html>
"""


def get_json(url):
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "NyvexiaIA/2.0"}
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

    if q in {"who are you", "what are you", "what is your name",
             "whats your name"}:
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

    # Use recent context for simple follow-up questions.
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
        # Search the previous topic again to provide more information.
        return None, []

    if q in {"what about him", "what about her", "what about it"}:
        if previous_question:
            return None, []

    # Personal statements should usually get a conversational reply.
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

    # Only send likely information requests to Wikipedia.
    question_starts = (
        "what ", "what's ", "whats ", "who ", "where ", "when ",
        "why ", "how ", "which ", "can you ", "could you ",
        "do you ", "does ", "did ", "is ", "are ", "was ", "were ",
        "will ", "would ", "should ", "explain ", "tell me ",
        "define ", "search for ", "find "
    )

    if lower.startswith(question_starts):
        return None, []

    if lower.endswith("?"):
        return None, []

    # Don't search random short messages or statements.
    if len(q.split()) <= 5:
        return random.choice([
            "I hear you 😎 Tell me a little more!",
            "Oh really? 👀 Go on!",
            "I'm listening! 💜"
        ]), []

    return None, []


def wikipedia_search(question, history):
    q = normalize(question)

    # Interpret simple follow-up questions using the previous topic.
    search_question = question.strip()

    if history:
        last = history[-1]
        if isinstance(last, dict):
            previous_question = str(last.get("question", "")).strip()
            previous_answer = str(last.get("answer", "")).strip()

            if q in {
                "tell me more", "explain more", "why",
                "why is that", "how so", "what do you mean",
                "continue"
            } and previous_question:
                search_question = previous_question

            elif q in {
                "what about him", "what about her", "what about it"
            } and previous_question:
                search_question = previous_question

    # Remove conversational prefixes so the search focuses on the subject.
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

    # Keep only recent, valid messages.
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
