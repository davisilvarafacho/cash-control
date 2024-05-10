from django.contrib import admin
from .models import Configuracao


admin.site.index_title = "Painel de administração"
admin.site.site_title = "Logix"
admin.site.site_header = "LOGIX"

@admin.register(Configuracao)
class ConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('ativo', 'codigo', 'descricao', 'valor')
    list_filter = ('ativo', 'codigo', 'descricao')
    search_fields = ('codigo',)
    ordering = ('codigo',)
