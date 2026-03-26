from django.conf import settings


def app_version(request):
    return {
        "APP_FULL_VERSION": settings.APP_FULL_VERSION,
    }