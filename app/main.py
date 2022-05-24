# from typing import List

from fastapi import Depends, FastAPI, HTTPException
# from sqlalchemy.orm import Session

# from .sql import crud, models, schemas
# from .sql.database import SessionLocal, engine
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


# получить автора и список его публикаций по ID
@app.get("/author/{author_id}")
async def get_author(author_id: int):
    '''
    Получить информацию по автору и список его публикаций по author_id
    '''
#    db_author = crud.get_author(db, author_id)
#    if not db_author:
#        raise HTTPException(status_code=404, detail="Author not found")
    db_author = None
    return db_author

    
# создать автора
@app.post("/author")
async def create_author(author: schemas.AuthorCreate):
    ''' создать автора '''
    db_author = crud.get_author_by_email(db, email=author.email)
    if db_author:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_author(db=db, author=author)    
    
    
# создать публикацию у автора    
@app.post("/author/{author_id}")
async def create_post(author_id: int, post: schemas.PostCreate):
    ''' создать публикацию у автора '''
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_author_post(db, post, author_id)

    
# получить всех авторов и кол-во публикаций
@app.get("/authors")
async def get_authors_and_posts():
    ''' получить всех авторов и кол-во публикаций '''
    return crud.get_author_and_post_count(db)
    
    