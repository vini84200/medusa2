# Generated by Django 2.1.7 on 2019-04-02 00:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('escola', '0022_auto_20190401_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificacao',
            name='title',
            field=models.CharField(max_length=160),
        ),
    ]