#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


class Member:
    def __init__(self,user_id,name,mail):
        self.name = name 
        self.user_id = user_id
        self.mail = mail 
        self.borrowed_books = []
        
    def __str__(self):
        self.borrowed_books_str = ', '.join(f"{book.book_id}:{book.title}" for book in self.borrowed_books)
        return f"(User ID: {self.user_id}, Name: {self.name}, Mail: {self.mail}, Borrowed Books: {self.borrowed_books_str})"


# In[7]:


import os
from tabulate import tabulate
import pandas as pd

class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.load_books()
        self.load_members()
        
    def add_book(self, book):
        existing_book = self.find_book_by_id(book.book_id)
        if existing_book:
            existing_book.count += 1
        else:
            self.books.append(book)
        self.save_books()


    def remove_book(self,book):
        self.books = [book for book in self.books if book.book_id != book_id]
        self.save_book()

        
        
    def save_books(self):
        with open('books.txt', 'w') as f:
            for book in self.books:
                f.write(f"{book.book_id},{book.title},{book.author},{book.category},{book.is_borrowed},{book.count}\n")
                
    def save_members(self):
        with open('members.txt', 'w') as f:
            for member in self.members:
                borrowed_books_str = ','.join(book.book_id for book in member.borrowed_books)
                f.write(f"{member.user_id},{member.name},{member.mail},{borrowed_books_str}\n")
        
    def add_member(self, member):
        if self.find_member_by_id(member.user_id):
            print("Member with that ID already exists.")
            return
        
        self.members.append(member)
        self.save_members()
        print("Member added successfully!")


    def remove_member(self, user_id):
        self.members = [member for member in self.members if member.user_id != user_id]
        self.save_members()

        
    def borrow_book(self, user_id, book_id):
        member = self.find_member_by_id(user_id)
        if not member:
            print("Member not found in database! Add your details to the database!")
#            member = Member(user_id, name, mail)
#            self.add_member(member)
        book = self.find_book_by_id(book_id)
        if member and book and book.count > 0:
            book.count -= 1
            member.borrowed_books.append(book)
            self.save_books()
            self.save_members()
            return True
        return False

    
    
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
    
#     def list_books(self):
#         return "\n".join(str(book) for book in self.books)
    
#     def list_members(self):
#         return "\n".join(str(member) for member in self.members)

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

    def list_members(self):
        # Create a list of dictionaries, each representing a member
        members_data = [{
            'User ID': member.user_id,
            'Name': member.name,
            'Mail': member.mail,
            'Borrowed Books': ', '.join(f"{book.book_id}:{book.title}" for book in member.borrowed_books),
            'Borrowed Book Count': len(member.borrowed_books)
        } for member in self.members]

        # Convert the list of dictionaries to a DataFrame
        return pd.DataFrame(members_data)

    def find_book_by_id(self, book_id):
        for book in self.books:
            if book.book_id == book_id:
                return book
        return None

    def find_member_by_id(self, user_id):
        for member in self.members:
            if member.user_id == user_id:
                return member
        return None
    

    def search_books_by_book_id(self, book_id):
        return [book for book in self.books if book_id.lower() in book.book_id.lower()]

    
    def search_books_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def search_books_by_author(self, author):
        return [book for book in self.books if author.lower() in book.author.lower()]

    def search_books_by_category(self, category):
        return [book for book in self.books if category.lower() in book.category.lower()]

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

    def load_members(self):
        if os.path.exists('members.txt'):
            with open('members.txt', 'r') as f:
                for line in f:
                    parts = line.strip().split(',')
                    user_id = parts[0]
                    name = parts[1]
                    mail = parts[2]
                    borrowed_books = parts[3:]
                    
                    member = Member(user_id, name, mail)
                    for book_id in borrowed_books:
                        if book_id:
                            book = self.find_book_by_id(book_id)
                            if book:
                                member.borrowed_books.append(book)
                    self.members.append(member)


# In[8]:


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
            print("Book added successfully.")
        
        elif choice == '2':
            book_id = input("Enter book ID to remove: ")
            library.remove_book(book_id)
            print("Book removed successfully.")
        
        elif choice == '3':
            user_id = input("Enter member ID: ")
            name = input("Enter member name: ")
            mail = input("Enter member email: ")
            library.add_member(Member(user_id, name, mail))
#             print("Member added successfully.")
        
        elif choice == '4':
            user_id = input("Enter member ID to remove: ")
            library.remove_member(user_id)
            print("Member removed successfully.")
        
        elif choice == '5':
            user_id = input("Enter member ID: ")
#            name = input("Enter member name: ")
#            mail = input("Enter member email: ")
            book_id = input("Enter book ID to borrow: ")
            if library.borrow_book(user_id, book_id):
                print("Book borrowed successfully.")
            else:
                print("Borrowing failed.")
        
        elif choice == '6':
            user_id = input("Enter member ID: ")
            book_id = input("Enter book ID to return: ")
            if library.return_book(user_id, book_id):
                print("Book returned successfully.")
            else:
                print("Returning failed.")
        
#         elif choice == '7':
#             print("Books in Library:")
#             print(library.list_books())

        elif choice == '7':
            print("Books in Library:")
            df_books = library.list_books()
            print(tabulate(df_books, headers='keys', tablefmt='fancy_grid'))


#         elif choice == '8':
#             print("Members in Library:")
#             print(library.list_members())


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


# In[ ]:





# In[ ]:




