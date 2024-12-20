from fastapi import FastAPI,Query,Header,File,UploadFile
from pydantic import BaseModel,Field,EmailStr,HttpUrl
import random
from typing import Annotated,Literal

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    image : Image | None = None

class User(BaseModel):
     id: int | None = None
     name: str = Field(..., min_length=1)
     email: Annotated[EmailStr ,"valid Email Address"]
     age: int | None = None

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: set[str] = set()

@app.get('/')
async def home():
    return {'message': 'Hello, Welcome to home'}
# @app.get('/items/{item_id}')
# async def get_items(item_id : int):
#     return {'message': f'Hello, {item_id}'}

@app.get('/products/{product_id}')
async def query_parameters(product_id: int, show_default:int = 0):
        return {'prodcut_id':product_id,'show':show_default}

@app.post('/users')
async def create_user(user: User):
     user.id = random.randint(1,100)
     return user
@app.put('/users/{user_id}')
async def update_user(user_id: int, user: User,q: Annotated[str | None,Query(min_length=3,max_length=50)] = None):
    #  alternate async def update_user(user_id: int, user: User,q: str | None = None):
     user.id = user_id
     user_dict = user.model_dump()
     if q:
          user_dict.update({"q":q})
     return user_dict

@app.get("/items/")
async def read_items(q: Annotated[list[str] | None, Query()] = None):
    query_items = {"q": q}
    return query_items
@app.get("/items/filtered")
async def read_items(filter_query: Annotated[FilterParams, Query()]):
    return filter_query

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results

@app.post("/files")
async def upload_file(file: Annotated[bytes, File()]):
     return {"filesize":len(file)}

@app.post("/uploadfile")
async def upload_file(file: UploadFile):
     return {"filesize":file.filename}