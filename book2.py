from fastapi import FastAPI,Query,Path,HTTPException
from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime
from starlette import status



app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    desc : str
    rating: float
    published_date: int
    
    def __init__(self,id,title,author,desc,rating,published_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.desc = desc
        self.rating = rating
        self.published_date = published_date
        
class BookRequest(BaseModel):
    id: Optional[int] = Field(description='IT is optional as it is set automaticall',default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    desc : str = Field(min_length=1, max_length=100)
    rating: float = Field(gt=-1, lt= 6)
    published_date: int = Field(gt=1000,lt=int(datetime.now().strftime("%Y"))+1)
    
    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "A NEW BOOK",
                "author": "Bhavin Karangia",
                "desc": "A new DESC of a book",
                "rating": 5,
                'published_date': 2020
            }
        }
    }
    

# BOOKS = [
#     Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
#     Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
#     Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5),
#     Book(4, 'HP1', 'Author 1', 'Book Description', 2),
#     Book(5, 'HP2', 'Author 2', 'Book Description', 3),
#     Book(6, 'HP3', 'Author 3', 'Book Description', 1)
# ]

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2025),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2025),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2019),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2008),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2007),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2006)
]

@app.get("/books",status_code=status.HTTP_200_OK)
def get_all_books():
    if BOOKS:
        return BOOKS
    raise HTTPException(status_code=404,detail='Book Not Found')


@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
def get_book_by_id(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404,detail='Book Not Found')
    

@app.get("/books/",status_code=status.HTTP_200_OK)
def get_books_by_rating_querry(book_rating:int = Query(gt=0,lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    if books_to_return:
        return books_to_return
    raise HTTPException(status_code=404,detail='Books Not Found')


@app.get("/books/publish/",status_code=status.HTTP_200_OK)
def get_books_by_published_date(published_date:int = Query(gt=1000,lt=int(datetime.now().strftime("%Y"))+1)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    if books_to_return:
        return books_to_return
    raise HTTPException(status_code=404,detail='Books Not Found')

@app.post("/create_book",status_code=status.HTTP_201_CREATED)
def create_book(new_book: BookRequest):
    # print(new_book.model_dump())
    new_book = Book(**new_book.model_dump()) # type: ignore
    BOOKS.append(create_book_id(new_book)) # type: ignore

def create_book_id(book:Book):
    book.id = 1 if not len(BOOKS) else BOOKS[-1].id+1
    return book


@app.put("/update_book",status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            return
    raise HTTPException(status_code=404,detail='Book Not Found')



@app.delete('/books/{book_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id:int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return 
    raise HTTPException(status_code=404,detail='Book Not Found')


