from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from . import models, schemas


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_author_by_email(db: Session, email: str):
    return db.query(models.Author).filter(models.Author.email == email).first()
    
    
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, email=author.email)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author_and_post_count(db: Session, skip: int = 0, limit: int = 100):
#    return db.query(models.Author).offset(skip).limit(limit).all()
    return db.query(models.Author.id, models.Author.name, models.Author.email, models.Author.created_at, models.Author.posts_count).all() 
#, func.count(models.Post.id)).select_from(models.Author).join(models.Post, isouter=True).group_by(models.Author).all()
#    return db.query(models.Author.name, models.Author.email, func.count(models.Post.id)).join(models.Post, isouter=True).group_by(models.Author).all() 
#, func.count(models.Post.id)).select_from(models.Author).join(models.Post, isouter=True).group_by(models.Author).all()
#    .offset(skip).limit(limit).all()


def create_author_post(db: Session, post: schemas.PostCreate, author_id: int):
    db_post = models.Post(**post.dict(), author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
