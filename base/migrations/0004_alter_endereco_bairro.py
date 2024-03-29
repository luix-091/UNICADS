# Generated by Django 5.0.2 on 2024-02-16 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_pessoa_detalhes_alter_pessoa_necessidades'),
    ]

    operations = [
        migrations.AlterField(
            model_name='endereco',
            name='bairro',
            field=models.CharField(choices=[('Água Verde', 'Água Verde'), ('Águas Claras', 'Águas Claras'), ('Amizade', 'Amizade'), ('Barra do Rio Cerro', 'Barra do Rio Cerro'), ('Barra do Rio Molha', 'Barra do Rio Molha'), ('Boa Vista', 'Boa Vista'), ('Braço Ribeirão Cavalo', 'Braço Ribeirão Cavalo'), ('Centenário', 'Centenário'), ('Centro', 'Centro'), ('Chico de Paulo', 'Chico de Paulo'), ('Czerniewicz', 'Czerniewicz'), ('Estrada Nova', 'Estrada Nova'), ('Ilha da Figueira', 'Ilha da Figueira'), ('Jaraguá 84', 'Jaraguá 84'), ('Jaraguá 99', 'Jaraguá 99'), ('Jaraguá Esquerdo', 'Jaraguá Esquerdo'), ('João Pessoa', 'João Pessoa'), ('Nereu Ramos', 'Nereu Ramos'), ('Nova Brasília', 'Nova Brasília'), ('Parque Malwee', 'Parque Malwee'), ('Rau', 'Rau'), ('Ribeirão Cavalo', 'Ribeirão Cavalo'), ('Rio Cerro I', 'Rio Cerro I'), ('Rio Cerro II', 'Rio Cerro II'), ('Rio da Luz', 'Rio da Luz'), ('Rio Molha', 'Rio Molha'), ('Santa Luzia(núcleo urbano isolado)', 'Santa Luzia(núcleo urbano isolado)'), ('Santo Antônio', 'Santo Antônio'), ('São Luís', 'São Luís'), ('Tifa Martins', 'Tifa Martins'), ('Tifa Monos', 'Tifa Monos'), ('Três Rios do Norte', 'Três Rios do Norte'), ('Três Rios do Sul', 'Três Rios do Sul'), ('Vieira', 'Vieira'), ('Vila Baependi', 'Vila Baependi'), ('Vila Lalau', 'Vila Lalau'), ('Vila Lenzi', 'Vila Lenzi'), ('Vila Nova', 'Vila Nova')], default='Não Informado', max_length=100),
        ),
    ]
