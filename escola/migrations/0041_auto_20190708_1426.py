# Generated by Django 2.2.2 on 2019-07-08 17:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0040_provamarcada_notificado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='turma',
            old_name='noti_tarefa_completa_proxima',
            new_name='noti_tarefa_proxima',
        ),
        migrations.RemoveField(
            model_name='turma',
            name='noti_tarefa_nao_completa_proxima',
        ),
    ]
