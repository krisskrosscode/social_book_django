from django.contrib import admin
from .models import Book, CustomUser, Profile
import pprint
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.sessions.models import Session

from .forms import NewUserForm, CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    add_form = NewUserForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_author"
    )

    list_editable = (
        "is_staff",
        "is_author"
    )

    list_filter = (
        "email",
        "is_staff",
        "is_active",
        "is_author"
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_active", "groups", "user_permissions", "is_author")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                    "is_author"
                ),
            },
        ),
    )
    search_fields = ("email", "is_author")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Book)
admin.site.register(Profile)

class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
    
    _session_data.allow_tags = True
    list_display = ['session_key', '_session_data', 'expire_date']
    readonly_fields = ['_session_data']
    exclude = ['_session_data']


admin.site.register(Session, SessionAdmin)
