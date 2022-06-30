import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from peewee import *

DATABASE = SqliteDatabase('database.db')

# Models go here...

# User Model
class User(UserMixin, Model):
    name = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)
    
    # Constructor Class
    @classmethod
    def create_user(cls, name, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    name=name,
                    email=email,
                    password=generate_password_hash(password)
                    )
        except IntegrityError:
            raise ValueError("User already exists")


# Run Database     
def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True) # put each model in array
    DATABASE.close()