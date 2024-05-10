from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh, token_verify
from .views import UsuarioViewSet, AuthViewSet

router = DefaultRouter()
router.register("usuarios", UsuarioViewSet, "usuarios")
router.register("auth", AuthViewSet, "auth")

urlpatterns = [
    path("", include(router.urls)),
    path("api/token/", token_obtain_pair, name="token_obtain_pair"),
    path("api/token/refresh/", token_refresh, name="token_refresh"),
    path("api/token/verify/", token_verify, name="token_verify"),
]
