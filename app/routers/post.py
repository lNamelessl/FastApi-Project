from turtle import mode
from typing import List, Optional
from fastapi import APIRouter,HTTPException,status,Response,Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import oauth2
from ..Database import get_db
from ..import models,schema


router = APIRouter(prefix="/posts",tags=["posts"])

@router.get("/m")
def get_message():
    return {"message":"Hello,World"}

@router.get("/",response_model=List[schema.PostOut])
def post(db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),limit:int = 5,skip:int=0,search:Optional[str]="" ):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    return results

@router.post("/" ,status_code=status.HTTP_201_CREATED)
def create_posts(post:schema.PostCreate,db: Session = Depends(get_db),
                  current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    # (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}",response_model=schema.PostOut)
def get_posts(id:int, db: Session = Depends(get_db),
        current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)),)
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter=True).group_by(
            models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id {id} was not found")
    return  post

@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)  ):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",(str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="post with id of {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail= "not authorised to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schema.Post)
def update_post(id:int, updated_post:schema.PostBase, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user) ):
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
    #                (post.title,post.content,post.published,(str(id))))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail= "post with id: {id} does not exist ")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,detail= "not authorised to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return  post_query.first()