# Generated by Django 2.1.2 on 2018-10-12 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('leituras', '0014_auto_20181012_1456'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leitura',
            name='tipo',
        ),
        migrations.AlterField(
            model_name='livro',
            name='serie',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='leituras.Serie'),
        ),
    ]