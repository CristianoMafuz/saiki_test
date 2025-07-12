"""
backend/main.py

Runs the backend server.
"""

# for uvicorn
from src.backend.api import app
from src.backend.db import *

"""
Setup running:
> uvicorn backend.main:app
"""


if __name__ == "__main__":
    pass
