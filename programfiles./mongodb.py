from pymongo import MongoClient


# creating connections
client = MongoClient('localhost', 27017)


# accessing database to use
db = client['pymongo_test']

# It doesn’t actually matter if your specified database has been created yet. By specifying this database name and saving data to it, you create the database automatically.


# Inserting Documents
# Storing data in your database is as easy as calling just two lines of code. The first line specifies which collection you’ll be using(posts in the example below). In MongoDB terminology, a collection is a group of documents that are stored together within the database. Collections and documents are akin to SQL tables and rows, respectively. Retrieving a collection is as easy as getting a database.

# The second line is where you actually insert the data in to the collection using the insert_one() method:


posts = db.posts

post_data = {
    'title': 'my first post',
    'content': 'my first post content',
    'author': 'James'
}

# result = posts.insert_one(post_data)
# print(result.inserted_id)

post_1 = {
    'title': 'Python and MongoDB',
    'content': 'PyMongo is fun, you guys',
    'author': 'Scott'
}
post_2 = {
    'title': 'Virtual Environments',
    'content': 'Use virtual environments, you guys',
    'author': 'Scott'
}
post_3 = {
    'title': 'Learning Python',
    'content': 'Learn Python, it is easy',
    'author': 'Bill'
}


# results = posts.insert_many([post_1, post_2, post_3])
# print(results.inserted_ids)


# Retrieve data

post = posts.find_one({'author': 'James'})
print(post)
print()

many_posts = posts.find({'author': 'Scott'})

for post in many_posts:
    print(post)
    print()