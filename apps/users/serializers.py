from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # coloque aqui os dados que deseja retornar no token
    
        return token


class RedefinirSenhaSerializer(serializers.Serializer):
    email = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field="email"
    )
    senha = serializers.CharField(max_length=128)
    confirmar_senha = serializers.CharField(max_length=128)
    nova_senha = serializers.CharField(max_length=128)


class AlterarSenhaSerializer(serializers.Serializer):
    email = serializers.SlugRelatedField(
        queryset=Usuario.objects.all(), slug_field="email"
    )
    nova_senha = serializers.CharField(max_length=128)
