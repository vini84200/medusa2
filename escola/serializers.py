"""Serializadores dos models para a API"""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from rest_polymorphic.serializers import PolymorphicSerializer
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'is_staff')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name',)



class TurmaSerializer(serializers.ModelSerializer):
    lider = GroupSerializer(required=True)
    vicelider = GroupSerializer(required=True)
    regente = GroupSerializer(required=True)

    class Meta:
        model = models.Turma
        fields = (
            'pk',
            'numero',
            'ano',
            'lider',
            'vicelider',
            'regente'
        )


class SeguidorManagerSerializer(serializers.ModelSerializer):
    seguidores = UserSerializer(many=True, read_only=True)

    class Meta:
        model = models.Notificador
        fields = (
            'pk',
            'link',
            'seguidores',
        )


class CargoTurmaSerializer(serializers.ModelSerializer):
    turma = TurmaSerializer()
    ocupante = UserSerializer()

    class Meta:
        model = models.CargoTurma
        fields = (
            'pk',
            'nome',
            'cod_especial',
            'ativo',
            'turma',
            'ocupante',
        )


class ProfessorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Professor
        fields = (
            'pk',
            'nome',
            'user',
        )


class MateriaDaTurmaSerializer(serializers.ModelSerializer):
    professor = ProfessorSerializer()

    class Meta:
        model = models.MateriaDaTurma
        fields = (
            'pk',
            'nome',
            'abreviacao',
            'professor',
            'conteudos',
        )


class AlunoSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    turma = TurmaSerializer()

    class Meta:
        model = models.Aluno
        fields = (
            'pk',
            'chamada',
            'nome',
            'user',
            'turma',
        )


class TarefaSerializer(serializers.ModelSerializer):
    turma = TurmaSerializer()
    materia = MateriaDaTurmaSerializer()

    class Meta:
        model = models.Tarefa
        fields = (
            'pk',
            'titulo',
            'tipo',
            'descricao',
            'deadline',
            'turma',
            'materia',
            'tarefacomentario_set',
        )


class TarefaCompletacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TarefaCompletacao
        fields = (
            'pk',
            'completo',
        )


class TarefaComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TarefaComentario
        fields = (
            'pk',
            'texto',
            'created_on',
        )


class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notificacao
        fields = (
            'pk',
            'visualizado',
            'dataCriado',
            'title',
            'msg',
            'link',
        )


class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Horario
        fields = (
            'pk',
            'turma',
        )


class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Turno
        fields = (
            'pk',
            'nome',
            'cod',
            'horaInicio',
            's1',
            's2',
            's3',
            's4',
            's5',
            'horaFim',
        )


class TurnoAulaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TurnoAula
        fields = (
            'pk',
            'diaDaSemana',
            'turno',
            'horario',
            'turma',
        )


class ConteudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Conteudo
        fields = (
            'pk',
            'nome',
            'professor',
            'descricao',
            'parent',
        )


class CategoriaConteudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoriaConteudo
        fields = (
            'nome',
            'cor',
        )


class LinkConteudoSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()
    categoria = CategoriaConteudoSerializer()

    class Meta:
        model = models.LinkConteudo
        fields = (
            'pk',
            'titulo',
            'link',
            'categoria',
            'descricao',
            'tags',
        )

# Provas e eventos


class AreaConhecimentoSerializer(serializers.ModelSerializer):
    turma = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='turma-detail',
        read_only=True,
    )
    class Meta:
        model = models.AreaConhecimento
        fields = (
            'id',
            'nome',
            'turma',
        )


class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Evento
        fields = (
            'nome',
            'data',
            'descricao'
        )


class EventoTurmaSerializer(serializers.ModelSerializer):
    turma = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='turma-detail',
        read_only=True
    )

    class Meta:
        model = models.EventoTurma
        fields = (
            'nome',
            'data',
            'descricao',
            'turma'
        )


class ProvaMarcadaSerializer(serializers.ModelSerializer):
    turma = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='turma-detail',
        read_only=True
    )
    conteudo = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='conteudo-detail',
        read_only=True
    )

    class Meta:
        model = models.ProvaMarcada
        fields = (
            'nome',
            'data',
            'descricao',
            'turma',
            'conteudo',
        )


class ProvaMarcadaMateriaSerializer(serializers.ModelSerializer):
    turma = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='turma-detail',
        read_only=True
    )
    conteudo = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='conteudo-detail',
        read_only=True
    )
    materia = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='materia-detail',
        read_only=True
    )
    item_avaliativo = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='item_avaliativo-detail',
        read_only=True
    )
    class Meta:
        model = models.ProvaMarcada
        fields = (
            'nome',
            'data',
            'descricao',
            'turma',
            'conteudo',
            'materia',
            'item_avaliativo',
        )


class ProvaMarcadaAreaSerializer(serializers.ModelSerializer):
    turma = serializers.HyperlinkedRelatedField(
        many=False,
        view_name='turma-detail',
        read_only=True
    )
    conteudo = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='conteudo-detail',
        read_only=True
    )
    area = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='area-detail',
        read_only=True
    )
    item_avaliativo = serializers.HyperlinkedRelatedField(
        many=True,
        view_name='item_avaliativo-detail',
        read_only=True
    )

    class Meta:
        model = models.ProvaMarcada
        fields = (
            'nome',
            'data',
            'descricao',
            'turma',
            'conteudo',
            'area',
            'item_avaliativo',
        )


class EventoPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        models.Evento: EventoSerializer,
        models.EventoTurma: EventoTurmaSerializer,
        models.ProvaMarcada: ProvaMarcadaSerializer,
        models.ProvaMateriaMarcada: ProvaMarcadaMateriaSerializer,
        models.ProvaAreaMarcada: ProvaMarcadaAreaSerializer,
    }


class ProvaMarcadaPolymorphicSerializer(PolymorphicSerializer):
    model_serializer_mapping = {
        models.ProvaMarcada: ProvaMarcadaSerializer,
        models.ProvaAreaMarcada: ProvaMarcadaAreaSerializer,
        models.ProvaMateriaMarcada: ProvaMarcadaMateriaSerializer,
    }