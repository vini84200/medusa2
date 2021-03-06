# Generated by Django 2.1.2 on 2019-03-05 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('escola', '0008_materiadaturma_abreviacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tarefa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=60)),
                ('tipo', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Tema'), (2, 'Trabalho'), (3, 'Pesquisa'), (4, 'Redação')], null=True)),
                ('descricao', models.TextField()),
                ('deadline', models.DateField(verbose_name='Data limite')),
                ('materia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='escola.MateriaDaTurma')),
                ('turma', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escola.Turma')),
            ],
        ),
        migrations.CreateModel(
            name='TarefaComentario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escola.Tarefa')),
            ],
        ),
        migrations.CreateModel(
            name='TarefaCompletacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completo', models.BooleanField(default=False)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escola.Aluno')),
                ('tarefa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='escola.Tarefa')),
            ],
        ),
    ]
