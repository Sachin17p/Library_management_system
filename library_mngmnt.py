#!/usr/bin/env python
# coding: utf-8

# The second line mentions the unicode is implemented to represent non-English characters


# Defining the class Book to handle the book attributes and return a string with all the attributes when called
class Book:
    def __init__(self,book_id,title,author,category,count):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.count = count
        self.is_borrowed = False
        
    def __str__(self):
        return f"(ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Category: {self.category}, Count: {self.count})"



# Defining the class Member to handle the members attributes and return a string with all the info when called
class Member:
    def __init__(self,user_id,name,mail):
        self.name = name 
        self.user_id = user_id
        self.mail = mail 
        self.borrowed_books = []
        
    def __str__(self):
        self.borrowed_books_str = ', '.join(f"{book.book_id}:{book.title}" for book in self.borrowed_books)
        return f"(User ID: {self.user_id}, Name: {self.name}, Mail: {self.mail}, Borrowed Books: {self.borrowed_books_str})"



# Importing necessary libraries
import os                               # To handle files
from tabulate import tabulate           # To represent data
import pandas as pd                     # For representing the data as pandas Dataframe



# Defining the class Library to carry out all the necessary operations of the library
class Library:

    # The constructor method
    def __init__(self):
        self.books = []
        self.members = []
        self.load_books()
        self.load_members()
        

    # Adding a new book 
    def add_book(self, book):
        # Validate book_id format
        if not (book.book_id.startswith('b') and book.book_id[1:].isdigit()):
            print("\033[91mInvalid Book ID. Valid book ID starts with 'b' followed by a number\033[0m")
            return

        existing_book_by_id = self.find_book_by_id(book.book_id)

        # Checking if the book already exists
        if existing_book_by_id:
            if existing_book_by_id.title != book.title:
                print("\033[91mError! That book ID had a different book. Use another book ID\033[0m")
                return
            elif (existing_book_by_id.author == book.author and
                  existing_book_by_id.category == book.category):
                existing_book_by_id.count += 1
                print("\033[92mBook count incremented successfully!\033[0m")
            else:
                print("\033[91mError! That book ID had a different book. Use another book ID\033[0m")
                return
        else:
            self.books.append(book)
            print("\033[92mBook added successfully!\033[0m")
        self.save_books()

    # Finding a book by its title
    def find_book_by_title(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None


    # Removing all the copies of a particular book
    def remove_book(self,book):
        self.books = [book for book in self.books if book.book_id != book_id]
        self.save_book()

        
    # Updating the books.txt file after every operation whenever Library class is instantiated
    def save_books(self):
        with open('books.txt', 'w') as f:
            for book in self.books:
                f.write(f"{book.book_id},{book.title},{book.author},{book.category},{book.is_borrowed},{book.count}\n")



    # Updating the members.txt file after every operation whenever Library class is instantiated
    def save_members(self):
        with open('members.txt', 'w') as f:
            for member in self.members:
                borrowed_books_str = ','.join(book.book_id for book in member.borrowed_books)
                f.write(f"{member.user_id},{member.name},{member.mail},{borrowed_books_str}\n")


    # Adding a new member after checking if it already exists
    def add_member(self, member):
        # Validate user_id format
        if not (member.user_id.startswith('m') and member.user_id[1:].isdigit()):
            print("\033[91mInvalid User ID. Valid user ID starts with 'm' followed by a number\033[0m")
            return

        # Check if the user_id already exists
        existing_member_by_id = self.find_member_by_id(member.user_id)
        if existing_member_by_id:
            print("\033[91mError! That user ID already exists. Use another user ID\033[0m")
            return

        # Check if the mail ID already exists
        for existing_member in self.members:
            if existing_member.mail == member.mail:
                print("\033[91mEnter a different mail ID, the entered mail ID already exists.\033[0m")
                return

        # Add the new member if no conflicts are found
        self.members.append(member)
        self.save_members()
        print("\033[92mMember added successfully!\033[0m")

    # Finding a member by its name
    def find_member_by_name(self, name):
        for member in self.members:
            if member.name == name:
                return member
        return None


    # Removing a member 
    def remove_member(self, user_id):
        self.members = [member for member in self.members if member.user_id != user_id]
        self.save_members()


    # Borrowing a book by checking if that book and at least one copy of the same is available
    def borrow_book(self, user_id, book_id):
        member = self.find_member_by_id(user_id)
        if not member:
            print("\033[91mMember not found in database! Add your details to the database!\033[0m")
        book = self.find_book_by_id(book_id)
        if member and book:
            if book.count > 0:
                book.count -= 1
                member.borrowed_books.append(book)
                self.save_books()
                self.save_members()
                return True
            else:
                print("\033[91mNo copies available.\033[0m")
        return False



    # Returning a borrowed book 
    def return_book(self, user_id, book_id):
        member = self.find_member_by_id(user_id)
        book = self.find_book_by_id(book_id)
        if member and book:
            if book in member.borrowed_books:
                book.count += 1
                member.borrowed_books = [b for b in member.borrowed_books if b.book_id != book_id]
                self.save_books()
                self.save_members()
                return True
            else:
                # Adding the book to the library if it was not previously in the library
                book_to_return = Book(book_id, "Unknown Title", "Unknown Author", "Unknown Category", 1)
                self.add_book(book_to_return)
                return True
        return False


    # Listing all the available books and their info
    def list_books(self):
        # Create a DataFrame
        df = pd.DataFrame([{
            'Book ID': book.book_id,
            'Title': book.title,
            'Author': book.author,
            'Category': book.category,
            'Count': book.count
        } for book in self.books])

        return df


    # Listing all the current member of the library with all the info
    def list_members(self):
    # Create a list of dictionaries, each representing a member
        members_data = [{
            'User ID': member.user_id,
            'Name': member.name,
            'Mail': member.mail,
            'Borrowed Books': f"[{', '.join(f'{book.book_id}: {book.title}' for book in member.borrowed_books)}]",
            'Borrowed Book Count': len(member.borrowed_books)
        } for member in self.members]

        return pd.DataFrame(members_data)


    # Finding a book by its book_id 
    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None


    # Finding a member by its member_id
    def find_member_by_id(self, user_id):
        for member in self.members:
            if member.user_id == user_id:
                return member
        return None


    # Searching through the books by its book_id
    def search_books_by_book_id(self, book_id):
        return [book for book in self.books if book_id.lower() in book.book_id.lower()]


    # Searching through the books by title
    def search_books_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    # Searching through the books by author name
    def search_books_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]


    # Searching through the books by their category
    def search_books_by_category(self, category):
        return [book for book in self.books if category.lower() in book.category.lower()]


    # Loading books into the books.txt file 
    def load_books(self):
        if os.path.exists('books.txt'):
            with open('books.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    book_id = parts[0]
                    title = parts[1]
                    author = parts[2]
                    category = parts[3]
                    count = int(parts[5])
                    book = Book(book_id, title, author, category, count)
                    self.books.append(book)


    # Loading the members and updated info into members.txt file
    def load_members(self):
        if os.path.exists('members.txt'):
            with open('members.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    user_id = parts[0]           # 1st argument of members.txt
                    name = parts[1]              # 2nd argument of members.txt
                    mail = parts[2]              # 3rd argument of members.txt
                    borrowed_books = parts[3:]   # 4th and later arguments of members.txt

                    member = Member(user_id, name, mail)
                    for book_id in borrowed_books:
                        if book_id:
                            book = self.find_book_by_id(book_id)
                            if book:
                                member.borrowed_books.append(book)
                    self.members.append(member)




# Ewxecuting the program with all the options
if __name__ == "__main__":
    library = Library()

    while True:
        print("\nOpen Source Library Management System")
        print("1. Add a New Book")
        print("2. Remove a Book")
        print("3. Add a New Member")
        print("4. Remove a Member")
        print("5. Borrow a Book")
        print("6. Return a Book")
        print("7. List all Books")
        print("8. List all Members")
        print("9. Search Books by Title")
        print("10. Search Books by Author")
        print("11. Search Books by Category")
        print("12. Search Books by Book ID")
        print("13. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            book_id = input("Enter book ID: ")
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            category = input("Enter book category: ")
            library.add_book(Book(book_id, title, author, category, 1))
            
        
        elif choice == '2':
            book_id = input("Enter book ID to remove: ")
            library.remove_book(book_id)
            print("\033[92mBook removed successfully.\033[0m")
        
        elif choice == '3':
            user_id = input("Enter member ID: ")
            name = input("Enter member name: ")
            mail = input("Enter member email: ")
            library.add_member(Member(user_id, name, mail))
        
        elif choice == '4':
            user_id = input("Enter member ID to remove: ")
            library.remove_member(user_id)
            print("\033[92mMember removed successfully.\033[0m")
        
        elif choice == '5':
            user_id = input("Enter member ID: ")
            book_id = input("Enter book ID to borrow: ")
            if library.borrow_book(user_id, book_id):
                print("\033[92mBook borrowed successfully.\033[0m")
            else:
                print("\033[91mBorrowing failed.\033[0m")
        
        elif choice == '6':
            user_id = input("Enter member ID: ")
            book_id = input("Enter book ID to return: ")
            if library.return_book(user_id, book_id):
                print("\033[92mBook returned successfully.\033[0m")
            else:
                print("\033[91mReturning failed.\033[0m")
        

        elif choice == '7':
            print("Books in Library:")
            df_books = library.list_books()
            print(tabulate(df_books, headers='keys', tablefmt='fancy_grid'))



        elif choice == '8':
            print("Members in Library:")
            df_members = library.list_members()
            print(tabulate(df_members, headers='keys', tablefmt='fancy_grid'))



        elif choice == '9':
            title = input("Enter book title to search: ")
            results = library.search_books_by_title(title)
            print("Search results:")
            for book in results:
                print(book)
        
        elif choice == '10':
            author = input("Enter book author to search: ")
            results = library.search_books_by_author(author)
            print("Search results:")
            for book in results:
                print(book)
        
        elif choice == '11':
            category = input("Enter book category: ")
            results = library.search_books_by_category(category)
            print("Search results: ")
            for book in results:
                print(book)
            
        elif choice == '12':
            book_id = input("Enter Book ID: ")
            results = library.search_books_by_book_id(book_id)
            for book in results:
                print(book)
                
        elif choice == '13':
            print("Exiting the system.")
            break
        
        else:
            print("Invalid choice. Please try again.")




