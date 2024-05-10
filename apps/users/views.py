from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import AllowCreateWithoutAuth
from .serializers import (
    Usuario,
    UsuarioSerializer,
    RedefinirSenhaSerializer,
    AlterarSenhaSerializer,
)


class UsuarioViewSet(ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class AuthViewSet(ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowCreateWithoutAuth]

    serializer_classes = {
        "redefinir_senha": RedefinirSenhaSerializer,
        "alterar_senha": AlterarSenhaSerializer,
    }

    def redefinir_senha(self, request):
        return Response(status=status.HTTP_200_OK)

    def alterar_senha(self, request):
        return Response(status=status.HTTP_200_OK)
