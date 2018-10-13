from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class CasaVotante(models.Model):
    nome = models.CharField(max_length=200)
    autoridade = models.IntegerField()

    def __str__(self):
        return self.nome.__str__()


class Cargo(models.Model):
    mandato = models.DurationField()
    nome = models.CharField(max_length=100)
    casa = models.ForeignKey(CasaVotante, on_delete=models.DO_NOTHING)
    tem_voto = models.BooleanField()

    def __str__(self):
        return self.nome.__str__() + " : " + self.casa.__str__() + "{" + self.pk.__str__() + "}"


class Cadeira(models.Model):
    cargo = models.ForeignKey(Cargo, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    public_key = models.CharField(max_length=30)
    casa = models.ForeignKey(CasaVotante, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.user is not None:
            return 'Cadeira n' + self.pk.__str__() + ' c:' + self.cargo.__str__() + ' de ' + self.user.first_name + ' ' + \
                   self.user.last_name
        return 'Cadeira n' + self.pk.__str__ + ' c:' + self.cargo.__str__() + ' -- inocupado '

    def is_ocupado(self):
        return self.user is not None


class TipoMocao(models.Model):
    nome = models.CharField(max_length=100)
    abreviatura = models.CharField(max_length=20)
    quorumMinimo = models.DecimalField(decimal_places=2,
                                       max_digits=3)  # Porcentagem de Quorum votante para abrir votaçao
    porcentagemDaCasa = models.DecimalField(decimal_places=2,
                                            max_digits=3)  # Porcentagem de Votos 'Sim' para moção passar, faltas são consideradas
    #                                           absetções,


class Mocao(models.Model):
    nome = models.CharField(max_length=200)
    numero = models.IntegerField()
    tipo = models.ForeignKey(TipoMocao, on_delete=models.DO_NOTHING)
    quorumMinimo = models.DecimalField(decimal_places=2, max_digits=3, null=True,
                                       blank=True)  # Porcentagem de Quorum votante para abrir votaçao
    porcentagemDaCasa = models.DecimalField(decimal_places=2, max_digits=3, null=True,
                                            blank=True)  # Porcentagem de Votos 'Sim' para moção passar, faltas são consideradas
    #                                           absetções,
    texto = models.TextField()
    casa = models.ForeignKey(CasaVotante, on_delete=models.CASCADE)


class TipoSesao(models.Model):
    nome = models.CharField(max_length=100)


class Sessao(models.Model):
    tipo = models.ForeignKey(TipoSesao, on_delete=models.DO_NOTHING)
    data = models.DateField()
    casa = models.ForeignKey(CasaVotante, on_delete=models.CASCADE)

    def registrar_preseca(self, cadeira):
        p = Presenca(sessao=self, cadeira=cadeira)
        p.save()

    @staticmethod
    def there_is_sessao_hoje():
        s = Sessao.objects.filter(data=timezone.now().today())
        return len(s) == 1

    @staticmethod
    def sessao_hoje():
        return Sessao.objects.filter(data=timezone.now().today())


class Presenca(models.Model):
    sessao = models.ForeignKey(Sessao, on_delete=models.CASCADE)
    cadeira = models.ForeignKey(Cadeira, on_delete=models.CASCADE)


class Votacao(models.Model):
    mocoes = models.ForeignKey(Mocao, on_delete=models.DO_NOTHING)
    casa = models.ForeignKey(CasaVotante, on_delete=models.DO_NOTHING)
    podeAbster = models.BooleanField()


class PosVoto(models.Model):
    votacao = models.ForeignKey(Votacao, on_delete=models.CASCADE)
    nome = models.CharField(max_length=200)
    desc = models.TextField()


class Voto(models.Model):
    votacao = models.ForeignKey(Votacao, on_delete=models.DO_NOTHING)
    cadeira = models.ForeignKey(Cadeira, on_delete=models.DO_NOTHING)
    voto = models.ForeignKey(PosVoto, on_delete=models.SET_NULL, null=True)
    assinatura = models.CharField(max_length=40)
