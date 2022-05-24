from sqlalchemy import Column, Table, Integer, String, DateTime, join
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..database import Base, database


class AuthorManager:
    def __init__(self, model_cls):
        self.table: Table = model_cls.__table__

    async def get_author(self, author_id: int):
        query = self.table.select(Author.id == author_id)
        return await database.fetch_one(query)

    async def get_all_authors(self):
        query = self.table.select()
        return await database.fetch_all(query)

    async def find_by_email(self, email: str):
        query = self.table.select().where(self.table.c.email == email)
        return await database.fetch_one(query)

    async def email_exists(self, email: str):
        # return await database.fetch_val(self.table.count()) == 1
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #self.table.columns
        query = self.table.select(None, columns=[func.count()]).select_from(self.table).where(self.table.c.email == email)
        print(query)
        return await database.fetch_val(query) == 1

    async def create_author(self, name: str, email: str):
        return await database.fetch_one(self.table.insert().values(name=name, email=email))
        count = self.find_by_email(email)
        if count == 0:
            return await database.fetch_one(self.table.insert().values(name=name, email=email))
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
