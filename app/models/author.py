from sqlalchemy import Column, Table, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, Query

from database import Base, database
from .post import Post


class AuthorManager:
    def __init__(self, model_cls):
        self.table: Table = model_cls.__table__

    async def get_author(self, author_id: int):
        query = self.table.select(Author.id == author_id)
        author_record = await database.fetch_one(query)
        if author_record is None:
            return False

        author = Author(**author_record)
        query = Post.objects.table.select(Post.author_id == author_id)
        posts = await database.fetch_all(query)
        return {"author": author, "posts": posts}

    @staticmethod
    async def get_all_authors():
        query = """SELECT a.*, COUNT(p.*) as posts
        FROM authors a LEFT JOIN posts p ON a.id=p.author_id 
        GROUP BY a.id, a.name, a.email, a.created_at
        ORDER BY a.id"""
        rows = await database.fetch_all(query)
        return rows

    async def find_by_email(self, email: str):
        query = self.table.select().where(self.table.c.email == email)
        return await database.fetch_one(query)

    async def find_by_id(self, author_id: int):
        query = self.table.select().where(self.table.c.id == author_id)
        return await database.fetch_one(query)

    @staticmethod
    async def email_exists(email):
        sub = Query(Author).filter(Author.email == email).exists()
        return await database.fetch_val(Query(sub).statement)

    async def create_author(self, name: str, email: str):
        email_exists = await self.__class__.email_exists(email)
        if not email_exists:
            return await database.fetch_one(self.table.insert().values(name=name, email=email).returning(self.table.c.id))
        raise Exception(f"Author with email={email} already exists")


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    posts = relationship("Post", back_populates="author")

    objects: AuthorManager = None


Author.objects = AuthorManager(model_cls=Author)
