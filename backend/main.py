from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.detect import router as detect_router
from utils.cache import init_cache
from routes.admin import router as admin_router

app = FastAPI()

init_cache()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect_router)
app.include_router(admin_router)
@app.get("/")
def home():
    return {"message": "Misinformation Shield API is running 🚀"}



