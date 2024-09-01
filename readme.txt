-------------------------------------------------------------------------------------------------------------------------------------
Class Declaration: Defines a new class named Book. A class in Python is a blueprint for creating objects (a particular data structure).

def __init__(self, book_id, title, author, category, count):

    __init__ Method: This is the initializer method for the class. It's called when a new instance of the class is created.
    Parameters:
        self: Refers to the instance of the class being created. It's a reference to the current instance of the class and is used to access
	variables that belong to the class.
        book_id: The unique identifier for the book.
        title: The title of the book.
        author: The author of the book.
        category: The category or genre of the book.
        count: The number of copies of the book available

self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.count = count
        self.is_borrowed = False

    self.book_id = book_id: Assigns the value of the book_id parameter to the instance variable book_id.
    self.title = title: Assigns the value of the title parameter to the instance variable title.
    self.author = author: Assigns the value of the author parameter to the instance variable author.
    self.category = category: Assigns the value of the category parameter to the instance variable category.
    self.count = count: Assigns the value of the count parameter to the instance variable count.
    self.is_borrowed = False: Initializes the is_borrowed instance variable to False. This variable indicates whether the book is currently
    borrowed or not.

def __str__(self):

    __str__ Method: This special method is called when the str() function is invoked on an instance of the class, or when the instance 
    is printed. It should return a string that is a “nice” representation of the instance.


return f"(ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Category: {self.category}, Count: {self.count})"

    Return Statement: Constructs and returns a formatted string that includes the book's ID, title, author, category, and count. This 
    string will be shown when the Book object is printed or converted to a string.

Example Usage:

book1 = Book(book_id="B001", title="1984", author="George Orwell", category="Dystopian", count=5)


------------------------------------------------------------------------------------------------------------------------------------------
Similary we can understand the class Member. It stores information about the members of the library.

Impoting important libraries:

import os                               # To handle files
from tabulate import tabulate           # To represent data
import pandas as pd                     # For representing the data as pandas Dataframe

------------------------------------------------------------------------------------------------------------------------------------------


class Library:

    Class Declaration: Defines a new class named Library. A class in Python is a blueprint for creating objects (a particular data structure).

Constructor Method

python

    def __init__(self):

    __init__ Method: This is the initializer method for the class. It's called when a new instance of the class is created.
    Parameters:
        self: Refers to the instance of the class being created. It's a reference to the current instance of the class and is used to access variables that belong to the class.

python

        self.books = []

    self.books = []: Initializes an empty list named books as an instance variable. This list will hold Book objects that represent the books in the library.

python

        self.members = []

    self.members = []: Initializes an empty list named members as an instance variable. This list will hold Member objects that represent the members of the library.

python

        self.load_books()

    self.load_books(): Calls the load_books method of the Library class. This method is supposed to load book data from a persistent storage (e.g., a file) and populate the self.books list with Book objects.

python

        self.load_members()

    self.load_members(): Calls the load_members method of the Library class. This method is supposed to load member data from a persistent 
    storage (e.g., a file) and populate the self.members list with Member objects.

Putting It All Together

When a new instance of the Library class is created, the following steps occur in sequence:

    Initialization of books List:
        An empty list named books is created to store Book objects. This list will later hold the books available in the library.

    Initialization of members List:
        An empty list named members is created to store Member objects. This list will later hold the members of the library.

    Loading Books:
        The load_books method is called to load the book data from a persistent storage and populate the books list with Book objects.

    Loading Members:
        The load_members method is called to load the member data from a persistent storage and populate the members list with Member objects.

These steps ensure that when the Library object is created, it has empty lists ready to store books and members, and it attempts to populate
these lists with data from persistent storage.

----------------------------------------------------------------------------------------------------------------------------------------------

  # Adding a new book 
    def add_book(self, book):

    Method Definition: This defines a method add_book that takes a single parameter book.
    Parameter:
        book: An instance of the Book class representing the book to be added.


        existing_book = self.find_book_by_id(book.book_id)

    Find Existing Book: Calls the find_book_by_id method with the book_id of the book to be 
                        added. This method searches for a book with the same ID in the library's collection.
    existing_book: Stores the result of the search. If a book with the same ID is found, existing_book will hold that book object; 
                   otherwise, it will be None.


        if existing_book:
            existing_book.count += 1

    Check if Book Exists: If existing_book is not None, it means a book with the same ID already exists in the library.
    Increment Count: Increases the count of the existing book by 1, indicating another copy of the same book is being added.


        else:
            self.books.append(book)

    Add New Book: If existing_book is None, it means the book is not already in the library.
    Append to List: Adds the new book to the books list.


        self.save_books()

    Save Changes: Calls the save_books method to save the updated list of books to the file books.txt.

remove_book Method


    # Removing all the copies of a particular book
    def remove_book(self, book_id):

    Method Definition: This defines a method remove_book that takes a single parameter book_id.
    Parameter:
        book_id: The ID of the book to be removed.


        self.books = [book for book in self.books if book.book_id != book_id]

    Remove Book: Creates a new list of books by iterating over the current list and including only those books whose book_id is not equal 
    to the given book_id. Effectively, this removes all copies of the book with the specified ID from the list.


        self.save_books()

    Save Changes: Calls the save_books method to save the updated list of books to the file books.txt.

save_books Method


    # Updating the books.txt file after every operation whenever Library class is instantiated
    def save_books(self):

    Method Definition: This defines a method save_books that takes no parameters.


        with open('books.txt', 'w') as f:

    Open File: Opens (or creates if it does not exist) a file named books.txt in write mode ('w').
    f: A file object used to write to the file.


            for book in self.books:

    Iterate Over Books: Loops through each book in the books list.


                f.write(f"{book.book_id},{book.title},{book.author},{book.category},{book.is_borrowed},{book.count}\n")

    Write Book Details: Writes the details of each book to the file books.txt in a comma-separated format.
        book.book_id: The ID of the book.
        book.title: The title of the book.
        book.author: The author of the book.
        book.category: The category of the book.
        book.is_borrowed: A boolean indicating whether the book is currently borrowed.
        book.count: The count of available copies of the book.
    Newline Character (\n): Ensures each book's details are written on a new line.
