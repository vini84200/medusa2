#  Developed by Vinicius José Fritzen
#  Last Modified 20/04/19 08:59.
#  Copyright (c) 2019  Vinicius José Fritzen and Albert Angel Lanzarini

from django.urls import path, include
from rest_framework import routers

import escola.views_aluno
import escola.views_cargo
import escola.views_horario
import escola.views_materia
import escola.views_professor
import escola.views_tarefa
import escola.views_turma
import escola.views_conteudo
from escola.views_aviso import AvisoDetailView, AvisoTurmaCreateView
from escola.views_feedback import FeedbackView
from escola.quotes.quotes_views import AllQuotesView
from escola import api, views_profile, views_provas_marcadas
from . import views

router = routers.DefaultRouter()
router.register(r'users', api.UserViewSet)
router.register(r'groups', api.GroupViewSet)
router.register(r'profile', api.ProfileViewSet)
router.register(r'turma', api.TurmaViewSet)
router.register(r'seguidormanager', api.SeguidorManagerViewSet)
router.register(r'cargoturma', api.CargoTurmaViewSet)
router.register(r'professor', api.ProfessorViewSet)
router.register(r'materiadaturma', api.MateriaDaTurmaViewSet)
router.register(r'aluno', api.AlunoViewSet)
router.register(r'tarefa', api.TarefaViewSet)
router.register(r'tarefacompletacao', api.TarefaCompletacaoViewSet)
router.register(r'tarefacomentario', api.TarefaComentarioViewSet)
router.register(r'notificacao', api.NotificacaoViewSet)
router.register(r'horario', api.HorarioViewSet)
router.register(r'turno', api.TurnoViewSet)
router.register(r'turnoaula', api.TurnoAulaViewSet)
router.register(r'conteudo', api.ConteudoViewSet)
router.register(r'link_conteudo', api.LinkConteudoViewSet)
router.register(r'categoria_conteudo', api.CategoriaConteudoViewSet)

app_name = 'escola'

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('', views.index, name='index'),
    # turma
    path('turmas/', escola.views_turma.list_turmas, name='list-turmas'),
    path('turmas/add/', escola.views_turma.add_turma, name='add-turma'),
    path('turmas/<int:pk>', escola.views_turma.TurmaDetailView.as_view(), name='detail-turma'),
    path('turmas/<int:pk>/edit', escola.views_turma.edit_turma, name='edit-turma'),
    path('turmas/<int:pk>/delete', escola.views_turma.delete_turma, name='delete-turma'),
    path('alunos/populate/', escola.views_aluno.populate_alunos, name='populate-alunos'),
    # cargos
    path('turmas/<int:pk_turma>/cargos', escola.views_cargo.list_cargos, name='list-cargos'),
    path('turmas/<int:turma_pk>/cargos/add', escola.views_cargo.add_cargo, name='add-cargo'),
    path('turmas/cargos/edit/<int:pk>', escola.views_cargo.edit_cargo, name='edit-cargo'),
    path('turmas/cargos/delete/<int:pk>', escola.views_cargo.delete_cargo, name='delete-cargo'),
    # alunos
    path('turma/<int:turma_pk>/alunos', escola.views_aluno.list_alunos, name='list-alunos'),
    path('turma/<int:turma_pk>/alunos/add', escola.views_aluno.add_aluno, name='add-aluno'),
    path('turmas/aluno/<int:aluno_pk>/edit', views.edit_aluno, name='edit-aluno'),
    path('turmas/aluno/<int:aluno_pk>/delete', views.delete_aluno, name='delete-aluno'),
    # horario
    path('turma/<int:turma_pk>/horario', escola.views_horario.ver_horario, name='show-horario'),
    path('turma/<int:turma_pk>/horario/edit/<int:turno_cod>/<int:dia_cod>', escola.views_horario.alterar_horario,
         name='alterar-horario'),
    # professores
    path('professores/add', escola.views_professor.add_professor, name='add-professor'),
    path('professores/', escola.views_professor.list_professores, name='list-professores'),
    path('professor/<int:pk>/edit', escola.views_professor.edit_professor, name='edit-professor'),
    path('professor/<int:pk>/delete', escola.views_professor.delete_professor, name='delete-professor'),
    # materias
    path('turma/<int:turma_pk>/materias/add', escola.views_materia.add_materia, name='add-materia'),
    path('turma/<int:turma_pk>/materias', escola.views_materia.list_materias, name='list-materias'),
    path('materia/<int:materia_pk>/edit', escola.views_materia.edit_materia, name='edit-materia'),
    path('materia/<int:materia_pk>/delete', escola.views_materia.delete_materia,
         name='delete-materia'),
    path('materia/<int:pk>', escola.views_materia.MateriaDaTurmaDetailView.as_view(),
         name='detail-materia'),
    # tarefa
    path('turma/<int:turma_pk>/tarefas/add', escola.views_tarefa.add_tarefa, name='add-tarefa'),
    path('turma/<int:turma_pk>/tarefas', escola.views_tarefa.list_tarefa, name='list-tarefa'),
    path('turma/tarefa/<int:tarefa_pk>/edit', escola.views_tarefa.edit_tarefa, name='edit-tarefa'),
    path('turma/tarefa/<int:tarefa_pk>/delete', escola.views_tarefa.delete_tarefa, name='delete-tarefa'),
    path('turma/tarefa/<int:tarefa_pk>/concluir', escola.views_tarefa.concluir_tarefa, name='concluir-tarefa'),
    path('turma/tarefa/<int:tarefa_pk>', escola.views_tarefa.detalhes_tarefa, name='detalhes-tarefa'),
    # Seguir
    path('seguir/<int:pk>', views.seguir_manager, name='seguir'),
]

