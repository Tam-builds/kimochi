from flask import Flask, request, jsonify, render_template
import time, re

app = Flask(__name__)

# ── Model loading ────────────────────────────────────────────────
print("⏳ Loading sentiment model...")
from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True, max_length=512
)

emotion_model = pipeline(
    "text-classification",
    model="bhadresh-savani/distilbert-base-uncased-emotion",
    truncation=True, max_length=512,
    top_k=None   # return ALL emotion scores
)
print("✦ Models ready!")

# ── Constants ────────────────────────────────────────────────────
SENTIMENT_EMOJI = {"POSITIVE": "😊", "NEGATIVE": "😔", "NEUTRAL": "😐"}
EMOTION_EMOJI   = {
    "joy":      "😄", "sadness": "😢", "anger":    "😠",
    "fear":     "😨", "surprise":"😲", "love":     "🥰",
}
EMOTION_COLOR = {
    "joy":      "#F59E0B", "sadness": "#3B82F6", "anger":   "#EF4444",
    "fear":     "#8B5CF6", "surprise":"#EC4899",  "love":   "#F43F5E",
}

# ── Helpers ──────────────────────────────────────────────────────
def get_sentiment(text: str) -> dict:
    r = sentiment_model(text[:512])[0]
    label = r["label"].upper()
    score = round(r["score"] * 100, 1)
    if score < 60:
        label = "NEUTRAL"
    return {"label": label, "score": score, "emoji": SENTIMENT_EMOJI[label]}

def get_emotions(text: str) -> list:
    results = emotion_model(text[:512])[0]
    emotions = sorted(results, key=lambda x: x["score"], reverse=True)
    return [
        {
            "label": e["label"],
            "score": round(e["score"] * 100, 1),
            "emoji": EMOTION_EMOJI.get(e["label"], "✨"),
            "color": EMOTION_COLOR.get(e["label"], "#7C3AED"),
        }
        for e in emotions
    ]

def split_sentences(text: str) -> list:
    raw = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in raw if len(s.strip()) > 3]

def analyze_full(text: str) -> dict:
    start = time.time()

    sentiment  = get_sentiment(text)
    emotions   = get_emotions(text)
    sentences  = split_sentences(text)

    # per-sentence sentiment
    sent_results = []
    for s in sentences[:15]:   # cap at 15 sentences
        sr = get_sentiment(s)
        sent_results.append({
            "text":  s,
            "label": sr["label"],
            "score": sr["score"],
            "emoji": sr["emoji"],
        })

    elapsed = round((time.time() - start) * 1000)

    return {
        "sentiment":   sentiment,
        "emotions":    emotions,
        "top_emotion": emotions[0] if emotions else {},
        "sentences":   sent_results,
        "stats": {
            "word_count":      len(text.split()),
            "char_count":      len(text),
            "sentence_count":  len(sentences),
            "time_ms":         elapsed,
            "avg_word_length": round(
                sum(len(w) for w in text.split()) / max(len(text.split()), 1), 1
            ),
        }
    }

# ── Routes ───────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze_route():
    data = request.get_json()
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400
    if len(text) > 5000:
        return jsonify({"error": "Max 5000 characters"}), 400
    try:
        return jsonify(analyze_full(text))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/analyze/compare", methods=["POST"])
def compare_route():
    data  = request.get_json()
    text1 = (data.get("text1") or "").strip()
    text2 = (data.get("text2") or "").strip()
    if not text1 or not text2:
        return jsonify({"error": "Both texts required"}), 400
    return jsonify({
        "result1": analyze_full(text1),
        "result2": analyze_full(text2),
    })

@app.route("/analyze/bulk", methods=["POST"])
def bulk_route():
    data  = request.get_json()
    texts = data.get("texts", [])
    if not texts or len(texts) > 20:
        return jsonify({"error": "Provide 1–20 texts"}), 400
    return jsonify([analyze_full(t[:512]) for t in texts if t.strip()])

if __name__ == "__main__":
    app.run(debug=True, port=5001)
