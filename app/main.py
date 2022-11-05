from . import models, utils
from .database import engine
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from .routers import post, user, auth, vote

# disabilita quando usi alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


my_posts = [{"title": "title post1", "content": "content", "id": 1},
            {"title": "food", "content": "pizza", "id": 2}
            ]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/', response_class=HTMLResponse)
def root():
    return '<h1 style="font-family:verdana">Welcome to my FASTAPI</h1><h2>By D.Iannozzi</h2>'
