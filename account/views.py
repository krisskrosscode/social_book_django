from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import NewUserForm, UploadFileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Book, CustomUser
from django.db.models import Count

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(
        request=request,
        template_name="register.html",
        context={"register_form": form},
    )


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(
        request=request, template_name="login.html", context={"login_form": form}
    )


# API rest_framework Code added by harshal

# @csrf_exempt
# @api_view(["POST"])
# @permission_classes((AllowAny,))
# def token_login_request(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")

#         if username is None or password is None:
#             return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)

#         user = authenticate(username=username, password=password)

#         if not user:
#             return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)

#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key}, status=HTTP_200_OK)


@login_required(login_url='login')
def index(request):
    return render(request, "index.html")


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("login")


def upload_book(request):
    User = get_user_model()
    # if request.user.is_authenticated:
    #     user_inst = request.user.username
    # initial_dict = {'author': user_inst}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        # print(form)
        # form.fields['author'] = User
        # print(form)
        print('post method')
        if form.is_valid():
            print('form valid')
            newdoc = Book(docfile=request.FILES['docfile'], author=request.user, pen_name=request.POST['pen_name'])
            newdoc.save()
            print(newdoc.author)

            # newdoc = form.save(commit=False)
            # newdoc.docfile = request.FILES['docfile']
            # newdoc.pen_name = request.POST['pen_name']
            # newdoc.save()
            # Redirect to the document list after POST
            # return JsonResponse({'status': 'success'})
            return HttpResponseRedirect(reverse('view'))
            # return render(request, 'view_uploads.html')
    else:
        print('empty form')
        form = UploadFileForm()  # A empty, unbound form
    return render(request, 'upload_book.html', {'form': form})
    # 1
    # if request.method == 'POST':
    #     uploaded_file = request.FILES['document']
    #     fs = FileSystemStorage()
    #     file = fs.save(uploaded_file.name, uploaded_file)
    #     url = fs.url(file)
    #     context['url'] = url

    # 2
    # context = {}
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         # file is saved
    #         form.save()
    #         return redirect('view_uploads')
    # else:
    #     form = UploadFileForm()
    #     context['upload_book_form'] = form

    # 3
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         handle_uploaded_file(request.FILES['file'])
    #         context = {'msg': '<span style="color: green;">File successfully uploaded</span>'}
    #         return render(request, "upload_book.html", context)
    # else:
    #     form = UploadFileForm()

    # context['form'] = form
    # authors = CustomUser.objects.filter(is_author=True)
    # context['authors'] = authors
    # return render(request, 'upload_book.html', context)

def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

@login_required(login_url='login')
def view_books(request):
    # Handle file upload
    User = get_user_model()
    context = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Book(docfile=request.FILES['docfile'], author=request.user, pen_name=request.POST['pen_name'])
            # newdoc.docfile = newdoc.docfile.split('/')[-1]
            newdoc.save()
            # handle_uploaded_file(request.FILES['docfile'])
            # context['msg'] = '<span style="color: green;">File successfully uploaded</span>'

            # Redirect to the document list after POST
            print(newdoc.author)
            return HttpResponseRedirect(reverse('view'))
    else:
        form = UploadFileForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Book.objects.all()

    # author_documents = Book.objects.filter(uploaded_by=request.user)
    context['documents'] = documents
    context['form'] = form
    # Extract users
    User = get_user_model()
    users = User.objects.all()
    context['all_users'] = users

    # Render list page with the documents and the form
    return render(request, 'view_uploads.html', context)

@login_required(login_url='login')
def show_users(request):
    User = get_user_model()
    users = User.objects.all()
    staff = User.objects.filter(is_staff=True)
    info = {}
    info['fields'] = User._meta.get_fields()
    params = {'all_users': users, 'staff_users': staff, 'info': info['fields']}
    return render(request, 'show_users.html', params)


@login_required(login_url='login')
def list_books(request):
    documents = Book.objects.all()
    return render(request, 'list_books.html', {'documents': documents})

@login_required(login_url='login')
def list_all_users(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, 'list_all_users.html', {'all_users': users})

@login_required(login_url='login')
def list_all_authors(request):
    User = get_user_model()
    authors = User.objects.filter(is_author=True)

    return render(request, 'list_all_authors.html', {'all_authors': authors})

@login_required(login_url='login')
def get_user_details(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    filtered_books = Book.objects.filter(author=user.id)
    total_books_uploaded = len(filtered_books)
    return render(request, 'user_details.html', {'user': user, 'books': filtered_books, 'upload_count': total_books_uploaded})


# @login_required(login_url='login')
# def get_books_by_author(request, pk):
#     authorname = get_object_or_404(CustomUser, pk=pk)
#     filtered_books = Book.objects.filter(uploaded_by=authorname)
#     return render(request, 'books_by_author.html', {'books': filtered_books})
