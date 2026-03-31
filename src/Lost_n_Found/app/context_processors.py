"""
app/context_processors.py
"""

from django.conf import settings


def app_version(request):
    return {
        "APP_FULL_VERSION": settings.APP_FULL_VERSION,
    }


def user_roles(request):
    user = request.user

    if not user.is_authenticated:
        return {
            "IS_CAMPUS_COMMUNITY_USER": False,
            "IS_SECURITY_OFFICE_STAFF": False,
        }

    return {
        "IS_CAMPUS_COMMUNITY_USER": user.groups.filter(name="Campus Community User").exists(),
        "IS_SECURITY_OFFICE_STAFF": user.groups.filter(name="Security Office Staff").exists(),
    }