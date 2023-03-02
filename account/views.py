from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import NewUserForm, UploadFileForm, ProfileUpdateForm, CustomUserChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
import os
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Book, CustomUser, Profile
from django.db.models import Count
from django.conf import settings
from datetime import datetime

# send emails
from django.core import mail
from django.core.mail import send_mail

# custom wrapper
from .decorators import add_profile_pic


# caching 
from django.views.decorators.cache import cache_page


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
                request.session['username'] = username  # create cache
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


@login_required(login_url="login")
def index(request):
    visits = int(request.COOKIES.get('visits', '0'))

    context = {
        'visits': visits
    }
    response = render(request, template_name="index.html", context=context)

    if 'last_visit' in request.COOKIES:
        last_visit = request.COOKIES['last_visit']
        # the cookie is a string - convert back to a datetime type
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        curr_time = datetime.now()
        if (curr_time - last_visit_time).days > 0:
            # if at least one day has gone by then inc the visit count.
            response.set_cookie('visits', visits + 1)
            response.set_cookie('last_visit', datetime.now())
        else:
            response.set_cookie('last_visit', datetime.now())
    return render(request, "index.html", context)


def logout_request(request):

    try:
        del request.session['username']
        logout(request)
        messages.info(request, "You have successfully logged out.")

    except Exception as e:
        return redirect("login")

    return redirect("login")


def upload_book(request):
    User = get_user_model()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        # print(form)
        # form.fields['author'] = User
        if form.is_valid():
            # print('form valid')
            newdoc = Book(
                docfile=request.FILES["docfile"],
                author=request.user,
                pen_name=request.POST["pen_name"],
            )
            newdoc.save()
            print(newdoc.docfile.__str__)

            # newdoc = form.save(commit=False)
            # newdoc.docfile = request.FILES['docfile']
            # newdoc.pen_name = request.POST['pen_name']
            # newdoc.save()
            # Redirect to the document list after POST
            # return JsonResponse({'status': 'success'})
            return HttpResponseRedirect(reverse("view"))
            # return render(request, 'view_uploads.html')
    else:
        # print('empty form')
        form = UploadFileForm()  # A empty, unbound form
    return render(request, "upload_book.html", {"form": form})

def handle_uploaded_file(f):
    with open(f.name, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


@login_required(login_url="login")
def view_books(request):
    # Handle file upload
    User = get_user_model()
    context = {}
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Book(
                docfile=request.FILES["docfile"],
                author=request.user,
                pen_name=request.POST["pen_name"],
            )
            # newdoc.docfile = newdoc.docfile.split('/')[-1]
            newdoc.save()
            # handle_uploaded_file(request.FILES['docfile'])
            # context['msg'] = '<span style="color: green;">File successfully uploaded</span>'

            # Redirect to the document list after POST
            print(newdoc.author)
            return HttpResponseRedirect(reverse("view"))
    else:
        form = UploadFileForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Book.objects.all()

    # author_documents = Book.objects.filter(uploaded_by=request.user)
    context["documents"] = documents
    context["form"] = form
    # Extract users
    User = get_user_model()
    users = User.objects.all()
    context["all_users"] = users

    # Render list page with the documents and the form
    return render(request, "view_uploads.html", context)


@login_required(login_url="login")
def show_users(request):
    User = get_user_model()
    users = User.objects.all()
    staff = User.objects.filter(is_staff=True)
    info = {}
    info["fields"] = User._meta.get_fields()
    params = {"all_users": users, "staff_users": staff, "info": info["fields"]}
    return render(request, "show_users.html", params)

@login_required(login_url="login")
@cache_page(30)
def list_books(request):
    documents = Book.objects.all()
    return render(request, "list_books.html", {"documents": documents})


@login_required(login_url="login")
@add_profile_pic
def list_all_users(request):
    User = get_user_model()
    users = User.objects.all()
    documents = Book.objects.all()
    return render(request, "list_all_users.html", {"all_users": users, 'documents':documents})


@login_required(login_url="login")
@add_profile_pic
def list_all_authors(request):
    User = get_user_model()
    authors = User.objects.filter(is_author=True)

    return render(request, "list_all_authors.html", {"all_authors": authors})


@login_required(login_url="login")
def get_user_details(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    logged_in_user = request.user
    filtered_books = Book.objects.filter(author=user.id)
    total_books_uploaded = len(filtered_books)
    return render(
        request,
        "user_details.html",
        {"user": user, "books": filtered_books, "upload_count": total_books_uploaded, 'logged_in_user': logged_in_user},
    )




# @login_required(login_url='login')
# def get_books_by_author(request, pk):
#     authorname = get_object_or_404(CustomUser, pk=pk)
#     filtered_books = Book.objects.filter(uploaded_by=authorname)
#     return render(request, 'books_by_author.html', {'books': filtered_books})


@login_required(login_url="login")
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        u_form = CustomUserChangeForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            # user = CustomUser.objects.get(username=request.user)
            # profile = Profile(user=user)
            # profile.save()
            messages.success(request, "Your account has been updated!")
            return redirect("profile")  # Redirect back to profile page

    else:
        u_form = CustomUserChangeForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {"u_form": u_form, "p_form": p_form}

    return render(request, "profile.html", context)


@login_required(login_url="login")
def sendemail(request, pk, bid):
    # user = get_object_or_404(CustomUser, pk=pk)

    user = CustomUser.objects.get(id=pk)
    book = Book.objects.get(id=bid)
    # from_email = settings.EMAIL_HOST_USER
    # connection = mail.get_connection()
    # connection.open()

    # print('send email function activated')
    email_content = f"Thank you {user}. We are happy to help you find the book of your dreams ~ {book.author} (Author of the book {book} you have downloaded)"

    # connection.send_messages([email_content])
    # connection.close()
    # CustomUser.objects.filter(id=pk).values('email')[0]['email']
    send_mail(
        f"Thank You {user} for choosing us as your go to book provider",
        email_content,
        "harshalparteke@gmail.com",
        [user.email],
        html_message=email_content,
        fail_silently=False,
    )
    return HttpResponseRedirect(reverse("download-ready"))
    # return render(request, 'sendemail.html', {'user': user})

@login_required(login_url="login")
def download_ready(request):
    return render(request, 'download-ready.html')


def testsession(request):
    if request.session.get('test', False):
        print(request.session['test'])
    
    # request.session.set_expiry(1)
    request.session['test'] = 'testing'
    request.session['test2'] = 'testing2'
    return render(request, 'testsession.html')
