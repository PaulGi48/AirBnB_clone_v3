#!/usr/bin/python3
'''
    Implementation of the User class which inherits from BaseModel
'''
from os import getenv
from hashlib import md5
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    '''
        Definition of the User class
    '''
    __tablename__ = "users"

    def __init__(self, **kwargs):
        """ Constructor """
        super().__init__(**kwargs)
        self.password = self.set_password(kwargs.get("password", ""))

    def set_password(self, plaintext):
        """ Sets password property to it's md5 value """
        return md5(plaintext.encode()).hexdigest()

    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        password = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
    else:
        email = ""
        password = self.set_password(kwargs.get("password", ""))
        first_name = ""
        last_name = ""
