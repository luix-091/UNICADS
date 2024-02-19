from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

# Create your models here.

class Endereco(models.Model):

    BAIRROS_CHOICES = [
        ('Água Verde', 'Água Verde'),
        ('Águas Claras', 'Águas Claras'),
        ('Amizade', 'Amizade'),
        ('Barra do Rio Cerro', 'Barra do Rio Cerro'),
        ('Barra do Rio Molha', 'Barra do Rio Molha'),
        ('Boa Vista', 'Boa Vista'),
        ('Braço Ribeirão Cavalo', 'Braço Ribeirão Cavalo'),
        ('Centenário', 'Centenário'),
        ('Centro', 'Centro'),
        ('Chico de Paulo', 'Chico de Paulo'),
        ('Czerniewicz', 'Czerniewicz'),
        ('Estrada Nova', 'Estrada Nova'),
        ('Ilha da Figueira', 'Ilha da Figueira'),
        ('Jaraguá 84', 'Jaraguá 84'),
        ('Jaraguá 99', 'Jaraguá 99'),
        ('Jaraguá Esquerdo', 'Jaraguá Esquerdo'),
        ('João Pessoa', 'João Pessoa'),
        ('Nereu Ramos', 'Nereu Ramos'),
        ('Nova Brasília', 'Nova Brasília'),
        ('Parque Malwee', 'Parque Malwee'),
        ('Rau', 'Rau'),
        ('Ribeirão Cavalo', 'Ribeirão Cavalo'),
        ('Rio Cerro I', 'Rio Cerro I'),
        ('Rio Cerro II', 'Rio Cerro II'),
        ('Rio da Luz', 'Rio da Luz'),
        ('Rio Molha', 'Rio Molha'),
        ('Santa Luzia', 'Santa Luzia'),
        ('Santo Antônio', 'Santo Antônio'),
        ('São Luís', 'São Luís'),
        ('Tifa Martins', 'Tifa Martins'),
        ('Tifa Monos', 'Tifa Monos'),
        ('Três Rios do Norte', 'Três Rios do Norte'),
        ('Três Rios do Sul', 'Três Rios do Sul'),
        ('Vieira', 'Vieira'),
        ('Vila Baependi', 'Vila Baependi'),
        ('Vila Lalau', 'Vila Lalau'),
        ('Vila Lenzi', 'Vila Lenzi'),
        ('Vila Nova', 'Vila Nova'),
    ]

    logradouro = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100,
                                choices=BAIRROS_CHOICES, default='Não Informado')
    regiao = models.CharField(max_length=100)

    def __str__(self):
        return self.logradouro

class Pessoa(models.Model):
    nome =  models.CharField(max_length=200, blank=False, null=False)
    cpf = models.CharField(max_length=20)
    data_nasc = models.DateField()
    genero = models.CharField(
        max_length=1,
        choices=[
        ('M', 'Masculino'),
        ('F', 'Feminino'),
    ],
        default='Não informado',
    )
    enderecos = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, default=None)
    deficiencia = models.CharField(max_length=15,
                                   choices=[
                                        ('Física', 'Física'),
                                        ('Auditiva', 'Auditiva'),
                                        ('Visual', 'Visual'),
                                        ('Intelectual', 'Intelectual'),
                                        ('Psicossocial', 'Psicossocial'),
                                   ],
                                   default='Não informada')
    detalhes = models.CharField(max_length=300, default='Não Fornecido')
    necessidades = models.CharField(max_length=300, default='Não Fornecida')

    def __str__(self):
        return self.nome