from pydantic import BaseModel, EmailStr

# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    role: str = "user"

class UserOut(UserBase):
    id: int
    role: str

    class Config:
        from_attributes = True

class UserInDB(UserOut):
    hashed_password: str

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

# Item schemas
class ItemBase(BaseModel):
    title: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class ItemOut(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True