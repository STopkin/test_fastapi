# from typing import List

from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session

# from .sql import crud, models, schemas
# from .sql.database import SessionLocal, engine
from .models import Author, Post
from .database import database


description = """
test_fastapi API это моё тестовое задание по fastapi

## Authors - авторы

Можно:
* создать автора, 
* получить информацию по автору, включая список его публикаций
* получить список всех авторов и количество его публикаций

## Posts - публикации

Можно:
* создать публикцию
"""


app = FastAPI(
    title="test_fastapi",
    description=description,
    version="0.0.1",
    #    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Toporkov Sergey",
        "url": "https://github.com/STopkin",
        "email": "stopkin0@gmail.com",
    },
    #    license_info={
    #        "name": "Apache 2.0",
    #        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    #    },
    swagger_ui_parameters={"deepLinking": False, "syntaxHighlight.theme": "obsidian"}
)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.get("/author/{author_id}")
async def get_author(author_id: int):
    """    Получить информацию по автору и список его публикаций по :author_id   """
    db_author = await Author.objects.get_author(author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail=f"Author {author_id} not found")
    return db_author

    
@app.post("/author")
async def create_author(name: str, email: str):
    """ создать автора
    :name - имя
    :email - email
    """
    if await Author.objects.email_exists(email):
        raise HTTPException(status_code=400, detail=f"Email {email} already registered")
    return await Author.objects.create_author(name, email)

    
@app.post("/author/{author_id}")
async def create_post(author_id: int, title: str):
    """ создать публикацию у автора
    :author_id - ID автора
    :title - заголовок публикации
    """
    db_author = await Author.objects.get_author(author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return await Post.objects.create_post(author_id, title)

    
@app.get("/authors")
async def get_authors_and_posts():
    """ получить всех авторов и кол-во публикаций """
    return await Author.objects.get_all_authors()
    
