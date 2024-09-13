import os

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def setCookie(response, value):
    response.set_cookie(key="code_names_access_token", value=value, secure=True, samesite="None", max_age=ACCESS_TOKEN_EXPIRE_MINUTES)