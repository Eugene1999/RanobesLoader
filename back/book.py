class Indent:
    FORMAT_TYPES = ("image", "text")

    def __init__(self, format_type: str, content: str):
        self.content = content

        if format_type in self.FORMAT_TYPES:
            self.format_type = format_type
        else:
            raise Exception(f"Indent haven`t this format: {format}")


class Chapter:
    def __init__(self, name: str = "", content: list = []):
        self.name = name
        self.content = content

    # @property
    # def content(self):
    #     return self.content

    # @content.setter
    # def content(self, new_list):
    #     validators = [
    #         type(new_list) == list,
    #         all([type(el) == Indent for el in new_list]),
    #         len(self.content) == 0,
    #     ]
    #     if all(validators):
    #         self.content = new_list
    #     else:
    #         raise Exception(
    #             "You can't set new content if it is not empty, or if new content not list!"
    #         )

    def add(self, indent):
        if type(indent) == Indent:
            self.content.append(indent)
        else:
            raise Exception("You can add to the chapter only Indent object!")


class Book:
    def __init__(self, name: str = "", chapters: list = []):
        self.name = name
        self.chapters = chapters

    def add(self, chapter):
        if type(chapter) == Chapter:
            self.chapters.append(chapter)
        else:
            raise Exception("You can add only Chapter object!")

    def save(self, format: str = "txt") -> str:
        # TODO
        return ""

    @property
    def txt(self):
        content = ""

        for chapter in self.chapters:
            content += "\n\n{}\n\n".format(chapter.name)

            for indent in chapter.content:
                content += indent.content + "\n\n"

        return {"name": self.name, "content": content}

