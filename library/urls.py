from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-books/', views.my_books_view, name='my_books'),
    path('issue/<int:book_id>/', views.issue_book, name='issue_book'),
    path('return/<int:book_id>/', views.return_book, name='return_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
    path('add-book/', views.add_book, name='add_book'),
    path('dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('borrow/<int:book_id>/', views.borrow_request_view, name='borrow_request'),
    path('approve/<int:request_id>/', views.approve_request, name='approve_request'),


    
]
