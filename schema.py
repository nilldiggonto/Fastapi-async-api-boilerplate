from pydantic import BaseModel,EmailStr

class UserloginSchema(BaseModel):
    email       :   EmailStr
    password    :   str

class UserSignUpSchema(UserloginSchema):
    confirm_password:   str
    phone_no        :   str
