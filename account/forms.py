from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Book, CustomUser
from crispy_forms.helper import FormHelper

# Create your forms here.

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True

        for fieldname in ['username', 'email', 'password2']:
            self.fields[fieldname].help_text = None

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ("email",)

class UploadFileForm(forms.ModelForm):

    class Meta:
        model = Book
        fields = ('docfile', 'author')   # changed here from "__all__"

    docfile = forms.FileField(
        label='Select a file',
        help_text='.pdf'
    )
    author = forms.CharField(
        label='Author Name'
    )
