
from pydantic import BaseModel







class otpVali(BaseModel):
    
    mobile_number:str
    
       

    class Config:
        orm_mode=True

class otpVar(BaseModel):

    mobile_number:str
    otp: str
   
    
    class Config:
        orm_mode=True
        


