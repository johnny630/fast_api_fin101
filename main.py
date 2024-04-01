from fastapi import FastAPI, Body
from pydantic import BaseModel, HttpUrl

from datetime import datetime

app = FastAPI()

BOOKS = [
  {'title': 'johnny book', 'price': 35, 'auth': 'johnny'},
  {'title': 'johnny book2', 'price': 30, 'auth': 'johnny'},
  {'title': 'rachel book', 'price': 12, 'auth': 'rachel'},
]

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
  name: str
  description: str | None = None
  price: float
  tax: float | None = None
  images: list[Image]

@app.post('/items')
async def create_item(item: Item):
  return item

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
