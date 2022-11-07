from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from .config import settings
from fastapi import Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session

# secret key
# Algorithm
# expiration time
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.Algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_min


def create_access_token(data: dict):
    to_encode = data.copy()
    #expire = datetime.utcnow() + timedelta(minutes=(ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.now() + timedelta(minutes=(60))
    print('expiry set to 60')
    print(expire)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return [encoded_jwt, expire]
    # return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user_id = db.query(models.User).filter(models.User.id == token.id).first()

    return user_id
