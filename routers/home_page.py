import json
import logging

from bs4 import BeautifulSoup
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

_books = []


@router.post('/')
def home_page(homePageQueryModel: HomePageQueryModel):
    logging.info("Fetching recomended books from libgen ")
    return fetch_recomended_books(homePageQueryModel=homePageQueryModel)


def fetch_recomended_books(homePageQueryModel: HomePageQueryModel):
    response = {}
    if len(_books) == 0:
        books = requests.get(url="http://gen.lib.rus.ec/json.php", params={
            "fields": "id,Title,Author,MD5,language,coverurl,topic,pages",
            "limit2": 500,
            "mode": "last",
            "timefirst": homePageQueryModel.fromDate,
            "timelast": homePageQueryModel.toDate
        })

        for y in json.loads(books.content.decode('utf-8')):
            if (y['language'] == "English"):
                _books.append(Books.from_dict(y))
    start = (homePageQueryModel.page - 1) * homePageQueryModel.page_size
    end = start + homePageQueryModel.page_size
    total_items = len(_books)
    total_pages = (total_items + homePageQueryModel.page_size - 1) // homePageQueryModel.page_size  # Ceiling division

    pagination_info = {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": homePageQueryModel.page,
        "page_size": homePageQueryModel.page_size,
        "next_page": homePageQueryModel.page + 1 if homePageQueryModel.page < total_pages else None,
        "prev_page": homePageQueryModel.page - 1 if homePageQueryModel.page > 1 else None,
    }
    response['data'] = _books[start:end]
    response.update(pagination_info)
    return response


@router.get('/download/{id}')
async def download_book_using_md5(id: str):
    if id is None or id == "":
        raise HTTPException(status_code=400, detail={'message': "Md5 can't be none or empty"})
    downloadLink = resolve_download_link(id)
    return {"download_link": downloadLink}


@router.get('/search/{title}')
def search_book(title: str):
    if title is None or title == "":
        raise HTTPException(status_code=400, detail={'message': "Title can't be none or empty"})
    result = libgenparser.search_title(title=title)
    return {'books': parse_search_result_to_books(result)}


def parse_search_result_to_books(result):
    logging.info(result)
    book_list = []
    for i in result:
        books = Books(i['ID'], i['Title'], i['Author'], i['MD5'], i['Language'], i['Thumb'], '', i['Pages'])
        book_list.append(books)
    return book_list


@router.get("/searchByIsbn/{isbn}")
def search_by_isbn(isbn):
    logging.info("Serching by ISBN")
    result = libgenparser.search_isbn(isbn=isbn)
    return {"book": result}


def resolve_download_link(md5) -> str:
    """
    resolves the book's download link by using it's md5 identifier
    and parses the download page of book for available download links
    and returns the first download link found.

    :param md5: md5 hash identifier of that specific book.
    :return: returns download url string of book on success.
    """
    downlod_get_url = BeautifulSoup(requests.get(f"http://library.lol/main/{md5}").text, "lxml")
    ids = downlod_get_url.find(attrs={"id": "download"})
    logging.debug(ids)
    return ids.find('a')['href']
