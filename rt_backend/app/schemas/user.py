from typing import Optional
from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None

# Properties to receive on user creation
class UserCreate(UserBase):
    email: EmailStr
    password: str

# Properties to receive on user update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties to return to client
class UserInDBBase(UserBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str 