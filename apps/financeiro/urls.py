from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import SaidaDinheiroViewSet, EntradaDinheiroViewSet

router = DefaultRouter()
# router.register('despesas', SaidaDinheiroViewSet, basename='despesas')
# router.register('entradas', EntradaDinheiroViewSet, basename='entradas')

urlpatterns = [
    path('', include(router.urls)),
]
