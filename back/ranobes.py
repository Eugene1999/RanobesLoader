import requests
import asyncio

from typing import Optional
from bs4 import BeautifulSoup

from book import Book, Chapter, Indent

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}


async def download_book(link: str) -> Book:
    base_link = await get_base_link(link)
    chapters_links = await get_chapters_links(base_link)

    title = await get_title_name(base_link)
    chapters = await download_chapters(chapters_links)

    return Book(name=title, chapters=chapters)


async def get_base_link(link: str):
    LEN_TYPES = {8: "contents", 5: "main", 6: "chapter"}
    type = LEN_TYPES.get(len(link.split("/")))
    # TODO make it via regular expressions
    if type == "contents":
        return "/".join(link.split("/")[:-3]) + "/"
    elif type == "main":
        link = link.split("/")
        link[3] = "chapters"

        title_name = "-".join(link[-1].split("-")[1:])
        link[-1] = title_name.split(".")[0]

        return "/".join(link) + "/"
    elif type == "chapter":
        return "/".join(link.split("/")[:-1]) + "/"
    else:
        raise Exception("Uncorrect link: it must be refers to specific title link")


async def get_title_name(base_link) -> str:
    data = requests.get(base_link, headers=HEADERS)
    bs = BeautifulSoup(data.text, "html.parser")

    return bs.find(class_="ellipses grey").get_text()


async def get_chapters_links(base_link):
    data = requests.get(base_link, headers=HEADERS)
    bs = BeautifulSoup(data.text, "html.parser")

    next = bs.find(class_="page_next").a["href"]
    chapters_pages = [base_link, next]

    while next:
        data = requests.get(next, headers=HEADERS)
        bs = BeautifulSoup(data.text, "html.parser")

        next = bs.find(class_="page_next")
        next = next.a["href"] if next.a else None

        if next:
            chapters_pages.append(next)

    chapters_links = []
    for link in chapters_pages[::-1]:
        data = requests.get(link, headers=HEADERS)
        bs = BeautifulSoup(data.text, "html.parser")

        links = []
        chapters_div = bs.find_all("div", {"class": "cat_block cat_line"})

        for div in chapters_div:
            links.append(div.a["href"])

        chapters_links += links[::-1]

    return chapters_links


async def download_chapters(
    chapters_links: list, start: Optional[int] = None, end: Optional[int] = None
):
    chapters = await asyncio.gather(
        *[download_chapter(link) for link in chapters_links[start:end]]
    )

    return list(chapters)


async def download_chapter(link: str):
    data = requests.get(link, headers=HEADERS)
    bs = BeautifulSoup(data.text, "html.parser")

    title = bs.find(class_="h4 title").get_text()
    content = get_page_content(bs.find(id="arrticle"))

    return Chapter(title=title, content=content)


def get_page_content(content: BeautifulSoup) -> list:
    data = []

    for block in content.contents:
        if block.name == "p" and block.string:
            data.append(Indent(format_type="text", content=block.string))
        elif block.name == "img":
            data.append(
                Indent(
                    format_type="image", content="https://ranobes.com" + block["src"]
                )
            )
        elif block.name == "div":
            data += get_page_content(block)

    return data

