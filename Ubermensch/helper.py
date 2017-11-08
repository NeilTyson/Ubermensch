from django.contrib.auth.models import User


# This file contains functions that you may call throughout the system
# Feel free to add functions here

# Makes sure that the username is unique
def is_unique(username):
    user = User.objects.get(username=username)

    return user is None
