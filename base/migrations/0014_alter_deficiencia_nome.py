# Generated by Django 5.0.2 on 2024-03-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_alter_deficiencia_nome'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deficiencia',
            name='nome',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
