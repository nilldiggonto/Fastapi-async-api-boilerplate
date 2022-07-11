from fastapi import APIRouter,HTTPException,Request
from database import db
from schema import UserSignUpSchema,UserloginSchema
from passlib.context import CryptContext
from models import User
from sqlalchemy.future import select
from authenticate import create_access_token,get_user


router = APIRouter(prefix='/user')

#Password hashed and validators
pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    return pwd_context.hash(password)

def verifyPass(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

#views
@router.post('/signup')
async def createUser(request:UserSignUpSchema):
    user = select(User).filter(User.email == request.email)#.first()
    # user = select(User).where(User.email==request.email)
    user = await db.execute(user)
    user = user.scalars().first()
    if user:
        return {'status':f'{user.email} already exists','alert':'email'}
    if not request.password == request.confirm_password:
        # raise HTTPException() #password validator #pydantic validator # whatever i want
        return {'status':'password not match','alert':'password'}
    _hashpassword = hash(request.password)
    user = User(phone_no=request.phone_no,email=request.email,password=_hashpassword)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'status':'created','alert':'register'}

@router.post('/login')
async def loginUser(_rsession:Request,request:UserloginSchema):
    user = select(User).where(User.email==request.email)
    user = await db.execute(user)
    user = user.scalars().first()
    if not user:
        return {'status':f'{request.email} Not Found','alert':'invalid'}
    if not verifyPass(request.password,user.password):
        return {'status':'wrong password'}
    access_token = await create_access_token(data= {"user_id":user.id,'email':user.email})
    session = _rsession.session.get('token',None)
    if not session:
        bearer_token = "Bearer "+ access_token
        _rsession.session['token'] =bearer_token
    return {'access_token':access_token,'token_type':"bearer",'alert':'success'}

@router.post('/verify/token')
async def verifyToken(request:Request):
    # data = await request.json()
    token = request.headers.get('Authorization',None)
    if not token:
        return {'status':'provide authorize token'}
    user = await get_user(token)
    if not user:
        return {'status':'invalid token'}
    return {'status':'token verified','username':user.email}
