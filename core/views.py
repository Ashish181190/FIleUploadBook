from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .forms import BookForm
from .models import Book

# Create your views here.

class Home(TemplateView):
    """ To show home page of our site """
    template_name = 'home.html'

def upload(request):
    """ Upload all details of Book and add book details in data """
    # return render(request, 'upload.html')
    # print(request.FILES)
    if request.FILES == {}:
        return render(request, 'simple_upload.html')
    else:
        request.method == "POST" and request.FILES['myfile']
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        messages.success(request, 'Your Book was added successfully!')
        return render(request, 'simple_upload.html', {'uploaded_file_url': uploaded_file_url})

def book_list(request):
    """ to show all books detials """
    books = Book.objects.all
    return render(request, 'book_list.html', {'books': books})

def upload_book(request):
    """ Upload all details of Book and add book details in data """
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Book was added successfully!')
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {'form': form})

def delete_book(request, pk):
    " Delete Book from data "
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')

def edit(request, pk):
    """ To Edit a book details """
    obj = get_object_or_404(Book, id=pk)
    form = BookForm(request.POST or None, request.FILES or None, instance=obj)

    if form.is_valid():
        form.save()
        messages.success(request, 'Your password was updated successfully!')
        return redirect('book_list')
    return render(request, 'upload_book.html', {'form': form})

def delete_all_book(request):
    """ To delete all books """
    all_books = Book.objects.all()
    for book in all_books:
        book.pdf.delete()
        book.cover.delete()
        book.delete()
    return redirect('book_list')



# Class Based Views
class BookListView(ListView):
    """ to get all book details """
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    """ To upload a new book """
    model = Book
    form_class = BookForm
    # success_url = 'class_book_list'
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
