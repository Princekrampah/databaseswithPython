from mysql.connector import connect, Error
from getpass import getpass

# create a database
# try:
#     with connect(
#         host='localhost',
#         user=input('Username: '),
#         password=getpass("Password: ")
#     ) as connection:
#         print(connection)
#         create_db = "CREATE DATABASE IF NOT EXISTS databasewithpython2;"
#         show_dbs = "SHOW DATABASES;"
#         with connection.cursor() as cursor:
#             cursor.execute(create_db)
#             print("Database created...")
#             cursor.execute(show_dbs)
#             for db in cursor:
#                 print(db)
# except Error as e:
#     print(e)

# connect to existing database

# In the context of SQL, data definition or data description language (DDL) is a syntax for creating and modifying database objects such as tables, indices, and ...
try:
    with connect(
        host='localhost',
        user=input("username: "),
        password=getpass("Password: "),
        database='databasewithpython2'
    ) as connection:
        print(connection)

        create_movies = """
            CREATE TABLE IF NOT EXISTS movies (
                id INT AUTO_INCREMENT,
                title VARCHAR(50),
                release_year YEAR(4),
                genre VARCHAR(20),
                collection_in_mil INT,
                PRIMARY KEY(id)
            );
        """

        with connection.cursor() as cursor:
            cursor.execute(create_movies)
            connection.commit()
            print("movie table created")

        create_reviewers = """
            CREATE TABLE IF NOT EXISTS reviews (
                id INT AUTO_INCREMENT,
                firstName VARCHAR(50),
                lastName VARCHAR(50),
                PRIMARY KEY (id)
            );   
        """

        with connection.cursor() as cursor:
            cursor.execute(create_reviewers)
            connection.commit()
            print("reviewers table created")

        create_rating = """
            CREATE TABLE IF NOT EXISTS ratings(
                movie_id INT,
                reviewer_id INT,
                rating DECIMAL(2, 1),
                FOREIGN KEY (movie_id) REFERENCES movies (id),
                FOREIGN KEY (reviewer_id) REFERENCES reviews (id),
                PRIMARY KEY (movie_id, reviewer_id)
            );
        """

        with connection.cursor() as cursor:
            cursor.execute(create_rating)
            connection.commit()
            print("ratings table created")

        # You may choose to reuse the same cursor for multiple executions. In that case, all executions would become one atomic transaction rather than multiple separate transactions. For example, you can execute all CREATE TABLE statements with one cursor and then commit your transaction only once:

        # with connection.cursor() as cursor:
            # cursor.execute(create_movies_table_query)
            # cursor.execute(create_reviewers_table_query)
            # cursor.execute(create_ratings_table_query)
            # connection.commit()

        # The above code will first execute all three CREATE statements. Then it will send a COMMIT command to the MySQL server that commits your transaction. You can also use .rollback() to send a ROLLBACK command to the MySQL server and remove all data changes from the transaction.

        # SHOW TABLE SCHEMA WITH DESCRIBE <TABLE NAME>

        show_schema = "DESCRIBE movies"
        with connection.cursor() as cursor:
            cursor.execute(show_schema)
            results = cursor.fetchall()
            for row in results:
                print(row)

        # In the movies table, you have a column called collection_in_mil, which contains a movie’s box office collection in millions of dollars. You can write the following MySQL statement to modify the data type of collection_in_mil attribute from INT to DECIMAL:

        alt_table = """
            ALTER TABLE movies MODIFY COLUMN collection_in_mil DECIMAL (4, 1);
        """

        with connection.cursor() as cursor:
            cursor.execute(alt_table)
            cursor.execute(show_schema)
            results = cursor.fetchall()
            print("Movie Table Schema after alteration:")
            for row in results:
                print(row)

        insert_movies_query = """
            INSERT INTO movies (title, release_year, genre, collection_in_mil)
            VALUES
                ("Forrest Gump", 1994, "Drama", 330.2),
                ("3 Idiots", 2009, "Drama", 2.4),
                ("Eternal Sunshine of the Spotless Mind", 2004, "Drama", 34.5),
                ("Good Will Hunting", 1997, "Drama", 138.1),
                ("Skyfall", 2012, "Action", 304.6),
                ("Gladiator", 2000, "Action", 188.7),
                ("Black", 2005, "Drama", 3.0),
                ("Titanic", 1997, "Romance", 659.2),
                ("The Shawshank Redemption", 1994, "Drama",28.4),
                ("Udaan", 2010, "Drama", 1.5),
                ("Home Alone", 1990, "Comedy", 286.9),
                ("Casablanca", 1942, "Romance", 1.0),
                ("Avengers: Endgame", 2019, "Action", 858.8),
                ("Night of the Living Dead", 1968, "Horror", 2.5),
                ("The Godfather", 1972, "Crime", 135.6),
                ("Haider", 2014, "Action", 4.2),
                ("Inception", 2010, "Adventure", 293.7),
                ("Evil", 2003, "Horror", 1.3),
                ("Toy Story 4", 2019, "Animation", 434.9),
                ("Air Force One", 1997, "Drama", 138.1),
                ("The Dark Knight", 2008, "Action",535.4),
                ("Bhaag Milkha Bhaag", 2013, "Sport", 4.1),
                ("The Lion King", 1994, "Animation", 423.6),
                ("Pulp Fiction", 1994, "Crime", 108.8),
                ("Kai Po Che", 2013, "Sport", 6.0),
                ("Beasts of No Nation", 2015, "War", 1.4),
                ("Andadhun", 2018, "Thriller", 2.9),
                ("The Silence of the Lambs", 1991, "Crime", 68.2),
                ("Deadpool", 2016, "Action", 363.6),
                ("Drishyam", 2015, "Mystery", 3.0)
            """
        with connection.cursor() as cursor:
            cursor.execute(insert_movies_query)
            connection.commit()

        # Using .executemany()
        # The previous approach is more suitable when the number of records is fairly small and you can write these records directly into the code. But this is rarely true. You’ll often have this data stored in some other file, or the data will be generated by a different script and will need to be added to the MySQL database.

        # This is where .executemany() comes in handy. It accepts two parameters:

        # A query that contains placeholders for the records that need to be inserted
        # A list that contains all records that you wish to insert

        insert_reviewers_query = """
            INSERT INTO reviews
            (firstName, lastName)
            VALUES ( %s, %s )
            """
        reviewers_records = [
            ("Chaitanya", "Baweja"),
            ("Mary", "Cooper"),
            ("John", "Wayne"),
            ("Thomas", "Stoneman"),
            ("Penny", "Hofstadter"),
            ("Mitchell", "Marsh"),
            ("Wyatt", "Skaggs"),
            ("Andre", "Veiga"),
            ("Sheldon", "Cooper"),
            ("Kimbra", "Masters"),
            ("Kat", "Dennings"),
            ("Bruce", "Wayne"),
            ("Domingo", "Cortes"),
            ("Rajesh", "Koothrappali"),
            ("Ben", "Glocker"),
            ("Mahinder", "Dhoni"),
            ("Akbar", "Khan"),
            ("Howard", "Wolowitz"),
            ("Pinkie", "Petit"),
            ("Gurkaran", "Singh"),
            ("Amy", "Farah Fowler"),
            ("Marlon", "Crafford"),
        ]
        with connection.cursor() as cursor:
            cursor.executemany(insert_reviewers_query, reviewers_records)
            connection.commit()

        insert_ratings_query = """
            INSERT INTO ratings
            (rating, movie_id, reviewer_id)
            VALUES ( %s, %s, %s)
            """
        ratings_records = [
            (6.4, 17, 5), (5.6, 19, 1), (6.3, 22, 14), (5.1, 21, 17),
            (5.0, 5, 5), (6.5, 21, 5), (8.5, 30, 13), (9.7, 6, 4),
            (8.5, 24, 12), (9.9, 14, 9), (8.7, 26, 14), (9.9, 6, 10),
            (5.1, 30, 6), (5.4, 18, 16), (6.2, 6, 20), (7.3, 21, 19),
            (8.1, 17, 18), (5.0, 7, 2), (9.8, 23, 3), (8.0, 22, 9),
            (8.5, 11, 13), (5.0, 5, 11), (5.7, 8, 2), (7.6, 25, 19),
            (5.2, 18, 15), (9.7, 13, 3), (5.8, 18, 8), (5.8, 30, 15),
            (8.4, 21, 18), (6.2, 23, 16), (7.0, 10, 18), (9.5, 30, 20),
            (8.9, 3, 19), (6.4, 12, 2), (7.8, 12, 22), (9.9, 15, 13),
            (7.5, 20, 17), (9.0, 25, 6), (8.5, 23, 2), (5.3, 30, 17),
            (6.4, 5, 10), (8.1, 5, 21), (5.7, 22, 1), (6.3, 28, 4),
            (9.8, 13, 1)
        ]
        with connection.cursor() as cursor:
            cursor.executemany(insert_ratings_query, ratings_records)
            connection.commit()

        # If you don’t want to use the LIMIT clause and you don’t need to fetch all the records, then the cursor object has .fetchone() and .fetchmany() methods as well:

        # .fetchone() retrieves either the next row of the result, as a tuple, or None if no more rows are available.
        # .fetchmany() retrieves the next set of rows from the result as a list of tuples. It has a size argument, which defaults to 1, that you can use to specify the number of rows you need to fetch. If no more rows are available, then the method returns an empty list.
        # Try retrieving the titles of the five highest-grossing movies concatenated with their release years again, but this time use .fetchmany():

except Error as e:
    print(e)
