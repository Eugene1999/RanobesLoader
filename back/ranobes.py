from os import name
import requests

from bs4 import BeautifulSoup

from book import Book, Chapter, Indent


def get_page_content(content: BeautifulSoup) -> str:
    """get all chapter content

    Args:
        page (BeautifulSoup): object with chapter page content data

    Returns:
        str: all chapter text with links to images if exists
    """
    data = []

    for block in content.contents:
        if block.name == "p" and block.string:
            data.append(Indent(format_type="text", content=block.string))
        elif block.name == "img":
            print("+", end="")
            data.append(Indent(format_type="image", content=block["src"]))
        elif block.name == "div":
            print("=", end="")
            data += get_page_content(block)
        else:
            print(block.name)

    return data


def get_book(link: str, chapters_count: int = 1):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }

    data = requests.get(link, headers=header)
    bs = BeautifulSoup(data.text, "html.parser")

    book_name = bs.find(class_="category grey ellipses").get_text().replace(" ", "_")
    book = Book(book_name)

    while chapters_count > 1:
        data = requests.get(link, headers=header)
        bs = BeautifulSoup(data.text, "html.parser")

        title = bs.find(class_="h4 title").get_text()
        print(f"\n{title}:")
        content = get_page_content(bs.find(id="arrticle"))

        book.add(Chapter(name=title, content=content))

        next = bs.find(id="next")
        link = next["href"] if next else None
        chapters_count = chapters_count - 1 if next else 0

    return book
