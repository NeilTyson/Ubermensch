from core.models import Profile


def get_user_type(request):
    if request.user.is_authenticated():
        user_type = Profile.objects.get(user=request.user)

        return {
            'user_type': user_type.user_type.upper()
        }
    else:
        return {

        }
