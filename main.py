from fastapi import FastAPI, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

posts = []
files_dir = "uploads"
os.makedirs(files_dir, exist_ok=True)

class Post(BaseModel):
    user: str
    content: str

@app.post("/post")
def create_post(post: Post):
    posts.append(post.dict())
    return {"message": "Post created", "data": post}

@app.get("/posts")
def get_posts():
    return posts

@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(files_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"message": "File uploaded", "filename": file.filename}

@app.get("/files")
def list_files():
    return os.listdir(files_dir)

@app.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message received: {data}")
