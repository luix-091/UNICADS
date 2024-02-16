from django.db import models

# Create your models here.

class Endereco(models.Model):
    logradouro = models.CharField(max_length=200)
    bairro = models.CharField(max_length=100)
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