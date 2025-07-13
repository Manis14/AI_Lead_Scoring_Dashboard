from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, EmailStr, Field
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import pandas as pd
import joblib
import os

# Load model and preprocessor
model = joblib.load("model/intent_model.pkl")
preprocessor = joblib.load("model/preprocessor_pipeline.pkl")

app = FastAPI()

# Static + Template setup
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# In-memory storage
stored_leads = []

class LeadInput(BaseModel):
    email: EmailStr
    phone_number: str
    age: int = Field(..., gt=0)
    credit_score: int = Field(..., ge=300, le=850)
    income: float
    age_group: str
    family_background: str
    comments: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/submit", response_class=HTMLResponse)
async def submit_lead(request: Request):
    form = await request.form()
    lead_data = {
        "email": form.get("email"),
        "phone_number": form.get("phone_number"),
        "age": int(form.get("age")),
        "credit_score": int(form.get("credit_score")),
        "income": float(form.get("income")),
        "age_group": form.get("age_group"),
        "family_background": form.get("family_background"),
        "comments": form.get("comments"),
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([{
        "age": lead_data["age"],
        "credit_score": lead_data["credit_score"],
        "income": lead_data["income"],
        "age_group": lead_data["age_group"],
        "family_background": lead_data["family_background"]
    }])

    try:
        X_transformed = preprocessor.transform(input_df)
        prob = model.predict_proba(X_transformed)[0][1]
        initial_score = int(prob * 100)

        # Re-rank score based on comments
        comment = lead_data["comments"].lower()
        positive_keywords = ["urgent", "call me", "interested", "need", "important", "asap", "looking", "buy", "query",
                             "help", "need assistance"]
        negative_keywords = ["not interested", "no thanks", "leave me", "stop", "unsub", "spam", "don't call",
                             "wrong number", "go away"]


        adjustment = 0
        # Apply adjustments
        for keyword in positive_keywords:
            if keyword in comment:
                adjustment += 5

        for keyword in negative_keywords:
            if keyword in comment:
                adjustment -= 10
        # Final score calculation
        final_score = min(100, max(0, initial_score + adjustment))

        # Store and return
        result = {
            "email": lead_data["email"],
            "initial_score": initial_score,
            "reranked_score": final_score,
            "comment": lead_data["comments"]
        }
        stored_leads.append(result)
        return templates.TemplateResponse("index.html", {"request": request, "result": result})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
