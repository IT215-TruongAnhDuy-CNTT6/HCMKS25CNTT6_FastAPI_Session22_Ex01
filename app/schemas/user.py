from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

class UserRegister(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True