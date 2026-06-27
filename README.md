---
title: Kimochi
emoji: 😊
colorFrom: pink
colorTo: purple
sdk: docker
pinned: false
license: mit
short_description: AI sentiment & emotion analyzer
---

# Kimochi ✦ v2 — Sentiment & Emotion AI

Upgraded sentiment analyser with **dual NLP models**, emotion detection, sentence breakdown, compare mode, and export.

## What's new in v2

| Feature | v1 | v2 |
|---------|----|----|
| Sentiment (Pos/Neg) | ✅ | ✅ |
| 6-Emotion Detection | ❌ | ✅ |
| Sentence Breakdown | ❌ | ✅ |
| Compare Two Texts | ❌ | ✅ |
| Live Debounced Input | ❌ | ✅ |
| History with Reload | ✅ | ✅ |
| Export JSON | ❌ | ✅ |
| Bulk API | ✅ | ✅ |
| Compare API | ❌ | ✅ |

## Models Used

| Model | Purpose |
|-------|---------|
| `distilbert-base-uncased-finetuned-sst-2-english` | Sentiment |
| `bhadresh-savani/distilbert-base-uncased-emotion` | Emotion Detection |

## Run Locally

```bash
python -m venv venv
pip install -r requirements.txt
python app.py
```

First run downloads the Hugging Face models.

## API

- `POST /analyze`
- `POST /analyze/compare`
- `POST /analyze/bulk`