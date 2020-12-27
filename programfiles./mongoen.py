from mongoengine import *
import datetime

# While PyMongo is very easy to use and overall a great library, it’s probably a bit too low-level for many projects out there. Put another way, you’ll have to write a lot of your own code to consistently save, retrieve, and delete objects.

# One library that provides a higher abstraction on top of PyMongo is MongoEngine. MongoEngine is an object document mapper(ODM), which is roughly equivalent to a SQL-based object relational mapper(ORM). The abstraction provided by MongoEngine is class-based, so all of the models you create are classes.


connect('mongoengine_test', host="localhost", port=27017)


# To set up our document object, we need to define what data we want our document object to have. Similar to many other ORMs, we’ll do this by subclassing the Document class and providing the types of data we want:


class Post(Document):
    title = StringField(required=True, max_lenght=50)
    content = StringField(required=True)
    author = StringField(required=True)
    published_date = DateTimeField(default=datetime.datetime.now)


# One of the more difficult tasks with database models is validating data. How do you make sure that the data you’re saving conforms to some format you need? Just because a database is said to be schema-less doesn’t mean it is schema-free.


# http: // docs.mongoengine.org/guide/defining-documents.html  # field-arguments

# read the doc in the link above for more information.


# Saving Documents
# To save a document to our database, we’ll use the save() method. If the document already exists in the database, then all of the changes will be made on the atomic level to the existing document. If it doesn’t exist, however, then it will be created.


post_1 = Post(
    title="My first doc post",
    content="My first doc content",
    author="John Doe"
)

post_1.save()


# posts.find({'author', "John Doe"})
