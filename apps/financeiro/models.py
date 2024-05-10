from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone as django_timezone

from apps.system.base.models import Base


class EntradaDinheiro(Base):
    ORIGENS = (
        ("SAL", "Salário"),
        ("DEC", "Décimo terceiro"),
        ("FER", "Férias"),
        ("PRO", "Projeto a parte"),
        ("MAN", "Manutenção"),
        ("OUT", "Outros"),
    )

    origem = models.CharField(
        _("tipo"),
        max_length=3,
        choices=ORIGENS,
        default="SAL",
    )

    valor = models.FloatField(
        _("valor"),
        help_text=_("Valor da entrada"),
        validators=[
            MinValueValidator(
                0.01, message=_("O valor da entrada deve ser maior que zero.")
            ),
        ],
    )

    data_entrada = models.DateField(
        _("data da entrada"),
        default=django_timezone.now,
    )

    def __str__(self):
        origem = None
        for valor_db, descricao in self.ORIGENS:
            if valor_db == self.origem:
                origem = descricao
                break

        return f'{origem} | {self.data_entrada.strftime("%m/%y")}'

    class Meta:
        db_table = "entrada_dinheiro"
        ordering = ["-id"]
        verbose_name = _("Entrada de dinheiro")
        verbose_name_plural = _("Entradas de dinheiro")


class SaidaDinheiro(Base):
    CLASSES = (
        ("LAZ", "Prazer"),
        ("DES", "Necessidade"),
        ("ECO", "Reserva de emergência"),
        ("INV", "Investimento finançeiro"),
        ("CRE", "Investimento pessoal"),
        ("IMP", "Imprevistos"),
        ("SON", "Sonho de consumo"),
        ("QUA", "Qualidade de vida"),
    )

    descricao = models.TextField(_("descrição"))

    valor_total = models.FloatField(
        _("valor"),
        help_text=_("Valor do pagamento"),
        validators=[
            MinValueValidator(
                0.01, message=_("O valor do pagamento deve ser maior que zero.")
            ),
        ],
    )

    categoria = models.CharField(_("Categoria"), choices=CLASSES, max_length=3, default="LAZ")

    entrada = models.ForeignKey(
        "EntradaDinheiro",
        verbose_name=_("entrada"),
        on_delete=models.CASCADE,
        related_name="saidas",
    )

    destino = models.ForeignKey(
        "DestinoGasto",
        verbose_name=_("destino"),
        on_delete=models.CASCADE,
        related_name="saidas",
    )

    parcela = models.PositiveIntegerField(_("parcela"), null=True, blank=True)

    total_parcelas = models.PositiveIntegerField(
        _("total de parcelas"), null=True, blank=True
    )

    data_gasto = models.DateField(_("data do gasto"), null=True, blank=True)

    paga = models.BooleanField(
        _("paga"),
        default=False,
    )

    saida = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name=_("saída"),
        blank=True,
        null=True,
    )

    parcial = models.BooleanField(
        _("parcial"),
        default=False,
        help_text=_(
            "Informa se a saída é uma parte de um pagamento com várias saídas, porque o dinheiro utilizado se originou de mais de uma entrada"
        ),
    )

    @property
    def valor_total_parcelas(self):
        return self.valor_total * self.total_parcelas

    def __str__(self):
        return self.descricao

    class Meta:
        db_table = "saida_dinheiro"
        ordering = ["-id"]
        verbose_name = _("Saída de dinheiro")
        verbose_name_plural = _("Gastos e despesas")


class DestinoGasto(Base):
    nome = models.CharField(_("nome"), max_length=50, help_text=_("Nome do destino"))

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "destino"
        ordering = ["-id"]
        verbose_name = _("Destino do gasto")
        verbose_name_plural = _("Destinos dos gastos")


class ItemListaDesejo(Base):
    TIPOS = (
        ("LIV", "Livro"),
        ("SON", "Sonho/Objetivo"),
        ("ROP", "Roupa"),
        ("TEN", "Tênis"),
        ("PER", "Perfume"),
        ("OUT", "Outros"),
    )
    
    nome = models.CharField(_("nome"), max_length=50, help_text=_("Nome"))

    tipo = models.CharField(
        _("tipo"),
        max_length=3,
        choices=TIPOS,
        default="LIV",
    )

    valor = models.FloatField(
        _("valor"),
        help_text=_("Valor do desejo"),
        validators=[
            MinValueValidator(
                0.01, message=_("O valor do desejo deve ser maior que zero.")
            ),
        ],
    )

    link = models.URLField(_("link"), blank=True)

    comprado = models.BooleanField(
        _("comprado"),
        default=False,
    )

    def __str__(self):
        return self.nome

    class Meta:
        db_table = "item_lista_desejo"
        ordering = ["-id"]
        verbose_name = _("Item da lista de desejos")
        verbose_name_plural = _("Lista de desejos")


@receiver(pre_save, sender=SaidaDinheiro)
def set_gasto_date(sender, instance, **kwargs):
    if not instance.data_gasto:
        instance.data_gasto = instance.entrada.data_entrada


@receiver(post_save, sender=EntradaDinheiro)
def set_gasto_date(sender, instance, **kwargs):
    for saida in instance.saidas.all():
        saida.data_gasto = instance.data_entrada
        saida.save()
