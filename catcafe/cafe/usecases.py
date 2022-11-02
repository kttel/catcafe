from .models import Profile


def check_search_field(request):
    return request.GET.get("search-dish")


def profile_update(user, avatar, ship_address):
    Profile.objects.filter(user=user).update(image=avatar, ship_address=ship_address)