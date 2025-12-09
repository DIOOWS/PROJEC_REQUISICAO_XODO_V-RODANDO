# core/models_config.py
from django.db import models

class SystemConfig(models.Model):
    logo_url = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return "Configurações do Sistema"

    class Meta:
        verbose_name = "Configuração do Sistema"
        verbose_name_plural = "Configurações do Sistema"
