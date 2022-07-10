from jose import JWTError,jwt
from datetime import datetime,timedelta
from database import db
from sqlalchemy.future import select
from models import User

SECRET_KEY = "whateverSecretKey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5

async def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


#--verify token
async def verfiyAccessToken(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id  = payload.get("user_id",None)
    except JWTError:
        user_id = None
        #or raise whatever 
    return user_id

async def get_user(token:str):
    _type,token = token.split(' ')
    if _type.lower() != 'bearer':
        return None
    user= await verfiyAccessToken(token) 
    print(user)
    if user:
        user = select(User).where(User.id==user)
        user = await db.execute(user)
        user, = user.first()
    return user