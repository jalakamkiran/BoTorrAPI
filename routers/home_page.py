import json
import logging

from fastapi import APIRouter, HTTPException
from models.books import Books
from utilities import utils
from datetime import datetime
import requests
from libgenparser import LibgenParser

router = APIRouter(
    prefix='/home_page',
    tags=['Home Page API']
)

libgenparser = LibgenParser()


@router.post('/')
def home_page():
    logging.info("Fetching recomended books from libgen ")
    return fetch_recomended_books()


def fetch_recomended_books():
    books = requests.get(url="http://gen.lib.rus.ec/json.php", params={
        "fields": "id,Title,Author,MD5,language,coverurl,topic,pages,descr",
        "limit2": 30,
        "mode": "last",
        "timefirst": utils.convert_to_date_format(utils.subtract_year(datetime.now(), 1)),
        "timelast": utils.convert_to_date_format(datetime.now())
    })
    _books = []
    for y in json.loads(books.content.decode('utf-8')):
        if (y['language'] == "English"):
            _books.append(Books.from_dict(y))
    return {"books": _books}


@router.get('/download/{id}')
async def download_book_using_md5(id: str):
    if id is None or id == "":
        raise HTTPException(status_code=400, detail={'message': "Md5 can't be none or empty"})
    downloadLink = libgenparser.resolve_download_link(id)
    return {"download_link":downloadLink}
