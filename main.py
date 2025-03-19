import streamlit as st
import json
import os

data_file = 'library.txt'

def load_library():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, 'w') as file:
        json.dump(library, file, indent=4)

def add_book(library, title, author, year, genre, read):
    new_book = {
        'title': title,
        'author': author,
        'year': year,
        'genre': genre,
        'read': read
    }
    library.append(new_book)
    save_library(library)

def remove_book(library, title):
    library = [book for book in library if book['title'].lower() != title.lower()]
    save_library(library)

def search_library(library, search_by, search_term):
    return [book for book in library if search_term.lower() in book[search_by].lower()]

def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book['read'])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0  
    return total_books, read_books, percentage_read

st.title("📚 Library Management System")

library = load_library()

menu = ["Add Book", "Remove Book", "Search Books", "View All Books", "Statistics"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Add Book":
    st.subheader("📖 Add a New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.text_input("Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        add_book(library, title, author, year, genre, read)
        st.success(f'Book "{title}" added successfully!')

elif choice == "Remove Book":
    st.subheader("🗑️ Remove a Book")
    title = st.text_input("Enter the title of the book to remove")
    if st.button("Remove Book"):
        remove_book(library, title)
        st.success(f'Book "{title}" removed successfully!')

elif choice == "Search Books":
    st.subheader("🔍 Search Books")
    search_by = st.selectbox("Search by", ["title", "author"])
    search_term = st.text_input(f"Enter {search_by} to search")
    if st.button("Search"):
        results = search_library(library, search_by, search_term)
        if results:
            for book in results:
                st.write(f'📖 {book["title"]} by {book["author"]} - {book["year"]} - {book["genre"]} - {"Read" if book["read"] else "Unread"}')
        else:
            st.warning("No books found.")

elif choice == "View All Books":
    st.subheader("📚 All Books")
    if library:
        for book in library:
            st.write(f'📖 {book["title"]} by {book["author"]} - {book["year"]} - {book["genre"]} - {"Read" if book["read"] else "Unread"}')
    else:
        st.warning("The library is empty.")

elif choice == "Statistics":
    st.subheader("📊 Library Statistics")
    total_books, read_books, percentage_read = display_statistics(library)
    st.write(f'Total Books: {total_books}')
    st.write(f'Read Books: {read_books}')
    st.write(f'Percentage Read: {percentage_read:.2f}%')
