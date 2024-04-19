from django.db import models
from django.contrib.auth.models import User
from medico.models import DadosMedico, DatasAbertas
from datetime import datetime


# Create your models here.
class Consulta(models.Model):
    status_choices = [
        ("A", "Agendado"),
        ("C", "Cancelada"),
        ("F", "Finalizada"),
        ("I", "Iniciada"),
    ]
    paciente = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name="paciente"
    )
    data_aberta = models.ForeignKey(DatasAbertas, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=1, choices=status_choices, default="A")
    link = models.URLField(null=True, blank=True)
    
    @property
    def medico(self):
        return DadosMedico.objects.get(user=self.data_aberta.user)
    
    @property
    def days_left(self):
        return (self.data_aberta.data - datetime.now()).days
    
    def __str__(self):
        return self.paciente.username
