from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from src.routers import chat, upload

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(chat.router)
app.include_router(upload.router)


@app.get("/")
def root() -> JSONResponse:
    return FileResponse("src/static/index.html")


@app.get("/admin")
def admin() -> JSONResponse:
    return FileResponse("src/static/admin.html")
