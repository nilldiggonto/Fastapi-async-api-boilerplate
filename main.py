# import uvicorn
from fastapi import FastAPI
from database import db

app = FastAPI()

db.init()

app = FastAPI(
    title="Blog Application",
    description="Blog Users",
    version="1",
)


@app.on_event("startup")
async def startup():
    await db.create_all()


@app.on_event("shutdown")
async def shutdown():
    await db.close()

@app.get("/")
async def hello_world():
    return "hello_world"


# @app.post('/create')
# async def create_article(request: dict= Body(...),db:_session=Depends(get_db)):
#     print(request['title'])
#     data = _model.Article(title=request['title'],description=request['description'])
#     db.add(data)
#     db.commit()
#     db.refresh(data)
#     return {'status':'created','data':"data"}


# if __name__ == '__main__':
#     uvicorn.run("app:app", port=1111, host='127.0.0.1')