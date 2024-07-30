from django.urls import path
from . import views

urlpatterns = [
  path('books_with_authors/', views.books_with_authors_view, name='books_with_authors'),
  path('purchases/', views.purchases_view, name='purchases'),
  path('stock/', views.stock_view, name='stock'),
  path('add_author/', views.add_author_view, name='add_author'),
  path('add_book/', views.add_book_view, name='add_book'),
]
