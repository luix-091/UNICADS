from django.db import models

# Create your models here.

class Endereco(models.Model):
    logradouro = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
    regiao = models.CharField(max_length=100)

class Pessoa(models.Model):
    nome =  models.CharField(max_length=200)
    cpf = models.CharField(max_length=20)
    data_nasc = models.DateField()
    genero = models.CharField(max_length=100)
    enderecos = models.ManyToManyField(Endereco)
    deficiencia = models.CharField(max_length=300)
    necessidades = models.CharField(max_length=300)