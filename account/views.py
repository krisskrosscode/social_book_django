from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import NewUserForm, UploadFileForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Book

# rest framework
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


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
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # print(uploaded_file.name, uploaded_file.size)
        fs = FileSystemStorage()
        file = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(file)
        context['url'] = url
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
    return render(request, 'upload_book.html', context)

@login_required(login_url='login')
def view_books(request):
    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Book(docfile=request.FILES['docfile'], author=request.POST['author'])
            newdoc.uploaded_by = request.user.username
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('view'))
    else:
        form = UploadFileForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Book.objects.all()

    # author_documents = Book.objects.filter(uploaded_by=request.user)

    # Extract users
    User = get_user_model()
    users = User.objects.all()

    # booknames = [d.docfile.name.split('/')[-1] for d in documents]
    # Render list page with the documents and the form
    return render(request, 'view_uploads.html', {'documents': documents, 'form': form, 'all_users': users})

@login_required(login_url='login')
def show_users(request):
    User = get_user_model()
    users = User.objects.all()
    staff = User.objects.filter(is_staff=True)
    info = {}
    info['fields'] = User._meta.get_fields()
    params = {'all_users': users, 'staff_users': staff, 'info': info['fields']}
    return render(request, 'show_users.html', params)
