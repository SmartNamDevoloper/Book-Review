# Project 1 

Web Programming with Python and JavaScript
The main objectives of this project was to
1. Become more comfortable with Python.
2. Gain experience with Flask.
3. Learn to use SQL to interact with databases.


Registration: Users are able to register for the website, providing a username and password.

Login: Users, once registered, are able to log in to the website with their username and password.

Logout: Logged in users are able to log out of the site.

Import: 
In a Python file called import.py separate from the web application, will take the books and import them into the PostgreSQL database.
A file called books.csv, which is a spreadsheet in CSV format of 5000 different books was provided.
Each one has an ISBN number, a title, an author, and a publication year. 

In the file create.sql the sql statements that were used to reate the tables are listed.
 
 
Search: Once a user has logged in, they are taken to a page where they can search for a book. 
Users should be able to type in the ISBN number of a book, the title of a book, or the author of a book. 
After performing the search, your website should display a list of possible matching results, or some sort of message if there were no matches.
If the user typed in only part of a title, ISBN, or author name, the search page will find matches for those as well!

Book Page: When users click on a book from the results of the search page, they will be taken to a book page, with details about the book: its title, author, publication year, ISBN number, and any reviews that users have left for the book on your website.

Review Submission: On the book page, users will be able to submit a review: consisting of a rating on a scale of 1 to 5, as well as a text component to the review where the user can write their opinion about a book.
Users will not be able to submit multiple reviews for the same book.

Goodreads Review Data: On the book details page, (if available) the average rating and number of ratings the work has received from Goodreads will be displayed.

API Access: If users make a GET request to the website’s /api/<isbn> route, where <isbn> is an ISBN number, your website will return a JSON response containing the book’s title, author, publication date, ISBN number, review count, and average score. The resulting JSON will follow the format:
{
    "title": "Memory",
    "author": "Doug Lloyd",
    "year": 2015,
    "isbn": "1632168146",
    "review_count": 28,
    "average_score": 5.0
}
If the requested ISBN number isn’t in the database, the website will return a customised 404 error page.

This project uses raw SQL commands (as via SQLAlchemy’s execute method) in order to make database queries. 


