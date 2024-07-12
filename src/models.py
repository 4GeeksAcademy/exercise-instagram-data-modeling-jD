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
    user_from = relationship("User", foreign_keys=[user_from_id], back_populates="following")
    user_to = relationship("User", foreign_keys=[user_to_id], back_populates="followers")
    


class User(Base):
    __tablename__ = 'user'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(250), unique=True, nullable=False)
    firstname = Column(String(250))
    lastname = Column(String(250))
    email = Column(String(250),unique=True, nullable = False)
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="author")
    followers = relationship("Follower", foreign_keys="Follower.user_to_id", back_populates="user_to")
    following = relationship("Follower", foreign_keys="Follower.user_from_id", back_populates="user_from")




class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable = False)
    post = relationship(User)

class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key = True)
    type= Column(Enum("image","video","audio"))
    url = Column(String,nullable=False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable = False)
    post = relationship("Post", back_populates="media")

class Comment(Base):
    __tablename__ = 'comment'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250), nullable=False)
    author_id = Column(Integer , ForeignKey('user.id'), nullable = False)
    post_id = Column(Integer, ForeignKey('post.id'), nullable = False )
    #person_id = Column(Integer, ForeignKey('person.id'))
    #person = relationship(Person)
    author = relationship("User", back_populates="comment")
    post = relationship("Post", back_populates="comment")
    def to_dict(self):
        return {}
    

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e