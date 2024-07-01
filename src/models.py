import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()



class Follower(Base):
    __tablename__ = "follower"
    user_from_id= Column(Integer, ForeignKey('user.id'), nullable = False, primary_key = True)
    user_to_id = Column(Integer,ForeignKey('user.id'), nullable = False, primary_key = True)
    
    


class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    firstname = Column(String(250), nullable=False)
    lastname = Column(String(250), nullable=False)
    email = Column(String(250),unique=True, nullable = False)

    followed = relationship(
        'User',
        secondary= 'Follower',
        primaryjoin = (Follower.user_from_id == id),
        secondaryjoin = (Follower.user_to_id == id),
        backref="following",
        lazy='dynamic'
    )





class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    post = relationship(User)

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key = True)
    type= Column(Enum)
    url = Column(String)
    post_id = Column(Integer, ForeignKey('post.id'), nullable = False)
    media = relationship(Post)

class Comment(Base):
    __tablename__ = 'comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250))
    author_id = Column(Integer , ForeignKey('user.id'), nullable = False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable = False )
    #person_id = Column(Integer, ForeignKey('person.id'))
    #person = relationship(Person)
    comment_user = relationship(User)
    comment_post = relationship(Post)

    def to_dict(self):
        return {}
    

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e