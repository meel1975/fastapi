from ast import While
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    # id: int

while True:
    try:
        # Connect to your postgres DB https://www.psycopg.org/docs/module.html
        conn = psycopg2.connect(host='localhost', dbname='postgres', user='postgres', password='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "post 1 title", "content": "post 1 content", "id": 1}, {"title": "post 2 title", "content": "post 2 content", "id": 2}, {"title": "post 3 title", "content": "post 3 content", "id": 3}]

# functions

def find_post(id: int):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id: int):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

@app.get("/")
# async def root():
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(payload: dict = Body(...)): # type: ignore
#     print(payload)
#     return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}
def create_post(post: Post):
    # print(post)
    # print(new_post.title)
    # print(new_post.content)

    post_dump = post.model_dump()
    post_dump["id"] = randrange(0,1000000)
    my_posts.append(post_dump)
    # print(post.model_dump())
    return {"data": post_dump}

@app.get("/posts/{id}")
def get_post(id: int, response: Response): #it converts automatically to integer
    # print(id)
    post = find_post(id)
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_with_id": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id: {id} does not exist")
    my_posts.pop(index)
    # return {"message": f"The post {id} was successfully deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    # print(index)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with id: {id} does not exist")
    post_dump = post.model_dump()
    # print(post_dump)
    post_dump["id"] = id
    my_posts[index] = post_dump
    return {"data": post_dump}