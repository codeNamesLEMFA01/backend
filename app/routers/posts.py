# import sys

# from pydantic import BaseModel
# from sqlalchemy.orm import Session

# from ..models import Post
# from database import engine, SessionLocal, get_db
# from fastapi import Depends, APIRouter, status

# from routers.auth import get_current_user, get_user_exception, verify_password, get_password_hash

# sys.path.append('..')

# router = APIRouter(
#     prefix='/posts',
#     tags=['Posts'],
#     responses={
#         status.HTTP_404_NOT_FOUND: {
#             'description': 'Not found'
#         }
#     }
# )

# models.Base.metadata.create_all(bind=engine)

# @router.get('/')
# async def read_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts