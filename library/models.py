from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = 'mysql+pymysql://dipkorimon:password@127.0.01/mydb'

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True)
  username = Column(String(100), nullable=False)
  email = Column(String(100), nullable=False, unique=True)
  password = Column(String(100), nullable=False)

  purchases = relationship('Purchase', back_populates='user')

  def __repr__(self):
    return f"<User(username='{self.username}', email='{self.email}')>"

class Author(Base):
  __tablename__ = 'authors'
  id = Column(Integer, primary_key=True)
  name = Column(String(100), nullable=False)
  bio = Column(String(255))

  books = relationship('Book', back_populates='author')

  def __repr__(self):
    return f"<Author(name='{self.name}')>"

class Book(Base):
  __tablename__ = 'books'
  id = Column(Integer, primary_key=True)
  title = Column(String(200), nullable=False)
  author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)
  published_date = Column(Date, nullable=False)

  author = relationship('Author', back_populates='books')
  purchases = relationship('Purchase', back_populates='book')
  stock = relationship('Stock', uselist=False, back_populates='book')

  def __repr__(self):
    return f"<Book(title='{self.title}', author='{self.author.name}')>"

class Purchase(Base):
  __tablename__ = 'purchases'
  id = Column(Integer, primary_key=True)
  user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
  book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
  purchase_date = Column(Date, nullable=False)

  user = relationship('User', back_populates='purchases')
  book = relationship('Book', back_populates='purchases')

  def __repr__(self):
    return f"<Purchase(user='{self.user.username}', book='{self.book.title}', date='{self.purchase_date}')>"

class Stock(Base):
  __tablename__ = 'stocks'
  id = Column(Integer, primary_key=True)
  book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
  quantity = Column(Integer, nullable=False)

  book = relationship('Book', back_populates='stock')

  def __repr__(self):
    return f"<Stock(book='{self.book.title}', quantity='{self.quantity}')>"

Base.metadata.create_all(engine)
