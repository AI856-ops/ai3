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
* { box-sizing: border-box; }
body {
    margin: 0; font-family: Arial, sans-serif;
    background: #080d1b; color: white;
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
header h1 { margin: 0; color: #71c7ff; }
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
.bot { background: #1b2943; align-self: flex-start; }
.user { background: #185d91; align-self: flex-end; }
#form {
    display: flex; gap: 10px; padding: 16px;
    border-top: 1px solid #263958;
}
input {
    flex: 1; min-width: 0; padding: 14px;
    border-radius: 10px; border: 1px solid #405574;
    background: #080d1b; color: white; font-size: 16px;
}
button {
    padding: 0 20px; border: 0; border-radius: 10px;
    background: #36a9f5; color: #07111f;
    font-weight: bold; cursor: pointer;
}
button:disabled { opacity: .5; }
a { color: #71c7ff; }
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
Ask me anything and let's explore the world! 🔥</div>
</div>
<form id="form">
<input id="question" placeholder="Ask Nyvexia anything..." autocomplete="off" required>
<button id="send" type="submit">SEND 🚀</button>
</form>
</div>
<script>
const messages = document.getElementById("messages");
const form = document.getElementById("form");
const input = document.getElementById("question");
const send = document.getElementById("send");

function addMessage(text, who, links=[]) {
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
            body: JSON.stringify({question})
        });
        const data = await response.json();
        addMessage(data.answer || "Sorry, I couldn't find an answer!", "bot", data.links || []);
    } catch (error) {
        addMessage("Oops! I couldn't connect. Please try again. 😭", "bot");
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
        url, headers={"User-Agent": "NyvexiaIA/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[?!.,]+", "", text)
    return re.sub(r"\s+", " ", text)


def chat_reply(question):
    q = normalize(question)

    greetings = {
        "hi", "hello", "hey", "heyy", "heyyy", "hii",
        "hiii", "yo", "sup", "wassup", "what's up",
        "whats up", "hello nyvexia", "hi nyvexia",
        "good morning", "good afternoon", "good evening"
    }

    if q in greetings:
        return random.choice([
            "Heyyy! 😎 What's up?",
            "Hiii! 👋 Welcome back!",
            "Yo brooo! 🔥 What are we doing today?",
            "Hellooo! 🚀 Ready to explore something?"
        ]), []

    if q in {"how are you", "how are you doing", "hows it going"}:
        return "I'm doing great! 😎 Ready for your questions!", []

    if q in {"who are you", "what are you", "what is your name",
             "whats your name"}:
        return "I'm Nyvexia IA! 🚀 Your Python-powered digital buddy!", []

    if q in {"thanks", "thank you", "thx", "ty"}:
        return "Anytime! 😎 Ask me something else!", []

    if q in {"bye", "goodbye", "see ya"}:
        return "Byeeee! 👋 Come back anytime!", []

    math_match = re.fullmatch(
        r"(-?\d+(?:\.\d+)?)\s*([+*/-])\s*(-?\d+(?:\.\d+)?)", q
    )
    if math_match:
        a = float(math_match.group(1))
        op = math_match.group(2)
        b = float(math_match.group(3))
        if op == "/" and b == 0:
            return "You can't divide by zero!", []
        result = {"+": lambda: a+b, "-": lambda: a-b,
                  "*": lambda: a*b, "/": lambda: a/b}[op]()
        if result == int(result):
            result = int(result)
        return "The answer is " + str(result) + "! 🧠", []

    return None, []


def wikipedia_search(question):
    params = urllib.parse.urlencode({
        "action": "query", "list": "search",
        "srsearch": question, "format": "json", "srlimit": 5
    })
    data = get_json(WIKIPEDIA_API + "?" + params)
    results = data.get("query", {}).get("search", [])
    if not results:
        return "Sorry, I couldn't find a Wikipedia result! 😭", []

    q = normalize(question)
    title = results[0]["title"]
    answer_title = title
    links = []

    # For questions about capitals, prefer a result about the city
    capital_match = re.search(r"capital of (?:the )?(.+)", q)
    if capital_match:
        country = capital_match.group(1).strip()
        country = re.sub(r"\b(please|thanks|thank you)\b", "", country).strip()
        params2 = urllib.parse.urlencode({
            "action": "query", "list": "search",
            "srsearch": country + " capital city",
            "format": "json", "srlimit": 5
        })
        try:
            data2 = get_json(WIKIPEDIA_API + "?" + params2)
            candidates = data2.get("query", {}).get("search", [])
            for candidate in candidates:
                t = candidate["title"]
                snippet = html.unescape(
                    re.sub("<.*?>", "", candidate.get("snippet", ""))
                ).lower()
                if "capital" in snippet or "capital" in t.lower():
                    answer_title = t
                    break
        except Exception:
            pass

    details_params = urllib.parse.urlencode({
        "action": "query", "prop": "extracts",
        "explaintext": 1, "exintro": 1, "exchars": 2200,
        "titles": answer_title, "format": "json"
    })
    details = get_json(WIKIPEDIA_API + "?" + details_params)
    pages = details.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    extract = re.sub(r"\s+", " ", html.unescape(
        page.get("extract", "")
    )).strip()

    if not extract:
        extract = "I found a Wikipedia page, but it has no summary."

    sentences = re.split(r"(?<=[.!?])\s+", extract)
    answer = " ".join(sentences[:4])

    for item in results[:3]:
        article = urllib.parse.quote(item["title"].replace(" ", "_"))
        links.append({
            "title": item["title"],
            "url": "https://en.wikipedia.org/wiki/" + article
        })

    if answer_title != title:
        article = urllib.parse.quote(answer_title.replace(" ", "_"))
        links.insert(0, {
            "title": answer_title,
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
        return jsonify({"answer": "Type a question first!", "links": []})

    try:
        answer, links = chat_reply(question)
        if answer is None:
            answer, links = wikipedia_search(question)
        return jsonify({"answer": answer, "links": links})
    except Exception:
        return jsonify({
            "answer": "Oops! I couldn't reach Wikipedia right now. Please try again! 😭",
            "links": []
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
