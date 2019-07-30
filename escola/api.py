"""Views da API do sistema"""
#  Developed by Vinicius José Fritzen
#  Last Modified 12/04/19 13:19.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini
import logging

from django.contrib.auth.models import Group, User
from django.core.exceptions import PermissionDenied
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from escola import api_permissions

from . import models, serializers


logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    """
       API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]


class ProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for the Profile class"""

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class TurmaViewSet(viewsets.ModelViewSet):
    """ViewSet for the Turma class"""

    queryset = models.Turma.objects.all()
    serializer_class = serializers.TurmaSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class SeguidorManagerViewSet(viewsets.ModelViewSet):
    """ViewSet for the SeguidorManager class"""

    queryset = models.Notificador.objects.all()
    serializer_class = serializers.SeguidorManagerSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class CargoTurmaViewSet(viewsets.ModelViewSet):
    """ViewSet for the CargoTurma class"""

    queryset = models.CargoTurma.objects.all()
    serializer_class = serializers.CargoTurmaSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class ProfessorViewSet(viewsets.ModelViewSet):
    """ViewSet for the Professor class"""

    queryset = models.Professor.objects.all()
    serializer_class = serializers.ProfessorSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class MateriaDaTurmaViewSet(viewsets.ModelViewSet):
    """ViewSet for the MateriaDaTurma class"""

    queryset = models.MateriaDaTurma.objects.all()
    serializer_class = serializers.MateriaDaTurmaSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class AlunoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Aluno class"""

    queryset = models.Aluno.objects.all()
    serializer_class = serializers.AlunoSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class TarefaViewSet(viewsets.ModelViewSet):
    """ViewSet for the Tarefa class"""

    queryset = models.Tarefa.objects.all()
    serializer_class = serializers.TarefaSerializer
    permission_classes = [permissions.DjangoObjectPermissions]

    @action(detail=True, methods=['post'],
            permission_classes=[permissions.IsAuthenticated])
    def set_as_finished(self, request, pk=None):
        """Conclui a tarefa do aluno"""
        logger.info('set_as_finished: Iniciando')
        user = request.user
        if user.profile_escola.is_aluno:
            aluno = user.aluno
        else:
            logger.info("O usuario não é um aluno, por tanto"
                        "não pode concluir tarefas")
            raise PermissionDenied("O usuario não é um aluno, por tanto"
                                   "não pode concluir tarefas")
        tarefa: models.Tarefa = self.get_object()
        conc = tarefa.get_completacao(aluno)
        conc.completo = not conc.completo
        conc.save()
        logger.info('set_as_finished: Finalizando')
        return Response({'status': 'success',
                        'concluido': conc.completo})


class TarefaCompletacaoViewSet(viewsets.ModelViewSet):
    """ViewSet for the TarefaCompletacao class"""

    queryset = models.TarefaCompletacao.objects.all()
    serializer_class = serializers.TarefaCompletacaoSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class TarefaComentarioViewSet(viewsets.ModelViewSet):
    """ViewSet for the TarefaComentario class"""

    queryset = models.TarefaComentario.objects.all()
    serializer_class = serializers.TarefaComentarioSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class NotificacaoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Notificacao class"""

    queryset = models.Notificacao.objects.all()
    serializer_class = serializers.NotificacaoSerializer
    permission_classes = [permissions.DjangoObjectPermissions]

    @action(detail=True, methods=['get', 'post'],
            permission_classes=[api_permissions.IsAdminOrIsTheUser])
    def set_as_read(self, request, pk=None):
        """Define o campo de visualizado de uma notificação."""
        noti: models.Notificacao = self.get_object()
        noti.visualizado = True
        noti.save()
        return Response({'success': 'True'})


class HorarioViewSet(viewsets.ModelViewSet):
    """ViewSet for the Horario class"""

    queryset = models.Horario.objects.all()
    serializer_class = serializers.HorarioSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class TurnoViewSet(viewsets.ModelViewSet):
    """ViewSet for the Turno class"""

    queryset = models.Turno.objects.all()
    serializer_class = serializers.TurnoSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class TurnoAulaViewSet(viewsets.ModelViewSet):
    """ViewSet for the TurnoAula class"""

    queryset = models.TurnoAula.objects.all()
    serializer_class = serializers.TurnoAulaSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class ConteudoViewSet(viewsets.ModelViewSet):
    """Viewset for the Conteudo class"""
    queryset = models.Conteudo.objects.all()
    serializer_class = serializers.ConteudoSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class LinkConteudoViewSet(viewsets.ModelViewSet):
    """Viewset for the LinkConteudo class"""
    queryset = models.LinkConteudo.objects.all()
    serializer_class = serializers.LinkConteudoSerializer
    permission_classes = [permissions.DjangoObjectPermissions]


class CategoriaConteudoViewSet(viewsets.ModelViewSet):
    """Viewset for the CategoriaConteudo class"""
    queryset = models.CategoriaConteudo.objects.all()
    serializer_class = serializers.CategoriaConteudoSerializer
    permission_classes = [permissions.DjangoObjectPermissions]
