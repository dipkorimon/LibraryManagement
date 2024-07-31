from django.shortcuts import render, redirect
from sqlalchemy.orm import sessionmaker
from .models import Book, Author, Purchase, User, Stock
from sqlalchemy import create_engine
from datetime import datetime
from django.http import JsonResponse

DATABASE_URL = 'mysql+pymysql://dipkorimon:password@127.0.01/mydb'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

def add_author_view(request):
  if request.method == 'POST':
    name = request.POST['name']
    bio = request.POST['bio']
    new_author = Author(name=name, bio=bio)
    session.add(new_author)
    session.commit()
    return redirect('add_author')
  return render(request, 'add_author.html')

def add_book_view(request):
  if request.method == 'POST':
    title = request.POST['title']
    author_id = request.POST['author_id']
    published_date = datetime.strptime(request.POST['published_date'], '%Y-%m-%d')
    new_book = Book(title=title, author_id=author_id, published_date=published_date)
    session.add(new_book)
    session.commit()
    return redirect('add_book')
  return render(request, 'add_book.html')

def books_with_authors_view(request):
  books_with_authors = session.query(Book.title, Author.name, Book.published_date).join(Author, Book.author_id == Author.id).all()
  books_with_authors_list = list(books_with_authors)
  return JsonResponse(books_with_authors_list, safe=False)

def purchases_view(request):
  purchases = session.query(Purchase.id, User.username, Book.title, Purchase.purchase_date).join(User, Purchase.user_id == User.id).join(Book, Purchase.book_id == Book.id).all()
  purchases_list = list(purchases)
  return JsonResponse(purchases_list, safe=False)

def stock_view(request):
  stock_details = session.query(Book.title, Stock.quantity).join(Stock, Book.id == Stock.book_id).all()
  stock_details_list = list(stock_details)
  return JsonResponse(stock_details_list, safe=False)
