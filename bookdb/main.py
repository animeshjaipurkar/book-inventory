from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

description = """
Book Inventory API lets you create, view, update & delete books
"""

app = FastAPI(
    title="Book Inventory App",
    description=description,
    version="0.0.1",    
    contact={
        "name": "Animesh Jaipurkar",        
        "email": "animesh.jaipurkar@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """
    Create a new book entity with given information
    """
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this title already exists")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, author: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Gets list of books available in the inventory 
    """
    if author:
        books = crud.get_books_by_author(db, author=author, skip=skip, limit=limit)
    else:
        books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete a book identified by id
    """
    book_to_delete = find_book(book_id, db)

    if book_to_delete is not None:
        crud.delete_book(db, book_to_delete)


def find_book(book_id, db) -> Optional[schemas.Book]:
    books = crud.get_all_books(db)
    for book in books:
        if book.id == book_id:
            return book
    return None

@app.patch("/books/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, item: schemas.BookUpdate, db: Session = Depends(get_db)):
    """
    Update an existing book with new information for one or more of its attributes
    """
    
    stored_book_data = crud.get_book_by_id(db, id=book_id)
    if not stored_book_data:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = item.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(stored_book_data, key, value)
    
    db.add(stored_book_data)
    db.commit()
    db.refresh(stored_book_data)

    return stored_book_data
