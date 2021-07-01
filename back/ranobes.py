from os import name
import requests

from bs4 import BeautifulSoup

from book import Book, Chapter, Indent


class Ranobes:
    """ Class for parsing data from ranobes site.
    
        Ways to uploading chapters:
            1. If link refers to specific title (main/specific chapter/chapters list page) go to chapters list page in any case
            2. Upload all list of links for parsing
            3. Async download all chapters
    """

    def __init__(self, link: str):
        if not link.startswith("https://ranobes.com/"):
            raise Exception("Invalid link: it must be https://ranobes.com/ link!")

        self.chapters_link = self._get_chapters_link(link)
        self.chapters = self._get_chapters(self.chapters_link)

    def _get_chapters_link(self, link: str):
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

    def _get_chapters(self, chapters_link):
        pass

    def _get_page_content(self, content: BeautifulSoup) -> str:
        """get all chapter content

        Args:
            page (BeautifulSoup): object with chapter page content data

        Returns:
            str: all chapter text with links to images if exists
        """
        data = []

        for block in content.contents:
            print(block.name)
            if block.name == "p" and block.string:
                data.append(Indent(format_type="text", content=block.string))
            elif block.name == "img":
                print("+", end="")
                data.append(Indent(format_type="image", content=block["src"]))
            elif block.name == "div":
                print("=", end="")
                data += self._get_page_content(block)
            # else:
            #     print(block.name)

        return data

    def get_book(self):
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
        }

        data = requests.get(link, headers=header)
        bs = BeautifulSoup(data.text, "html.parser")

        book_name = (
            bs.find(class_="category grey ellipses").get_text().replace(" ", "_")
        )
        book = Book(book_name)

        while chapters_count > 1:
            data = requests.get(link, headers=header)
            bs = BeautifulSoup(data.text, "html.parser")

            title = bs.find(class_="h4 title").get_text()
            print(f"\n{title}:")
            content = self._get_page_content(bs.find(id="arrticle"))

            book.add(Chapter(name=title, content=content))

            next = bs.find(id="next")
            link = next["href"] if next else None
            chapters_count = chapters_count - 1 if next else 0

        return book
