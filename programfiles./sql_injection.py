from getpass import getpass
from mysql.connector import connect, Error

movie_id = input("Enter movie id: ")
reviewer_id = input("Enter reviewer id: ")
new_rating = input("Enter new rating: ")
update_query = """
UPDATE
    ratings
SET
    rating = "%s"
WHERE
    movie_id = "%s" AND reviewer_id = "%s";

SELECT *
FROM ratings
WHERE
    movie_id = "%s" AND reviewer_id = "%s"
""" % (
    new_rating,
    movie_id,
    reviewer_id,
    movie_id,
    reviewer_id,
)

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="databasewithpython2",
    ) as connection:
        with connection.cursor() as cursor:
            for result in cursor.execute(update_query, multi=True):
                if result.with_rows:
                    print(result.fetchall())
            connection.commit()

        select_query = """
        SELECT firstName, lastName
        FROM reviews
        """
        with connection.cursor() as cursor:
            cursor.execute(select_query)
            for reviewer in cursor.fetchall():
                print(reviewer)


except Error as e:
    print(e)


# The rating with movie_id=18 and reviewer_id=15 has been changed to 5.0. But if you were hacker, then you might send a hidden command in your input:

# 15"; UPDATE reviewers SET last_name = "A


# The above code displays the first_name and last_name for all records in the reviewers table. The SQL injection attack corrupted this table by changing the last_name of all records to "A".

# There’s a quick fix to prevent such attacks. Don’t add the query values provided by the user directly to your query string. Instead, update the modify_ratings.py script to send these query values as arguments to .execute():


# movie_id = input("Enter movie id: ")
# reviewer_id = input("Enter reviewer id: ")
# new_rating = input("Enter new rating: ")
# update_query = """
# UPDATE
#     ratings
# SET
#     rating = %s
# WHERE
#     movie_id = %s AND reviewer_id = %s;

# SELECT *
# FROM ratings
# WHERE
#     movie_id = %s AND reviewer_id = %s
# """
# val_tuple = (
#     new_rating,
#     movie_id,
#     reviewer_id,
#     movie_id,
#     reviewer_id,
# )

# try:
#     with connect(
#         host="localhost",
#         user=input("Enter username: "),
#         password=getpass("Enter password: "),
#         database="online_movie_rating",
#     ) as connection:
#         with connection.cursor() as cursor:
#             for result in cursor.execute(update_query, val_tuple, multi=True):
#                 if result.with_rows:
#                     print(result.fetchall())
#             connection.commit()
# except Error as e:
#     print(e)
# Notice that the % s placeholders are no longer in string quotes. Strings passed to the placeholders might contain some special characters. If necessary, these can be correctly escaped by the underlying library.

# cursor.execute() makes sure that the values in the tuple received as argument are of the required data type. If a user tries to sneak in some problematic characters, then the code will raise an exception:

# In this tutorial, you saw MySQL Connector/Python, which is the officially recommended means of interacting with a MySQL database from a Python application. There are two other popular connectors:

# mysqlclient is a library that is a close competitor to the official connector and is actively updated with new features. Because its core is written in C, it has better performance than the pure-Python official connector. A big drawback is that it’s fairly difficult to set up and install, especially on Windows.

# MySQLdb is a legacy software that’s still used in commercial applications. It’s written in C and is faster than MySQL Connector/Python but is available only for Python 2.

# These connectors act as interfaces between your program and a MySQL database, and you send your SQL queries through them. But many developers prefer using an object-oriented paradigm rather than SQL queries to manipulate data.

# Object-relational mapping(ORM) is a technique that allows you to query and manipulate data from a database directly using an object-oriented language. An ORM library encapsulates the code needed to manipulate data, which eliminates the need to use even a tiny bit of SQL. Here are the most popular Python ORMs for SQL-based databases:

# SQLAlchemy is an ORM that facilitates communication between Python and other SQL databases. You can create different engines for different databases like MySQL, PostgreSQL, SQLite, and so on. SQLAlchemy is commonly used alongside the pandas library to provide complete data-handling functionality.

# peewee is a lightweight and fast ORM that’s quick to set up. This is quite useful when your interaction with the database is limited to extracting a few records. For example, if you need to copy selected records from a MySQL database into a CSV file, then peewee might be your best choice.

# Django ORM is one of the most powerful features of Django and is supplied alongside the Django web framework. It can interact with a variety of databases such as SQLite, PostgreSQL, and MySQL. Many Django-based applications use the Django ORM for data modeling and basic queries but often switch to SQLAlchemy for more complex requirements.

# You might find one of these approaches to be more suitable for your application. If you’re not sure which one to use, then it’s best to go with the officially recommended MySQL Connector/Python that you saw in action in this tutorial.
