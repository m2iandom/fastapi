from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from ..database import get_db, IntegrityError

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    #import ipdb
    # ipdb.set_trace()
    # hash pwd
    user.password = utils.hashPassword(user.password)

    new_user = models.User(**user.dict())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError as e:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"error : '{e.orig.args[1]}'")
    except Exception as e1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"error : '{e1.args}'")
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    # def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id {id} was not found")
    return user
