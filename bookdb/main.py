from typing import Optional, List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book_by_title(db, title=book.title)
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this title already exists")
    return crud.create_book(db=db, book=book)


@app.get("/books/", response_model=List[schemas.Book])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books


@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)) -> None:
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
