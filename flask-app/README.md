# Project 1

Web Programming with Python and JavaScript

# application.py

This file represents my flask application. Below is the desription of diffrent functions and routes in the app.

## login

This is the default index page for the webapp and lets the user login. If user has not signed up, it also has a link that takes the user to signup page. Keep in mind the user ID is cse ssensitive. The page wont let you proceded if you keep user Id or password fields empty. For wrong user ID or password, an error message 'Invalid credentials' is shown to the user. If the user logs in successfully , user is redirected to **searchbooks** page. Successful login also puts the user object containing user info in session.

## signup

Thjis page lets a new user signup. The page does not let the user signup if any of thre fields in the signup form are empty. If the user ID typed by the user aleady exists in the database, user is shown a message ans requested to use a diffrent user Id. Usually user Id should be case insensitive but in this application both user Id and password are supposed to be case sensitive. Also, ideally it would be better to store some has value of password but for now we are storing password in plain text. 

## signout

This button removes user from session and redirect user back to login screen.

## searchbooks

To acces this page, user should be logged in.

This page is where user lands when logged in. User may use this page to search for books based no author, title or isbn. User may use exact author, title and/or isbn OR user may use a substring of the actuasl author, title or isbn. The search button in the form is intentionally kept as GET not POST since there is nothing to hide in the search. If no field is entered and user hits Search button , nothing will happen. If any of the field is there, a search is done in the db. Either search results show the list of books mathcing search criteria or shows a message if there are no books matching search criteria. The ISBN of the books is shown as a link that would take you the details of that particular book.


## books/\<isbn\>

To acces this page, user should be logged in.

This page shows info abotu the particular book with isbn as in the url. If the isbn does not exist, this page show an error page. If the book does exists, all info about the book is shown along with the reviews available for that book from current user, other users and info from goodreads (if available).

## api/books/\<isbn\>

To acces this page, user is NOT required to be logged in.

This is a public API provided through this app. If the isbn provided does not exists , it gives a 404 and a message. If the isbn exists in the db, this api returns the book's info in json forma.t It gets the info both from the webapp db and goodreads API.

## getgoodreadreviews(isbn)

This function gets the info about the book by calling godread api. If the book does not exists, it returns avegage rating as 0.0 and rating count as -1

# templates

This section includes documentation about all the templates in this webapp.

## layout.html
This layout is included in all pages. It importa the bootstrap lib in all pages. It say Hi to the user asnd adds a logout button is user is logged in. It also puts all the content of pages in a container div.

## signup.html

This page lets a new user signup.

## login.html

This is the home/welcome/index page of the webapp and lets a user sign in. 

## searchbooks.html

This page lets the user search for books. User may use any of the title, author and/or isbn as the criteria for search. Search is case sensitive.

## book.html

This page shows information about a particular book along with the reviews available. It also lets the current user leave a review. Once current user left a review, she/he may not edit the review.

## error.html

User is redirected to this page if the isbn entered in the url does not exist. 

# Other stuff

## createtables.sql

This files create 3 diffrent tables - users, books and reviews
- 'user' table contains user infromation like user id , password, user's name etc.
- 'book' table contains all of the books information. Books info was imported from the 500 books in the csv provided.
- 'reviews' table contains the reviews of a book from a user and references back to user and book tables.

## import.py

This file imports the books' information from books.csv. First line is ignored since it was the header. DB URL is read from DATABASE_URL

## requirements.txt

I added **requests** package to the provided file to also import the requests package to make necessary API calls to goodreads.

