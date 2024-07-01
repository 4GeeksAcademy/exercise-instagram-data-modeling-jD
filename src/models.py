import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    user_name = Column(String(250), index=True)
    first_name = Column(String(250))
    last_name = Column(String(250))
    email = Column(String(250), nullable=False)
    
    followers = relationship(
        'Follower',
        foreign_keys='Follower.user_to_id',
        back_populates='user_to'
    )
    
    followings = relationship(
        'Follower',
        foreign_keys='Follower.user_from_id',
        back_populates='user_from'
    )

class Follower(Base):
    __tablename__ = "follower"
    id = Column(Integer, primary_key=True)
    user_from_id = Column(Integer, ForeignKey("user.id"))
    user_to_id = Column(Integer, ForeignKey("user.id"))

    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='followings')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='followers')
class Post(Base):
    __tablename__="post"
    id = Column(Integer, primary_key=True)
    user_id= Column(Integer,ForeignKey("User.id"))
    user= relationship(User)

class Comment(Base):
    __tablename__="comment"
    id = Column(Integer, primary_key=True)
    comment_text = Column(String(250))
    author_id = Column(Integer, ForeignKey("User.id"))
    post_id= Column (Integer, ForeignKey("Post.id"))
    user= relationship(User)
    post= relationship(Post)



class Media(Base):
    __tablename__= "media"
    id= Column(Integer, primary_key=True)
    type= Column(Enum("like","comment"),nullable=False)
    url= Column(String(250))
    post_id= Column(Integer, ForeignKey("Post.id"))



#         return {}

# class Media (Base):
#     __tablename__=""
#     id= Column(Integer, ForeignKey("Post.id"))
#     like_



# class User(Base):
#     __tablename__ = 'user'
#     # Here we define columns for the table person
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     user_name= Column(String(250), index=True),
#     first_name= Column(String(250), nullable=False),
#     last_name= Column(String(250), nullable=False),
#     email= Column(String(250), nullable=False),


# class Address(Base):
#     __tablename__ = 'address'
#     # Here we define columns for the table address.
#     # Notice that each column is also a normal Python instance attribute.
#     id = Column(Integer, primary_key=True)
#     street_name = Column(String(250))
#     street_number = Column(String(250))
#     post_code = Column(String(250), nullable=False)
#     person_id = Column(Integer, ForeignKey('person.id'))
#     person = relationship(Person)

#     def to_dict(self):
#         return {}

## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
