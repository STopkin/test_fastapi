from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .sql import crud, models, schemas
from .sql.database import SessionLocal, engine
import json


models.Base.metadata.create_all(bind=engine)


app = FastAPI(swagger_ui_parameters={"deepLinking": False, "syntaxHighlight.theme": "obsidian"})


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

# получить автора и список его публикаций по ID
@app.get("/author/{author_id}", response_model=schemas.Author)
async def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_author

    
# создать автора
@app.post("/author", response_model=schemas.Author)
async def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author_by_email(db, email=author.email)
    if db_author:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_author(db=db, author=author)    
    
    
# создать публикацию у автора    
@app.post("/author/{author_id}")
async def create_post(author_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_author = crud.get_author(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_author_post(db, post, author_id)

    
# получить всех авторов и кол-во публикаций
@app.get("/authors")
async def get_authors_and_posts(db: Session = Depends(get_db)):
    return crud.get_author_and_post_count(db)
    
    