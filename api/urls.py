from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import (
    token_obtain_pair as token_obtain,
    token_refresh,
    token_verify,
)

apps_urls = [path("api/v1/", include(app + ".urls")) for app in settings.LOGIX_APPS]

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/token/obtain/", token_obtain, name="token_obtain"),
    path("api/token/refresh/", token_refresh, name="token_refresh"),
    path("api/token/verify/", token_verify, name="token_verify"),

    *apps_urls,

    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
