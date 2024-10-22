from pydantic import BaseModel, validator




class otpVali(BaseModel):
    
    mobile_number:str
    
       

    class Config:
        orm_mode=True

class otpVar(BaseModel):

    mobile_number:str
    otp: str
   
    
    class Config:
        orm_mode=True
        


class UserModel(BaseModel):
    first_name: str
    last_name: str
    # mobile_number: str
    email: str
    
    # otp: int

    class Config:
        orm_mode = True

class SignupRequest(BaseModel):
    first_name: str
    last_name: str
    mobile_number: str
    email: str
    # password: str  # Uncomment if using password-based authentication
