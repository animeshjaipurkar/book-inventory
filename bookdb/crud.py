from sqlalchemy.orm import Session

from . import models, schemas


def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_book_by_title(db: Session, title: str):
    return db.query(models.Book).filter(models.Book.title == title).first()

def get_book_by_id(db: Session, id: int):
    return db.query(models.Book).filter(models.Book.id == id).first()

def get_books_by_author(db: Session, author: str):
    return db.query(models.Book).filter(models.Book.author == author).all()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_all_books(db: Session):
    return db.query(models.Book).all()

def create_book(db: Session, book: schemas.Book):
    db_book = models.Book(author=book.author, title=book.title, published_date=book.published_date)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book: schemas.Book):
    db.delete(book)
    db.commit()
