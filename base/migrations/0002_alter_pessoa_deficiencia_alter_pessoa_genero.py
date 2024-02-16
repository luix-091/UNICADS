# Generated by Django 5.0.2 on 2024-02-15 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='deficiencia',
            field=models.CharField(choices=[('Física', 'Física'), ('Auditiva', 'Auditiva'), ('Visual', 'Visual'), ('Intelectual', 'Intelectual'), ('Psicossocial', 'Psicossocial')], default='Não informada', max_length=15),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Feminino')], default='Não informado', max_length=1),
        ),
    ]
