from typing import Any
from dataclasses import dataclass
import json


@dataclass
class Books:
    id: str
    title: str
    author: str
    md5: str
    language: str
    coverurl: str
    topic: str
    pages : str

    @staticmethod
    def from_dict(obj: Any) -> 'Books':
        _id = str(obj.get("id"))
        _title = str(obj.get("title"))
        _author = str(obj.get("author"))
        _md5 = str(obj.get("md5"))
        _language = str(obj.get("language"))
        _coverurl = "https://libgen.is/covers/" + str(obj.get("coverurl"))
        _topic = str(obj.get("topic"))
        _pages = str(obj.get("pages"))
        return Books(_id, _title, _author, _md5, _language, _coverurl, _topic,_pages)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)
