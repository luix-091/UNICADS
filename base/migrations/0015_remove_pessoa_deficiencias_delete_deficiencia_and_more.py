# Generated by Django 5.0.2 on 2024-03-08 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_alter_deficiencia_nome'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoa',
            name='deficiencias',
        ),
        migrations.DeleteModel(
            name='Deficiencia',
        ),
        migrations.AddField(
            model_name='pessoa',
            name='deficiencias',
            field=models.CharField(default='', max_length=100),
        ),
    ]
