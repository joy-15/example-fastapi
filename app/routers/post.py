from typing import List, Optional

from fastapi.encoders import jsonable_encoder

from app import oauth2
from .. import models,schemas
from fastapi import Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db


router = APIRouter(prefix="/posts", tags=['Posts'])

# @router.get("/",response_model=List[schemas.Post])
@router.get("/",response_model = List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit: int= 10,skip: int = 0,search: Optional[str]=""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    return [
    schemas.PostOut(
        post=schemas.Post(
            id=post.id,
            created_at=post.created_at,
            title=post.title,
            content=post.content,
            published=post.published,
            owner_id=post.owner_id,
            owner=schemas.UserOut(
                id=post.owner.id,  # Assuming you're loading the owner relationship
                email=post.owner.email,
                created_at=post.owner.created_at,
            )
        ),
        votes=votes,
    )
    for post, votes in posts
]
    
    


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s,%s,%s) RETURNING *
    #                """,(post.title,post.content,post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id,**post.__dict__)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model = schemas.PostOut)
def get_post(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * from posts where id = %s""",(str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()


    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} was not found')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : f'post with id: {id} was not found'}
    

    if post[0].owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Not authorized to perform the requested action")
    
    return schemas.PostOut(
        post=schemas.Post(
            id=post[0].id,
            created_at=post[0].created_at,
            title=post[0].title,
            content=post[0].content,
            published=post[0].published,
            owner_id=post[0].owner_id,
            owner=schemas.UserOut(
                id=post[0].owner.id,  # Assuming you're loading the owner relationship
                email=post[0].owner.email,
                created_at=post[0].owner.created_at,
            )
        ),
        votes=post[1])
    

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute(""" DELETE FROM posts where id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Not authorized to perform the requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model = schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s  WHERE id = %s
    #                RETURNING *""",(post.title,post.content,post.published,str(id),))
    # updated_post  = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail = f"Not authorized to perform the requested action")
    
    post_query.update(updated_post.__dict__,synchronize_session=False)

    db.commit()
    
    
    return  post_query.first()
