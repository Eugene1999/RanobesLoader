from epub import Epub
from fb2 import Fb2


class Book(Epub, Fb2):
    def __init__(self) -> None:
        super().__init__()
    
    def save(self, format: str="fb2") -> str:
        # TODO 
        return "path/to/book/"
