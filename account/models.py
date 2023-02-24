from django.db import models
# from django.core.validators import FileExtensionValidator
from django.forms import ValidationError
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here

class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=False, default='User')
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    # last_login = models.DateTimeField(verbose_name="last logged in", auto_now=True)
    is_admin = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_author = models.BooleanField(default=False)

    # date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    # to disable view and add you can do this
    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True

class Book(models.Model):
    def validate_file_extension(filename):
        if filename.file.content_type != 'application/pdf':
            raise ValidationError(u' ERROR : You can upload only a pdf file')

    docfile = models.FileField(
        upload_to='documents/%Y/%m/%d',
        default='SampleFilename',
        validators=[validate_file_extension],
        )
    publish_date = models.DateField(default=timezone.now)
    publish_time = models.TimeField(default=timezone.now)
    pen_name = models.CharField(max_length=100, default='None')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=get_user_model())
    # uploaded_by = models.CharField(max_length=100, default=get_user_model())

    REQUIRED_FIELDS = ["docfile", "pen_name"]