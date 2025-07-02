from fastapi import FastAPI
from .api.routes import router as api_router
app = FastAPI()
app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    print("✅ FastAPI запущен")