from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from .. import Database,schema,models,utils,oauth2

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login(user_credentials: schema.UserLogin ,db : Session = Depends(Database.get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid credentials")
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    return{"access_token":access_token, "token_type": "bearer"}

