from fastapi import APIRouter,HTTPException
from database import db
from schema import UserSignUpSchema
from passlib.context import CryptContext
from models import User



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
    # user = db.query(User).filter(User.id==id).first()
    # if not user:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No Such User")
    if not request.password == request.confirm_password:
        # raise HTTPException() #password validator #pydantic validator # whatever i want
        return {'status':'password not match'}
    _hashpassword = hash(request.password)
    user = User(phone_no=request.phone_no,email=request.email,password=_hashpassword)
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {'status':'created'}