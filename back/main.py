from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

from ranobes import download_book

app = FastAPI()


class BookInput(BaseModel):
    link: str
    chapters_count: Optional[int] = 1


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/download/")
async def update_item(book_input: BookInput):
    # ranobe = Ranobes(book.link)
    # chapters = await download_chapters(ranobe.chapters_links)

    book = await download_book(book_input.link)
    return book.txt
