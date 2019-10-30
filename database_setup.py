import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    author = Column(String(250), nullable=False)
    # bookformat = Column(String(250), nullable=True)

    @property
    def serialize(self):
        return{
            'title': self.title,
            'author': self.author,
            'id': self.id,
        }

# engine = create_engine('sqlite:///books-collection.db')

# Base.metadata.create_all(engine)