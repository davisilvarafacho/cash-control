from datetime import timedelta, date

from django.db.models import Sum
from django.db.models.functions import TruncDay

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import (
    SaidaDinheiro,
    SaidaDinheiroSerializer,
    EntradaDinheiro,
    EntradaDinheiroSerializer,
)


class EntradaDinheiroViewSet(ReadOnlyModelViewSet):
    queryset = EntradaDinheiro.objects.all()
    serializer_class = EntradaDinheiroSerializer

    @action(methods=["get"], detail=True)
    def gastos(self, request, pk, *args, **kwargs):
        entrada = self.get_object()
        gastos = entrada.saidas.all()

        page = self.paginate_queryset(self.filter_queryset(gastos))
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class SaidaDinheiroViewSet(ReadOnlyModelViewSet):
    queryset = SaidaDinheiro.objects.all()
    serializer_class = SaidaDinheiroSerializer
    filterset_fields = {
        "data_gasto": ["month"],
    }

    @action(methods=["get"], detail=False)
    def fixas(self, request):
        queryset = self.filter_queryset(self.get_queryset()).filter(fixa=True)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(methods=["get"], detail=False)
    def total_gasto_por_dia(self, request):
        # Obtenha o mês a partir da query string
        filtro_data_gasto = request.query_params.get("data_gasto__month")
        if not filtro_data_gasto:
            raise ValidationError({"data_gasto__month": "Essa query é obrigatória."})

        # Obtenha o primeiro e último dia do mês atual
        primeiro_dia = date.today().replace(day=1, month=int(filtro_data_gasto))
        ultimo_dia = (primeiro_dia + timedelta(days=32)).replace(day=1) - timedelta(
            days=1
        )

        # Crie uma lista de todos os dias do mês
        todos_dias = [
            primeiro_dia + timedelta(days=i)
            for i in range((ultimo_dia - primeiro_dia).days + 1)
        ]

        # Obtenha os totais de gastos por dia
        queryset = self.filter_queryset(self.get_queryset())
        gastos = list(
            queryset.annotate(data=TruncDay("data_gasto"))
            .values("data")
            .annotate(total=Sum("valor_total"))
            .order_by("data")
        )

        # Combine a lista de todos os dias com os totais de gastos
        resultados = []
        for dia in todos_dias:
            for gasto in gastos:
                if gasto["data"] == dia:
                    resultados.append(gasto)
                    break
            else:
                resultados.append({"data": dia, "total": 0})

        return Response({"resultados": resultados})

    @action(methods=["get"], detail=False)
    def total_gasto_por_categoria(self, request):
        # Obtenha o mês a partir da query string
        filtro_data_gasto = request.query_params.get("data_gasto__month")
        if not filtro_data_gasto:
            raise ValidationError({"data_gasto__month": "Essa query é obrigatória."})

        # Obtenha o primeiro e último dia do mês atual
        primeiro_dia = date.today().replace(day=1, month=int(filtro_data_gasto))
        ultimo_dia = (primeiro_dia + timedelta(days=32)).replace(day=1) - timedelta(
            days=1
        )

        # Obtenha os totais de gastos por categoria e também a porcentagem
        queryset = self.filter_queryset(self.get_queryset())
        gastos = list(
            queryset.filter(data_gasto__range=[primeiro_dia, ultimo_dia])
            .values("categoria__nome")
            .annotate(total=Sum("valor_total"))
            .order_by("categoria")
        )

        return Response({"resultados": gastos})

    @action(methods=["get"], detail=False)
    def kpis(self, request):
        # Obtenha o mês a partir da query string
        filtro_data_gasto = request.query_params.get("data_gasto__month")
        if not filtro_data_gasto:
            raise ValidationError({"data_gasto__month": "Essa query é obrigatória."})

        # Obtenha o primeiro e último dia do mês atual
        primeiro_dia = date.today().replace(day=1, month=int(filtro_data_gasto))
        ultimo_dia = (primeiro_dia + timedelta(days=32)).replace(day=1) - timedelta(
            days=1
        )

        # Obtenha os totais de gastos por categoria e também a porcentagem
        queryset = self.filter_queryset(self.get_queryset())
        gastos = list(
            queryset.filter(data_gasto__range=[primeiro_dia, ultimo_dia])
            .values("origem")
            .annotate(total=Sum("valor_total"))
            .order_by("origem")
        )

        return Response({"resultados": gastos})
