from typing import List
from fastapi import APIRouter,HTTPException,status,Response,Depends
from sqlalchemy.orm import Session
from ..Database import get_db
from ..import models,schema,utils,oauth2

router = APIRouter(prefix="/users",tags=["users"])

@router.post("/" ,status_code=status.HTTP_201_CREATED,response_model=schema.UserOut )
def create_user(user: schema.UserCreate,db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user) ):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schema.UserOut)
def get_user(id:int,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user) ):
    user = db.query(models.User).filter(models.User.id == id).first()
     
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id {id} was not found")
    print(current_user.email)
    return user
     