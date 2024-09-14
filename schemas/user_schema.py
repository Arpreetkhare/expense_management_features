from pydantic import BaseModel,field_validator



class UserModel(BaseModel):
    first_name: str
    last_name: str
    # mobile_number: str
    email: str
    
    # otp: int

    @field_validator('first_name', 'last_name')
    def check_name(cls, value):
        if not value.isalpha():
            raise ValueError('Name should only contain alphabets')
        return value

    class Config:
        orm_mode = True


class Settings(BaseModel):
    authjwt_secret_key: str = 'b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02'

