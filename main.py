from fastapi import (
  FastAPI, Body, Path, Cookie, Header, Form, File,
  Request, HTTPException, UploadFile, status,
  Depends
)
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.responses import HTMLResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Any

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from uuid import UUID
import uuid

# async def verify_token(x_token: str = Header()):
#     if x_token != "fake-super-secret-token":
#         raise HTTPException(status_code=400, detail="X-Token header invalid")

# async def verify_key(x_key: str = Header()):
#     if x_key != "fake-super-secret-key":
#         raise HTTPException(status_code=400, detail="X-Key header invalid")
#     return x_key

# app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
app = FastAPI()

BOOKS = [
  {'title': 'johnny book', 'price': 35, 'auth': 'johnny'},
  {'title': 'johnny book2', 'price': 30, 'auth': 'johnny'},
  {'title': 'rachel book', 'price': 12, 'auth': 'rachel'},
]

class Image(BaseModel):
    url: HttpUrl = Field(examples=['https://google.com'])
    name: str = Field(examples=['google'])

class Item(BaseModel):
  name: str
  description: str | None = None
  price: float
  tax: float | None = None
  images: list[Image]

@app.post('/items', response_model=Item, response_model_exclude={'tax', 'images'}, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
  return item

@app.put("/items/{item_id}", status_code=status.HTTP_200_OK)
async def read_items(
    item_id: UUID = Path(description=uuid.uuid4()),
    user_agent: Annotated[str | None, Header()] = None,
    ads_id: Annotated[str | None, Cookie()] = None,
    start_datetime: Annotated[datetime | None, Body()] = None,
    end_datetime: Annotated[datetime | None, Body()] = None,
    repeat_at: Annotated[time | None, Body()] = None,
    process_after: Annotated[timedelta | None, Body()] = None,
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
        "ads_id": ads_id,
        "user_agent": user_agent,
    }

class Plan(BaseModel):
  name: str | None = None
  description: str | None = None
  price: float | None = None
  tax: float = 10.5
  tags: list[str] = []
  start_datetime: datetime | None = None
  process_after: timedelta | None = None # detail ref: https://en.wikipedia.org/wiki/ISO_8601
  after_datetime: datetime | None = None

plans = {
  "foo": {"name": "Foo", "price": 50.2},
  "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
  "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}

@app.get("/plans/{plan_id}", response_model=Plan, tags=['plans'])
async def read_plan(plan_id: str):
    return plans[plan_id]

@app.put('/plans/{plan_id}', response_model=Plan, tags=['plans'])
async def update_plan(plan_id: str, plan: Plan):
  if plan.start_datetime and plan.process_after:
    plan.after_datetime = plan.start_datetime + plan.process_after
  update_plan_encoded = jsonable_encoder(plan)
  plans[plan_id] = jsonable_encoder(plan)
  return update_plan_encoded

@app.patch('/plans/{plan_id}', response_model=Plan, tags=['plans'])
async def patch_update_plan(plan_id: str, plan: Plan):
  plan_model = Plan(**plans[plan_id])

  if plan.start_datetime and plan.process_after:
    plan.after_datetime = plan.start_datetime + plan.process_after
  update_data = plan.model_dump(exclude_unset=True)
  updated_plan = plan_model.model_copy(update=update_data, deep=True)
  plans[plan_id] = jsonable_encoder(updated_plan)
  return plans[plan_id]

# @app.exception_handler(HTTPException)
# async def http_exception_handler(request, exc):
#     return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     return PlainTextResponse(str(exc), status_code=400)

async def common_params(
  q: str | None = None,
  skip: int = 0,
  limit: int = 100
):
  return {'q': q, 'skip': skip, 'limit': limit}

@dataclass
class CommonPrams:
  q: str | None = None
  skip: int = 0,
  limit: int = 100

@app.get('/query1/', tags=['Dependencies'])
async def query1(commons: CommonPrams = Depends()):
  return commons

@app.get('/query2/', tags=['Dependencies'])
async def query2(commons: CommonPrams = Depends()):
  return commons

o_auth2_schema = OAuth2PasswordBearer(tokenUrl='token')

fake_users_db = {
  "johndoe": {
    "username": "johndoe",
    "full_name": "John Doe",
    "email": "johndoe@example.com",
    "hashed_password": "fakehashedsecret",
    "disabled": False,
  },
  "alice": {
    "username": "alice",
    "full_name": "Alice Wonderson",
    "email": "alice@example.com",
    "hashed_password": "fakehashedsecret2",
    "disabled": True,
  },
}


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def fake_hash_password(password: str):
  return "fakehashed" + password

@app.post("/token", tags=['user'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
  user_dict = fake_users_db.get(form_data.username)
  if not user_dict:
      raise HTTPException(status_code=400, detail="Incorrect username or password")
  user = UserInDB(**user_dict)
  hashed_password = fake_hash_password(form_data.password)
  if not hashed_password == user.hashed_password:
      raise HTTPException(status_code=400, detail="Incorrect username or password")

  return {"access_token": user.username, "token_type": "bearer"}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(o_auth2_schema)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/current_user", tags=['user'])
async def current_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/ping")
async def ping():
  return {"message": "pong"}

@app.get("/time")
async def time():
  return {"time": datetime.now().isoformat()}

@app.get('/books')
async def all_books():
  return BOOKS

# title is path parameter, auth is query parameter
@app.get('/books/title/{title}')
async def book_by_title(title: str, auth: str):
  for book in BOOKS:
    if book['title'].casefold() == title.casefold() and \
       book['auth'].casefold() == auth.casefold():
        return book

@app.post('/books')
async def create_book(new_book=Body()):
  BOOKS.append(new_book)

@app.put('/books')
async def update_book(update_book=Body()):
  for i in range(len(BOOKS)):
    if BOOKS[i]['title'].casefold() == update_book['title'].casefold():
        BOOKS[i] = update_book

@app.delete('/books')
async def delete_book(delete_book=Body()):
  for i in range(len(BOOKS)):
    if BOOKS[i]['title'].casefold() == delete_book['title'].casefold():
        BOOKS.pop(i)
        break

@app.post("/file/")
async def create_file(file: bytes | None = File(default=None)):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}


@app.post("/upload_file/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}

@app.post("/files/")
async def create_files(
    files: list[bytes] = File(description="Multiple files as bytes"),
):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/upload_files/")
async def create_upload_files(
    files: list[UploadFile] = File(description="Multiple files as UploadFile"),
):
    return {"filenames": [file.filename for file in files]}

@app.get("/upload")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/upload_files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)