# Conteudos
urlpatterns += \
    [
        path('conteudo/<int:pk>', escola.views_conteudo.ConteudoDetail.as_view(), name='conteudo-detail'),
        path('conteudo/add/<int:pk_parent>', escola.views_conteudo.ConteudoCreate.as_view(), name='conteudo_add'),  # TODO: 13/04/2019 por wwwvi: Nomenclatura errada, mudar para add-conteudo
        path('conteudo/add/', escola.views_conteudo.ConteudoCreate.as_view(), name='conteudo_add'),  # TODO TAMBEM
        path('materia/<int:materia>/addConteudos', escola.views_conteudo.addConteudosAMateria.as_view(), name='add-conteudo-materia'),
        path('conteudo/<int:pk>/add', escola.views_conteudo.LinkConteudoCreateView.as_view(), name='add-link-conteudo'),
        path('link-conteudo/<int:pk>/remove', escola.views_conteudo.RemoveLinkFromConteudoView.as_view(), name='delete-link-conteudo'),
        path('conteudo/<int:pk>/add/<int:cat>', escola.views_conteudo.LinkConteudoCreateView.as_view(), name='add-link-conteudo'),
        path('conteudo/<int:pk>/edit', escola.views_conteudo.ConteudoUpdateView.as_view(), name='update-conteudo'),
    ]

# Notificações
urlpatterns += \
    [
        path('notificacoes', escola.views.NotificacaoListView.as_view(), name='notificacoes-list'),
        path('update-email', escola.views.atualisar_emails, name='update-email')
    ]

# Pagina de sobre
urlpatterns += \
    [
        path('sobre', escola.views.SobreView.as_view(), name='sobre'),
    ]

# Paginas do professor
urlpatterns += \
    [
        path('self/materias', escola.views_professor.MateriaProfessorListView.as_view(), name='materias_professor'),  # TODO: 13/04/2019 por wwwvi: Alterar name, nomeclatura esta errada
        path('self/conteudos', escola.views_conteudo.MeusConteudosListView.as_view(), name='conteudos-professor'),
    ]

# Offline template
urlpatterns += \
    [
        path('base_layout', escola.views.base_layout, name='base_layout_offline'),
    ]

# Perfil do usuario
urlpatterns +=\
    [
        path('self/emailChange', views_profile.email_change, name='self-email-change'),
    ]

# Marcar Provas

urlpatterns +=\
    [
        path('turmas/<int:turma_pk>/provas', views_provas_marcadas.ListaProvasTurmaView.as_view(),
             name='provas-turma-list'),
        path('provas/add/materia', views_provas_marcadas.CreateProvaMateriaView.as_view(),
             name='marcar-prova-materia'),
        path('provas/add/area', views_provas_marcadas.CreateProvaAreaView.as_view(),
             name='marcar-prova-area'),
        path('self/provas', views_provas_marcadas.ListaProvasProfessorView.as_view(),
             name='provas-professor'),  # As provas do professor
        path('provas/materia/<int:pk>/delete', views_provas_marcadas.ProvaMateriaDeleteView.as_view(),
             name='provas-materia-delete'),
        path('provas/area/<int:pk>/delete', views_provas_marcadas.ProvaAreaDeleteView.as_view(),
             name='provas-area-delete'),
        path('provas/<int:pk>', views_provas_marcadas.ProvaDetailView.as_view(),
             name='prova-detail'),
        path('turmas/<int:pk>/dias_livres', views_provas_marcadas.CalendarioTurmaDatasLivresView.as_view(),
             name='turma-provas-calendario'),
    ]

# Quotes

urlpatterns += \
    [
        path('all-quotes', AllQuotesView.as_view(), name='todas-quotes'),
    ]

# Feedback

urlpatterns += \
    [
        path('feedback', FeedbackView.as_view(), name='feedback'),
    ]

# Avisos

urlpatterns += \
    [
        path('aviso/add-turma', AvisoTurmaCreateView.as_view(), name='aviso-add-turma'),
        path('aviso/<int:pk>', AvisoDetailView.as_view(), name='aviso-detail'),
    ]

# Temporarias

# urlpatterns += \
#     [
#           JAMAIS ADICIONAR NOVAMENTE, É DEBUG!!!
#         path('users/', escola.views.UserListView.as_view())
#     ]
