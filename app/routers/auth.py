from ..auth.authServices import authenticate_user, create_access_token, get_password_hash, get_current_active_user

from ..models.users import User

import os
from typing import Annotated
from datetime import timedelta
from fastapi import Depends, HTTPException, status, APIRouter, Response
from fastapi.security import OAuth2PasswordRequestForm
from mongoengine.errors import NotUniqueError
from ..utils.cookies import setCookie

router = APIRouter(
  prefix="/auth",
)

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response
):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )

    setCookie(response, access_token)

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register")
async def register_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response
):
    user_data = User(
    email= form_data.username,
    hashed_password= get_password_hash(form_data.password),
    disabled= False
    )
    try:
        User.objects.insert(user_data)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user_data.email}, expires_delta=access_token_expires
        )

        setCookie(response, access_token)

        return {
            "message": "User registered successfully",
            "access_token": access_token,
            "token_type": "bearer"
        }
    except NotUniqueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    user={
        "email": current_user["email"],
        "disabled": current_user["disabled"]
    }
    return user

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="code_names_access_token")
    return {"message": "Successfully logged out"}
