# Restful API for Book Inventory

Following are the steps to setup the API locally on unix/mac systems

Git clone the repository:
 - git clone git@github.com:animeshjaipurkar/book-inventory.git


Install python3.6+ if not already installed

Set up virtual environment
- python3 -m venv env 

Activate the virtual environment
- . ./env/bin/activate


Install the requirements
- pip install requirements.txt


Start the server with command:
- uvicorn bookdb.main:app --reload


View the api in browser:
- Open the browser and navigate to localhost:8000
- For viewing all books: http://localhost:8000/books/
- For api docs: http://localhost:8000/docs


How to run unittests
- Navigate to the bookdb/tests directory 
- Run the command: pytest
