from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
from . import models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session
#connecting to Database
models.Base.metadata.create_all(bind=engine)

app=FastAPI()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

my_posts=[{"title":"Title of Post 1","content":"content of post 1","id":1},
{"title":"Pork","content":"Pork is my favourite meat","id":2}]


class Post(BaseModel):
    title:str
    content:str
    published:bool=True
    rating:Optional[int]=None

def findPost(id:int):
    post={}
    for post1 in my_posts:
        if post1.get('id')==id:
            post=post1
            break
    return post

def findIndex(id:int):
    for i ,p in enumerate(my_posts):
        if p.get("id")==id:
            return i
    return -1

@app.get("/")
def index():
    return "Hello world!"

@app.get("/posts")
def get_posts():
    return {"data":my_posts}


@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post):
    post_dict=new_post.dict()
    post_dict["id"]=randrange(0,1000)
    my_posts.append(post_dict)
    return {"data":post_dict}


@app.get("/posts/{id}")
def get_post(id:int,response:Response):
    post=findPost(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Post with id:{id} not found")
    else:
        return {"post":post}


@app.delete("/posts/{id}")
def delete_post(id:int):
    post_index:int=findIndex(id)
    if post_index==-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Post with id:{id} not found")
    else:
        my_posts.pop(post_index)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


#Updating the Post

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    post_index:int=findIndex(id)
    if post_index==-1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The Post with id:{id} not found")
    else:
        post_dict=post.dict()
        post_dict["id"]=id
        my_posts[post_index]=post_dict
        return {"message":my_posts}
