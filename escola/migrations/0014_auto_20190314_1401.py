# Generated by Django 2.1.2 on 2019-03-14 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_prometheus.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('escola', '0013_notificacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeguidorManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(blank=True, null=True)),
                ('seguidores', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            bases=(models.Model, django_prometheus.models.Mixin),
        ),
        migrations.AddField(
            model_name='tarefa',
            name='manager_seguidor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='escola.SeguidorManager'),
        ),
    ]
