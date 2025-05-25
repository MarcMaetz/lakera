from fastapi import FastAPI
import uvicorn
from src.moderation.api import router

app = FastAPI(title="Content Moderation API")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 