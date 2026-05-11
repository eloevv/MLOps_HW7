import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()
MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")

try:
    model = joblib.load("artifacts/model.pkl")
except Exception:
    model = None


class PredictRequest(BaseModel):
    x: List[float]


@app.get("/health")
def health():
    return {"status": "ok", "version": MODEL_VERSION}


@app.post("/predict")
def predict(req: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    try:
        x = np.array(req.x).reshape(1, -1)
        prediction = int(model.predict(x)[0])
        return {"prediction": prediction, "version": MODEL_VERSION}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
