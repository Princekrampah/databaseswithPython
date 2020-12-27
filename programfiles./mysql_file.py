import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

PASSWD = os.getenv("DATABASE_PWD")


def create_connection(host_name, user_name, user_pwd):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_pwd
        )
        print("Connection established")
    except Error as e:
        print(f"The error {e} occured")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print(f"{query.split(' ')[2]} Database created.")
    except Error as e:
        print(f"{e} error occured")


def create_connection_to_db(host_name, user_name, user_pwd, db_name):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_pwd,
            database=db_name
        )
        print("Connection established")
    except Error as e:
        print(f"The error {e} occured")

    return connection


connection = create_connection("127.0.0.1", "root", PASSWD)

# create_db_query = "CREATE DATABASE databasewithpython"
# create_database(connection, create_db_query)

connection = create_connection_to_db(
    "127.0.0.1", "root", PASSWD, "databasewithpython")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Done")
    except Error as e:
        print(f"{e} occured")


create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT,
        name TEXT NOT NULL,
        age INT,
        gender TEXT,
        nationality TEXT,
        PRIMARY KEY (id)
    ) ENGINE = InnoDB;
"""

execute_query(connection, create_users_table)


create_posts_table = """
  CREATE TABLE IF NOT EXISTS posts(
    id INT AUTO_INCREMENT, 
    title TEXT NOT NULL, 
    description TEXT NOT NULL, 
    user_id INTEGER NOT NULL, 
    FOREIGN KEY (user_id) REFERENCES users (id),
    PRIMARY KEY (id)
) ENGINE = InnoDB;
"""


execute_query(connection, create_posts_table)


create_comments_table = """
    CREATE TABLE IF NOT EXISTS comments (
        id INT  AUTO_INCREMENT,
        text TEXT NOT NULL,
        user_id INT NOT NULL,
        post_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (post_id) REFERENCES posts(id),
        PRIMARY KEY (id)
    )ENGINE = InnoDB;
"""


execute_query(connection, create_comments_table)


create_likes_table = """
    CREATE TABLE IF NOT EXISTS likes (
        id INT AUTO_INCREMENT,
        user_id INT NOT NULL,
        post_id INT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (post_id) REFERENCES posts(id),
        PRIMARY KEY (id)
    ) ENGINE = InnoDB;
"""

execute_query(connection, create_likes_table)

create_users = """
INSERT INTO
  `users` (`name`, `age`, `gender`, `nationality`)
VALUES
  ('James', 25, 'male', 'USA'),
  ('Leila', 32, 'female', 'France'),
  ('Brigitte', 35, 'female', 'England'),
  ('Mike', 40, 'male', 'Denmark'),
  ('Elizabeth', 21, 'female', 'Canada');
"""

# execute_query(connection, create_users)


create_posts = """
INSERT INTO
  posts (title, description, user_id)
VALUES
  ("Happy", "I am feeling very happy today", 1),
  ("Hot Weather", "The weather is very hot today", 2),
  ("Help", "I need some help with my work", 2),
  ("Great News", "I am getting married", 1),
  ("Interesting Game", "It was a fantastic game of tennis", 5),
  ("Party", "Anyone up for a late-night party today?", 3);
"""

# execute_query(connection, create_posts)


create_comments = """
INSERT INTO
  comments (text, user_id, post_id)
VALUES
  ('Count me in', 1, 6),
  ('What sort of help?', 5, 3),
  ('Congrats buddy', 2, 4),
  ('I was rooting for Nadal though', 4, 5),
  ('Help with your thesis?', 2, 3),
  ('Many congratulations', 5, 4);
"""

create_likes = """
INSERT INTO
  likes (user_id, post_id)
VALUES
  (1, 6),
  (2, 3),
  (1, 5),
  (5, 4),
  (2, 4),
  (4, 2),
  (3, 6);
"""

# execute_query(connection, create_comments)
# execute_query(connection, create_likes)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    results = None
    try:
        cursor.execute(query)
        results = cursor.fetchall()
    except Error as e:
        print(e)

    return results

# Queries


# Joint
users_posts = """
    SELECT 
        users.id,
        users.name,
        posts.description
    FROM
        users
    INNER JOIN posts ON posts.id = users.id;
"""

results = execute_read_query(connection, users_posts)

for record in results:
    print(record)

print()

mutiple_joins = """
SELECT
  posts.description as post,
  text as comment,
  name
FROM
  posts
  INNER JOIN comments ON posts.id = comments.post_id
  INNER JOIN users ON users.id = comments.user_id
"""


results = execute_read_query(connection, mutiple_joins)

for record in results:
    print(record)

print()

post_likes = """
    SELECT
        posts.description as post,
        COUNT(likes.id) as likes
    FROM
        posts,
        likes
    WHERE
        posts.id = likes.post_id
    GROUP BY
        likes.post_id;
"""

post_like_other = """
    SELECT
        description as post,
        COUNT(likes.post_id)
    FROM
        posts
        INNER JOIN likes ON posts.id = likes.post_id
    GROUP BY
        likes.post_id
"""


results = execute_read_query(connection, post_like_other)

for record in results:
    print(record)

print()

# update tables

update = """
    UPDATE
        posts
    SET
        description = "Updated post"
    WHERE
        id = 3;
"""

execute_query(connection, update)

print(execute_read_query(connection, "SELECT * FROM posts  WHERE id = 3"))

# Delete

print(execute_read_query(connection, "SELECT * FROM comments  WHERE id = 3"))
print()
print()

execute_query(connection, "DELETE FROM comments WHERE id = 2")


print(execute_read_query(connection, "SELECT * FROM comments  WHERE id = 3"))
