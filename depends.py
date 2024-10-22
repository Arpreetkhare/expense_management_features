from datetime import datetime, timedelta,timezone

from typing import Optional
import jwt
from fastapi.exceptions import HTTPException




SECRET_KEY = "b4bb9013c1c03b29b9311ec0df07f3b0d8fd13edd02"
# ALGORITHM = "SHA256"
ACCESS_TOKEN_EXPIRE_MINUTES = 3000


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data:dict,expire_delta:Optional[timedelta]=None):
    to_encode = data.copy()
    if expire_delta:
        expire=datetime.utcnow() + expire_delta

    expire=datetime.utcnow()+timedelta(300)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)
    return encoded_jwt


def verify_token(token:str):
    try:
       payload = jwt.decode(token, SECRET_KEY)
       exp = payload.get("exp")
       if exp and datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            raise jwt.ExpiredSignatureError("Token has expired")
       return payload

    except jwt.ExpiredSignatureError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")

def __user_model(auth_token):
    user_model = jwt.decode(auth_token, SECRET_KEY)
    return user_model['sub']

# def verify_password(plane_password,hashed_password):
#     return pwd_context.verify(plane_password,hashed_password)



# def get_passwod_hash(password):
#     return pwd_context.hash(password)


