from fastapi import APIRouter,Response,Body
from database import db
from models import Article
from sqlalchemy.future import select
from sqlalchemy import update,delete

router = APIRouter(prefix="/article")


@router.post('/create')
async def createArticle(request:dict=Body(...)):
    query = Article(title=request['title'],description=request['description'])
    db.add(query)
    await db.commit()
    await db.refresh(query)
    # query = Article.insert().values(title=request['title'],descripton=request['description'])
    # await db.execute(query)
    return {'status':'created'}

@router.get('/all')
async def fetchArticle():
    query = select(Article)
    query = await db.execute(query)
    query = query.scalars().all()
    data = [{'id':q.id,'title':q.title,'description':q.description,'updated':q.updated} for q in query]
    return data

@router.put('/update/{id}')
async def updateArticle(id:int,request:dict=Body(...)):

    query = update(Article).where(Article.id==id)
    query = query.values(title=request['title'],description=request['description'])  
    query.execution_options(synchronize_session="fetch")
    await db.execute(query)
    # await db.commit()    
    return {'status':'updated'}

@router.delete('/delete/{id}')
async def deleteArticle(id:int):
    query = delete(Article).where(Article.id == id)
    await db.execute(query)
    return {'status':'deleted'}