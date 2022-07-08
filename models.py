
from sqlalchemy import Column,String,Text,Integer,Boolean,DateTime
from database import Base
from sqlalchemy.sql import func

class Article(Base):
    __tablename__ = "article"

    id          =   Column(Integer,primary_key=True,index=True)
    title       =   Column(String)
    description =   Column(Text)
    created     =   Column(DateTime(timezone=True), server_default=func.now())
    updated     =   Column(DateTime(timezone=True),onupdate=func.now(),server_default=func.now())