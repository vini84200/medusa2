# Generated by Django 2.1.2 on 2019-03-05 22:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('leituras', '0027_auto_20190305_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livro',
            name='serie',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='leituras.Serie'),
        ),
    ]