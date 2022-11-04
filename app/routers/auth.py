from os import access
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    tags=['Authentication']
    )


@router.post('/login', response_model=schemas.Token)
def Userlogin (user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"invalid credentials")


    #print(user_credentials.password)
    #print(user.password)
    #print(utils.verifyPassword(user_credentials.password,  user.password  ))

    if not utils.verifyPassword(user_credentials.password,  user.password  ):
           raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"invalid credentials")

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    print(access_token)
    return {'access_token' : access_token[0], "expire" : access_token[1], "token_type": "bearer" }
        


