from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.register_request, name='register'),
    path("register/", views.register_request, name='register'),
    path("login/", views.login_request, name='login'),
    path("index/", views.index, name='index'),
    path("logout/", views.logout_request, name='logout'),
    path("upload_books/", views.upload_book, name='upload'),
    path("view_books/", views.view_books, name='view'),
    path('show_users/', views.show_users, name='show_users'),
    # path('api/login', view=views.token_login_request, name='token_login'),
    # path('auth/', obtain_auth_token),
]
