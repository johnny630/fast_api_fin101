from fastapi import (
  FastAPI, Body, Path, Cookie, Header, Form, File,
  Request, HTTPException, UploadFile, status
)
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import HTTPException, RequestValidationError
from starlette.responses import HTMLResponse
from pydantic import BaseModel, Field, HttpUrl
from typing import Annotated, Any

from datetime import datetime, time, timedelta
from uuid import UUID
import uuid

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

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)


@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    if username != 'johnny':
      raise HTTPException(status_code=418, detail=f"Nope! I don't like {username}.")

    return {'username': username, 'password': password}

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