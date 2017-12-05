from core.models import Profile


def profile_processor(request):
    profile = Profile.objects.get(user=request.user)
    return {
        'profile': profile
    }