from django.contrib.auth.models import User


def username_present(username):
    if User.objects.filter(username=username).exists():
        return True

    return False