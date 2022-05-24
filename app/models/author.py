from sqlalchemy import Column, Table, Integer, String, DateTime, join, select
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from ..database import Base, database
from .post import Post

class AuthorManager:
    def __init__(self, model_cls):
        self.table: Table = model_cls.__table__

    async def get_author(self, author_id: int):
        # join_ = self.table.join(Post.objects.table,
        #                       onclause=self.table.c.id == Post.objects.table.c.author_id, isouter=True)
        # print(join_)
        query = self.table.select(Author.id == author_id)  # .select_from(join_)
        author_record = await database.fetch_one(query)
        if author_record is None:
            return False

        author = Author(**author_record)
        print(str(author))

        query2 = Post.objects.table.select(Post.author_id == author_id)
        print(query2)
        posts = await database.fetch_all(query2)
        print(str(posts))
        # .where(Author.id == author_id)
        return {"author": author, "posts": posts}

    @staticmethod
    async def get_all_authors():
        query = """SELECT a.*, COUNT(p.*) 
        FROM authors a LEFT JOIN posts p ON a.id=p.author_id 
        GROUP BY a.id, a.name, a.email, a.created_at
        ORDER BY a.id"""
        rows = await database.fetch_all(query)
        return rows

    async def find_by_email(self, email: str):
        query = self.table.select().where(self.table.c.email == email)
        return await database.fetch_one(query)

    async def find_by_id(self, id: int):
        query = self.table.select().where(self.table.c.id == id)
        return await database.fetch_one(query)

    async def email_exists(self, email: str):
        # return await database.fetch_val(self.table.count()) == 1
        query = self.table.select().where(self.table.c.email == email).count()
        return await database.fetch_val(query) == 1
        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #self.table.columns
        query = self.table.select(None, columns=[func.count()]).select_from(self.table)\
            .where(self.table.c.email == email)
        print(query)
        return await database.fetch_val(query) == 1

    async def create_author(self, name: str, email: str):
        return await database.fetch_one(self.table.insert().values(name=name, email=email))
        count = await self.find_by_email(email)
        if count == 0:
            return await database.fetch_one(self.table.insert().values(name=name, email=email))
        raise Exception(f"Author with email={email} already exists")

    async def create_post(self, author_id: int, title: str):
#        if await Author.objects.find_by_id(author_id):
#            return await database.fetch_one(self.table.insert().values(author_id=author_id, title=title).
#                                            returning(self.table.c.id))
        return None


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())

    posts = relationship("Post", back_populates="author")

    objects: AuthorManager = None


Author.objects = AuthorManager(model_cls=Author)
