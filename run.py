#!/usr/bin/env python3
import os
import sys
import uvicorn

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Prevent Python from writing .pyc files
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[project_root]
    ) 