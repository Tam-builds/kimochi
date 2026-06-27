# Kimochi ✦ v2 — Sentiment & Emotion AI

Upgraded sentiment analyser with **dual NLP models**, emotion detection, sentence breakdown, compare mode, and export.

## What's new in v2

| Feature               | v1 | v2 |
|-----------------------|----|----|
| Sentiment (Pos/Neg)   | ✅ | ✅ |
| 6-Emotion Detection   | ❌ | ✅ |
| Sentence Breakdown    | ❌ | ✅ |
| Compare Two Texts     | ❌ | ✅ |
| Live Debounced Input  | ❌ | ✅ |
| History with Reload   | ✅ | ✅ |
| Export JSON           | ❌ | ✅ |
| Bulk API              | ✅ | ✅ |
| Compare API           | ❌ | ✅ |

## Models Used

| Model | Purpose |
|-------|---------|
| `distilbert-base-uncased-finetuned-sst-2-english` | Sentiment (Positive/Negative) |
| `bhadresh-savani/distilbert-base-uncased-emotion` | Emotions (joy, sadness, anger, fear, surprise, love) |

## Run Locally

```bash
cd kimochi-v2
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
# open http://localhost:5001
```

> First run downloads ~500MB of models. Subsequent runs are instant.

## API

### POST /analyze
```json
{ "text": "I absolutely love this!" }
```

### POST /analyze/compare
```json
{ "text1": "Amazing product!", "text2": "Terrible experience" }
```

### POST /analyze/bulk
```json
{ "texts": ["Great!", "Awful", "Okay"] }
```

## Resume Line
> Built Kimochi v2 — NLP sentiment + emotion analysis app using dual DistilBERT models (HuggingFace). Features sentence breakdown, compare mode, REST API, and export. Deployed on Render.
