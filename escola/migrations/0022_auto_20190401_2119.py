# Generated by Django 2.1.7 on 2019-04-02 00:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('escola', '0021_linkconteudo_conteudo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacao',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
