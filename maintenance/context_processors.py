from core.models import Profile


def profile_processor(request):
    return Profile.objects.get(user=request.user)