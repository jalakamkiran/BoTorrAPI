import json
import logging

from fastapi import APIRouter, HTTPException
from models.books import Books
from models.home_page_query_model import HomePageQueryModel
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
def home_page(homePageQueryModel : HomePageQueryModel):
    logging.info("Fetching recomended books from libgen ")
    return fetch_recomended_books(homePageQueryModel=homePageQueryModel)


def fetch_recomended_books(homePageQueryModel : HomePageQueryModel):
    books = requests.get(url="http://gen.lib.rus.ec/json.php", params={
        "fields": "id,Title,Author,MD5,language,coverurl,topic,pages",
        "limit2": 50,
        "mode": "last",
        "timefirst": homePageQueryModel.fromDate,
        "timelast": homePageQueryModel.toDate
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
    return {"download_link": downloadLink}


@router.get('/search/{title}')
def search_book(title: str):
    if title is None or title == "" :
        raise HTTPException(status_code=400, detail={'message': "Title can't be none or empty"})
    result = libgenparser.search_title(title=title)
    return {'books': parse_search_result_to_books(result)}

def parse_search_result_to_books(result):
    book_list = []
    for i in result:
        books = Books(i['ID'], i['Title'], i['Author'], i['MD5'], i['Language'], i['Thumb'], '',i['Pages'])
        book_list.append(books)
    return book_list
