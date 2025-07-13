# 🧠 AI Lead Scoring Dashboard

An end-to-end web-based lead scoring system that predicts prospect intent using a trained machine learning model and a rule-based LLM-inspired re-ranker.

---

## 📌 Problem Statement

Sales teams often waste valuable time on low-intent leads, slowing down the conversion pipeline. This dashboard provides an **Intent Score (0–100)** to help prioritize high-intent leads, improving conversion efficiency by 2–3x.

---

## 🎯 Features

- 🔮 Predicts lead intent using a **Gradient Boosting Classifier**
- 🧾 Re-ranks the intent score based on **comments using rules inspired by LLMs**
- 📋 Single-page web UI for data input and score visualization
- ⚡ FastAPI backend for scoring
- 🚀 Deployed using **Netlify (frontend)** and **Render (backend)**

---

## 🏗️ Architecture

User Form (HTML + JS)
↓
Flask Frontend
↓
FastAPI Endpoint (/score)
↓
ML Model (.pkl) + Preprocessor Pipeline
↓
Re-ranker (based on keywords in comments)
↓
JSON Response with Initial + Reranked Scores


---

## 🧪 Tech Stack

- 🧠 ML: `scikit-learn`, `GradientBoostingClassifier`
- 🧱 Backend: `FastAPI`, `joblib`, `Pydantic`
- 🌐 Frontend: `HTML`, `CSS`, `JavaScript`, `Flask`
- ⚙️ DevOps: `Render`, `Netlify`, `GitHub`

---
---

## ⚙️ Setup Instructions

### 🔧 Backend Setup (FastAPI)

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run FastAPI backend
uvicorn main:app --reload
```
---

## 🧬 Dataset

- ✅ Synthetic dataset with 10,000 leads
- ✅ Features include:
  - `email`, `phone_number` (dummy fields)
  - `age`, `income`, `credit_score`
  - `age_group`, `family_background`
  - `comments`, `intent` (target)

---

## 🤖 ML Model

- Trained using:
  - `GradientBoostingClassifier`
  - 80-20 train-test split
  - Scaled prediction to 0–100
- Accuracy: **83%**

---

## 📈 Re-Ranker Logic

```python
comment = comment.lower()
if "urgent" in comment:
    score += 10
if "not interested" in comment:
    score -= 10
if "call me" in comment or "interested" in comment:
    score += 5
```
---
## Input and Output 

<img width="777" height="893" alt="image" src="https://github.com/user-attachments/assets/b9c2ffd8-4204-4f96-8329-3f4963634ab1" /> 

<img width="742" height="284" alt="image" src="https://github.com/user-attachments/assets/8d05869f-fc2f-47cc-98b2-a1865f6f7e78" />

