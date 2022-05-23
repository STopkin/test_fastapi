from typing import List
from pydantic import BaseModel
import datetime


class PostBase(BaseModel):
    title: str
    
    
class PostCreate(PostBase):
    pass
    
    
class Post(PostBase):
    id: int
    author_id: int
    created_at: datetime.datetime
    
    class Config:
        orm_mode = True
        
        
class AuthorBase(BaseModel):
    name: str
    email: str
    
    
class AuthorCreate(AuthorBase):
    pass
    
    
class Author(AuthorBase):
    id: int
    created_at: datetime.datetime
    posts: List[Post] = []

    class Config:
        orm_mode = True
        
