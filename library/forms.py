from django import forms
from .models import Book,BorrowRequest

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']
class BorrowRequestForm(forms.ModelForm):
    class Meta:
        model = BorrowRequest
        fields = ['id_proof']
