from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)
    icone = models.ImageField(upload_to="icones", null=True, blank=True)

    def __str__(self):
        return self.especialidade

class DadosMedico(models.Model):
    crm = models.CharField(max_length=30, null=False, blank=False, unique=True)
    nome = models.CharField(max_length=100, null=False, blank=False)
    cep = models.CharField(max_length=15)
    rua = models.CharField(max_length=100)
    bairro = models.CharField(max_length=100)
    numero = models.IntegerField()
    rg = models.ImageField(upload_to="rgs")
    cedula_identidade_medica = models.ImageField(upload_to='cim')
    foto = models.ImageField(upload_to="fotos_perfil")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    descricao = models.TextField(null=True, blank=True)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING, null=True, blank=True)
    valor_consulta = models.FloatField(default=100)

    def __str__(self):
        return self.user.username
    
class DatasAbertas(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    data = models.DateTimeField()
    agendado = models.BooleanField(default=False)

    def __str__(self):
        return str(self.data)