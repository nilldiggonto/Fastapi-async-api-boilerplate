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
    user = select(User).where(User.email==request.email)
    user = await db.execute(user)
    user, = user.first()
    if user:
        return {'status':f'{user.email} already exists'}
    if not request.password == request.confirm_password:
        # raise HTTPException() #password validator #pydantic validator # whatever i want
        return {'status':'password not match'}
    _hashpassword = hash(request.password)
    user = User(phone_no=request.phone_no,email=request.email,password=_hashpassword)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {'status':'created'}

@router.post('/login')
async def loginUser(request:UserloginSchema):
    user = select(User).where(User.email==request.email)
    user = await db.execute(user)
    user, = user.first()
    if not user:
        return {'status':f'{user.email} Not Found'}
    if not verifyPass(request.password,user.password):
        return {'status':'wrong password'}
    access_token = await create_access_token(data= {"user_id":user.id,'email':user.email})
    return {'access_token':access_token,'token_type':"bearer"}

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
