from pydantic import BaseModel


class HomePageQueryModel(BaseModel):
    fromDate: str
    toDate: str
    page: int
    page_size : int
