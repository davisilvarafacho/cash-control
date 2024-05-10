from rest_framework import serializers
from .models import SaidaDinheiro, EntradaDinheiro, CategoriaGasto


class SaidaDinheiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaidaDinheiro
        fields = "__all__"
        depth = 1


class EntradaDinheiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = EntradaDinheiro
        fields = "__all__"
        depth = 1


class CategoriaGastoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaGasto
        fields = "__all__"
