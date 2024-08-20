import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()






Followers = Table(
    'followers',
    Base.metadata,
    Column('follower_id', Integer, ForeignKey('user.ID'), primary_key=True),
    Column('following_id', Integer, ForeignKey('user.ID'), primary_key=True)
)

class User(Base):
    __tablename__='user'
    ID= Column(Integer, primary_key=True)
    user_name = Column(String(250),nullable=False)
    first_name = Column(String(250),nullable=False)
    last_name = Column(String(250),nullable=False)
    email = Column(String(250),nullable=False)
    post= relationship('Post', backref='user', lazy=True)
    comment= relationship('Comment', backref='user', lazy=True)
    followed = relationship(
        'User',
        secondary=Followers,
        primaryjoin=(Followers.c.following_id==id), # Seguidos
        secondaryjoin=(Followers.c.follower_id==id), # Yo sigo
        backref='following',
        lazy='True'
    )

class Media(Base):
    __tablename__= 'media'
    ID= Column(Integer, primary_key=True)
    type = Column(Enum('photo','video','reel'),nullable=False)
    url = Column(String(250),nullable=False)
    post_id = Column(Integer, ForeignKey('post.ID'))
    
class Post(Base):
    __tablename__='post'
    ID= Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.ID'))
    comment= relationship('Comment',backref='post', lazy=True)
    media= relationship('Media',backref='post', lazy=True)

class Comment(Base):
    __tablename__='comment'
    ID= Column(Integer, primary_key=True)
    comment_text = Column(String(250),nullable=False)
    author_id = Column(Integer, ForeignKey('user.ID'))
    post_id = Column(Integer, ForeignKey('post.ID'))


## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e
