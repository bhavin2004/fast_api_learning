from fastapi import FastAPI,Body

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get('/books')
def read_all_books():
    return BOOKS

@app.get('/books/{book_title}')
def read_book(book_title:str):
    for book in BOOKS:
        if book['title'].casefold() == book_title.casefold():
            return book
        
    return "NOT FOUND/not exit"

@app.get("/books/")
def get_with_querry(category:str):
    books_to_return=[]
    for book in BOOKS:
        if book['category'].casefold() == category.casefold():
            books_to_return.append(book) 
    return books_to_return

@app.get('/books/by_author/')
def get_book_of_author_with_querry(author_name: str):
    book_to_return = []
    
    for book in BOOKS:
        if book['author'].lower() == author_name.lower(): 
            book_to_return.append(book)
    
    return book_to_return

@app.get('/books/{author_name}/')
def get_author_with_querry(author_name:str,category:str):
    books_to_return = []
    for book in BOOKS:
        if book['author'].casefold() == author_name.casefold() and book['category'].casefold() == category.casefold():
            books_to_return.append(book)
        
    return books_to_return

@app.post("/books/new_book")
def new_book(new_book=Body()):
    BOOKS.append(new_book)
    return {"message": f"{new_book['title']} Added successfully"}
    
    
@app.put("/books/update_book")
def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].lower() == update_book['title'].lower():
            BOOKS[i] = update_book
            return {"message": f"{BOOKS[i]['title']} Updated successfully"}
    return {"message": "Book not found"}  

@app.delete('/books/delete_book/{book_title}')
def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i]['title'].lower() == book_title.lower():
            deleted_book = BOOKS[i]
            BOOKS.pop(i)
            return {"message": f"{deleted_book['title']} deleted successfully"}
    return {"message": "Book not found"}

@app.get('/books/by_author/{author_name}')
def get_book_of_author(author_name: str):
    book_to_return = []
    print("Ho")
    for book in BOOKS:
        if book['author'].lower() == author_name.lower(): 
            book_to_return.append(book)
    
    return book_to_return


