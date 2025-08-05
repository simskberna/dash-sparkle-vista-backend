from pydantic import BaseModel, EmailStr, constr

class RegisterSchema(BaseModel):
    email: EmailStr  # Email format kontrolü
    password: constr(min_length=6)  # Min 6 karakter

class LoginSchema(BaseModel):
    email: EmailStr
    password: str
