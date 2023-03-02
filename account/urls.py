from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

# cache 
from django.views.decorators.cache import cache_page

urlpatterns = [
    path("", views.register_request, name='register'),
    path("register/", views.register_request, name='register'),
    path("login/", views.login_request, name='login'),
    path("index/", views.index, name='index'),
    path("logout/", views.logout_request, name='logout'),
    path("upload_books/", views.upload_book, name='upload'),
    path("view_books/", views.view_books, name='view'),
    path('show_users/', views.show_users, name='show_users'),
    path('list_books/', view=views.list_books, name='list_books'),
    path('list_all_users/', views.list_all_users, name='list_all_users'),
    path('list_all_authors/', views.list_all_authors, name='list_all_authors'),
    path('user_details/<int:pk>/', views.get_user_details, name='user_details'),
    path('profile/', view=views.profile, name='profile'),
    path('sendemail/<int:pk>/<int:bid>/', view=views.sendemail, name='sendemail'),
    path('download-ready/', view=views.download_ready, name='download-ready'),
    path('testsession/', views.testsession)
    # path('api/login', view=views.token_login_request, name='token_login'),
    # path('auth/', obtain_auth_token),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
