from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: constr(min_length=8)
    confirm_password: str

    class Config:
        schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "johndoe@example.com",
                "password": "strongpassword123",
                "confirm_password": "strongpassword123"
            }
        }

    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
