
from email.policy import default
from sqlalchemy import Column,String,Text,Integer,Boolean,DateTime
from sqlalchemy.sql.sqltypes import TIME, TIMESTAMP
from database import Base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey

class Article(Base):
    __tablename__ = "article"

    id          =   Column(Integer,primary_key=True,index=True)
    title       =   Column(String)
    description =   Column(Text)
    active      =   Column(Boolean,default=True)
    created     =   Column(DateTime(timezone=True), server_default=func.now())
    updated     =   Column(DateTime(timezone=True),onupdate=func.now(),server_default=func.now())
    owner_id    =   Column(Integer,ForeignKey('users.id',ondelete="CASCADE"),nullable=True)

    owner       =   relationship("User",backref="articles") 

class User(Base):
    __tablename__ = 'users'
    id          =   Column(Integer,primary_key=True,nullable=False)
    phone_no    =   Column(String,nullable=True)
    email       =   Column(String,nullable=False,unique=True)
    password    =   Column(String,nullable=False)
    created_at  =   Column(DateTime(timezone=True), server_default=func.now())