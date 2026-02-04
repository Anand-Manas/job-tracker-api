from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    company: str
    position: str
    status: str

class ApplicationResponse(ApplicationCreate):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
