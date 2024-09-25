from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles


from langchain_core.embeddings import Embeddings
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_google_community import BigQueryVectorStore

from routers import chat, upload



app = FastAPI()

app.add_middleware(middleware_class=CORSMiddleware,
                   allow_methods = ["*"],
                   allow_headers = ["*"])

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(chat.router)
app.include_router(upload.router)


@app.get("/")
def root() -> JSONResponse:
    return FileResponse("static/index.html")








