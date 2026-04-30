from pydantic import BaseModel

class UserUnhashed(BaseModel):
    email: str
    password_plaintext: str
    
class UserHashed(BaseModel):
    id: int
    email: str
    password_hashed: str
    