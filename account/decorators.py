from .models import CustomUser, Profile
from django.contrib.auth import get_user_model


def add_profile_pic(funct):
    def wrapper(request, *args, **kwargs):
        User = get_user_model()
        profile_pic = Profile.objects.get(user=User.objects.get(id=request.user.id))
        profile_pic_object = Profile._meta.get_field('image')
        profile_pic_value = getattr(profile_pic, profile_pic_object.attname)
        
        print(profile_pic_object.get_default())
        if profile_pic_value == profile_pic_object.get_default():
            print("Please add your profile pic")

        else:
            print('Your profile is complete')

        return funct(request)

    return wrapper
