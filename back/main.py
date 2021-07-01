from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from ranobes import Ranobes

app = FastAPI()


class BookLink(BaseModel):
    link: str
    chapters_count: Optional[int] = 1


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/get_some/{item_id}")
def get_some(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.post("/download/")
async def update_item(book: BookLink):
    ranobe = Ranobes(book.link)
    # b = ranobe.get_book()

    return "aaa"  # b.txt
