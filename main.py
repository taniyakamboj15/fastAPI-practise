from fastapi import FastAPI
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

a = os.getenv("SECURITY_CODE");

@app.get("/")
def root():
    return {"message": "FastAPI backend running on macOS 🚀"}

@app.get("/health")
def health_check():
    return {"status": a}
