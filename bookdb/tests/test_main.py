import json
import unittest
from unittest.mock import patch

from fastapi import HTTPException
from fastapi.testclient import TestClient

from bookdb.main import app

class TestMain(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.book_1 = {'title': "hello", 'author': "auth hello", 'published_date': "2020-01-01", 'id': 123}
        self.book_2 = {'title': "goodbye", 'author': "auth another", 'published_date': "2020-01-01", 'id': 124}
        self.book_list = [self.book_1, self.book_2]

    def test_create_book(self):        
        with patch('bookdb.main.crud.get_book_by_title') as mock_get_book, \
            patch('bookdb.main.crud.create_book') as mock_create_book:

            mock_get_book.return_value = None
            mock_create_book.return_value = self.book_1

            response = self.client.post("/books/", json={'title': "hello", 'author': "auth hello", 'published_date': "2020-01-01"})
              
            mock_get_book.assert_called_once()
            mock_create_book.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), self.book_1)


            mock_get_book.reset_mock()
            mock_get_book.return_value = {'title': "hello"}
            response = self.client.post("/books/", json={'title': "hello", 'author': "auth hello", 'published_date': "2020-01-01"})
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), {'detail': 'Book with this title already exists'})

    def test_read_books(self):         
        with patch('bookdb.main.crud.get_books') as mock_get_books:
            mock_get_books.return_value = self.book_list
            response = self.client.get("/books/")            
            mock_get_books.assert_called_once()
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), self.book_list)
