"""
main.py
--------
FastAPI server for the Drawing Idea Generator.
Handles CORS for the Next.js frontend.
"""

import os
from typing import Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from prompt_engine import Category, Difficulty, Mood, generate
from pydantic import BaseModel

app = FastAPI(title="Drawing Idea Generator API", version="1.0.0")

# ── CORS ───────────────────────────────────────────────────────────────
# Allow requests from the Next.js frontend

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # local dev
        "https://jdr2v.github.io",  # production
    ],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Request / Response models ──────────────────────────────────────────


class GenerateRequest(BaseModel):
    category: Optional[str] = "any"
    difficulty: Optional[str] = "study"
    mood: Optional[str] = "any"


class GenerateResponse(BaseModel):
    prompt: str
    subject: str
    category: str
    modifiers: list[str]
    difficulty: str
    mood: str
    source: str


# ── Routes ─────────────────────────────────────────────────────────────


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/generate", response_model=GenerateResponse)
def generate_prompt(body: GenerateRequest):
    result = generate(
        category=body.category,
        difficulty=body.difficulty,
        mood=body.mood,
    )
    return result
