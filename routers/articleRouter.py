from fastapi import APIRouter,Response,Body
from database import db
from models import Article
from sqlalchemy.future import select

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

@router.get('/articles')
async def fetchArticle():
    query = select(Article)
    query = await db.execute(query)
    query = query.scalars().all()
    data = [{'id':q.id,'title':q.title,'description':q.description} for q in query]
    return data