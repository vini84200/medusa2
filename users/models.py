from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField


class Profile(models.Model):
    """Perfil basico, todos os usuarios do sistema devem ter um."""
    user = models.OneToOneField(
        User, related_name='profile_escola', on_delete=models.CASCADE)
    is_aluno = models.BooleanField('student status', default=False)
    is_professor = models.BooleanField('teacher status', default=False)
    bio = MarkdownxField(blank=True, null=True)
    cor = models.CharField(max_length=12, blank=True, null=True)

    receber_email_notificacao = models.BooleanField(default=True)

    @property
    def template_data(self):
        """
        Retorna valores basicos requeridos pelo template,
        como notificações, etc...
        """
        context = {
            'notificacoes': self.get_unread_notifications(),
            'notificacao_count': len(self.get_unread_notifications()),
        }
        return context

    def get_unread_notifications(self):
        """Retorna lista de todas as notificações não lidas desse usuario."""
        return self.user.notificacao_set.filter(visualizado=False) \
            .order_by('-dataCriado')

    def read_all_notifications(self):
        """Marca como lida todas as notificações"""
        for n in self.get_unread_notifications():
            n.visualizado = True
            n.save()

    def __str__(self):
        return f"Profile de {self.user.__str__()}"


class Aluno(models.Model):
    """Aluno de uma turma."""
    chamada = models.PositiveSmallIntegerField(
        null=True, blank=True, default=0)
    nome = models.CharField(max_length=70)
    user = models.OneToOneField(
        User, related_name='aluno', on_delete=models.CASCADE)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    class Meta:
        """Meta"""
        permissions = (('edit_aluno', 'Pode editar um aluno.'),
                       ('can_delete_aluno', 'Pode deletar um aluno.'),)


class Professor(models.Model):
    """Um professor, não esecifico para uma turma."""
    user = models.OneToOneField(
        User, related_name='professor', on_delete=models.CASCADE)
    nome = models.CharField(max_length=70)

    def __str__(self):
        return self.nome

    class Meta:
        """Classe meta"""
        permissions = (('can_add_professor', 'Pode adicionar um novo Professor'),
                       ('can_edit_professor', 'Pode editar um professor'),
                       ('can_delete_professor', 'Pode deletar um professor'),)
        ordering = ['nome']
