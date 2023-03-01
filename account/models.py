from django.db import models
# from django.core.validators import FileExtensionValidator
from django.forms import ValidationError
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from PIL import Image
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
    # profile_picture = models.ImageField(upload_to='profile_pictures/{CustomUser.id}/', default='profile_pictures/default.png')

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

class Profile(models.Model):
    def get_user_id(self):
        return self.id
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pictures/default.png', upload_to='profile_pictures/users/', max_length=500)

    def __str__(self) -> str:
        return self.user.username
    
    
    #  Override the save method of the model

    # def save(self, *args, **kwargs):
    #     super(Profile, self).save(*args, **kwargs)

    #     img = Image.open(self.image.path)  # Open image

    #     # resize image
    #     if img.height > 300 or img.width > 300:
    #         output_size = (50, 50)
    #         img.thumbnail(output_size)  # Resize image
    #         img.save(self.image.path)  # Save it again and override the larger image
    

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
    
    REQUIRED_FIELDS = ["docfile", "pen_name"]

    def __str__(self):
        return self.docfile.name.split('/')[-1]
