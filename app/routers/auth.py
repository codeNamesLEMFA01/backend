# Tried from here : https://fastapi.tiangolo.com/tutorial/security/

from ..auth.authServices import authenticate_user, create_access_token, get_password_hash, get_current_active_user

from ..models.token import Token
from ..models.users import User

from typing import Annotated
from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
  prefix="/auth",
)

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register")
async def register_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user_data = User(
    username= form_data.username,
    full_name= form_data.username,
    email= f"{form_data.username}@example.com",
    hashed_password= get_password_hash(form_data.password),
    disabled= False
    )
    User.objects.insert(user_data)
    return {"message": "User registered successfully"}

# @router.get("/users/me")
# async def read_users_me(
#     current_user: Annotated[User, Depends(get_current_active_user)],
# ):
#     return current_user