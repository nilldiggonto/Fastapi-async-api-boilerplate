# import uvicorn
from fastapi import FastAPI,Request
from database import db
from routers import authRouter as _auth,crudRouter as _crud
from starlette.middleware.sessions import SessionMiddleware
from authenticate import get_user
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles

db.init()

app = FastAPI(title="Blog Application",description="Blog Users",version="1",docs_url=None, redoc_url=None)

@app.on_event("startup")
async def startup():
    await db.create_all()


@app.on_event("shutdown")
async def shutdown():
    await db.close()

app.add_middleware(SessionMiddleware,secret_key='whatever')

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

async def get_authenticate_user(request):
    session = request.session.get('token',None)
    if session:
        user = await get_user(session)
        return user
    return session

@app.get("/",response_class=HTMLResponse)
async def index(request:Request):
    user = await get_authenticate_user(request)
    if not user:
        return RedirectResponse('/register')
    return templates.TemplateResponse("home.html",{'request':request})
    
@app.get("/register",response_class=HTMLResponse)
async def register(request:Request):
    return templates.TemplateResponse("register.html",{'request':request})

@app.get("/login",response_class=HTMLResponse)
async def login(request:Request):
    return templates.TemplateResponse("login.html",{'request':request})


app.include_router(_crud.router)
app.include_router(_auth.router)




# @app.get("/")
# async def testworld(request:Request):
#     # session = request.session.get('token',None)
#     # if not session:
#     #     request.session['token'] ="i am token"
#     return "yo"

# @app.get('/test',response_class=HTMLResponse)
# async def test(request:Request):
#     user = await get_authenticate_user(request)
#     if not user:
#         return "<h1> not authenticate </h1>"
#     return templates.TemplateResponse("test.html",{'request':request})


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