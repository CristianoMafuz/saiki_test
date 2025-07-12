"""
backend/api/req.py

Requests via FastAPI~

(deprecated~)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or list your frontend URLs
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/cmrd")
def read_root() -> dict[str, str]:
    return { 
        "msg": "Hello from backend! Camarada"
    }


@app.get("/api/hangar")
def read_root() -> dict[str, str]:
    return { 
        "msg": "Helicóptero"
    }
