# Generated by Django 2.1.2 on 2019-03-04 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0002_auto_20190304_0908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='turma',
            options={'permissions': (('can_add_turma', 'Pode criar turmas'), ('can_edit_turma', 'Pode editar turmas'), ('can_delete_turma', 'Pode deletar turmas'), ('can_populate_turma', 'Pode popular turmas'))},
        ),
    ]
