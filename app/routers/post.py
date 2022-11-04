from .. import models, schemas, oauth2
from fastapi import FastAPI, status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', response_model=List[schemas.PostOut])
# @router.get('/')
def get_posts(db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.title.contains(search)).offset(skip).all()

    #print (results)
    # return results
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):

    # print(current_user_id.id)
    new_post = models.Post(user_id=current_user_id.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts ORDER BY ID DESC LIMIT 1""")
    latest_post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    return latest_post

# decorator with path parameter


@router.get("/{id}", response_model=schemas.PostOut)
# @router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):

    #new_id = id
    #cursor.execute("""SELECT * FROM posts where id = (%s) """, new_id)
    #post = cursor.fetchone()
    #print (post)
    #post = find_post(id)

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()

    #post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user_id: int = Depends(oauth2.get_current_user)):
    # deleting post
    # find index in array for ID
    # my_posts.pop(index)
    #index  = find_index_post(id)
    # if index == None:
    #    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} does not exist.")

    #cursor.execute(""" SELECT * FROM posts WHERE id = (%s)""", id)
    #deleted_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist.")

    if post.user_id != current_user_id.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"post with id {id} does not belong to you")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user_id: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    #cursor.execute(""" SELECT * FROM posts WHERE id = (%s)""", id)
    #updated_post = cursor.fetchone()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist.")

    #print (updated_post.user_id)
    #print (current_user_id.id)

    if post.user_id != current_user_id.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"post with id {id} does not belong to you")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
