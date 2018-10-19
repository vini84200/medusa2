from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone, dates
from .models import TipoMocao, Mocao, Cargo, Cadeira, CasaVotante, Votacao, Sessao, TipoSesao, PosVoto, User, Presenca, \
    Voto


def presenca_painel(request):
    sessao = get_object_or_404(Sessao, data=timezone.now().today())
    casa = sessao.casa
    cadeiras = get_list_or_404(Cadeira, casa=casa)
    presencas = Presenca.objects.filter(sessao=sessao)
    presentes = [a.cadeira.user for a in presencas]

    return render(request, 'voting/listaPresença.html', {
        'sessao': sessao,
        'casa': casa,
        'cadeiras': cadeiras,
        'presentes': presentes,
        'quorum': len(presencas) / len(cadeiras) * 100
    })


@login_required
def registrar_presenca(request, sessao):
    s = get_object_or_404(Sessao, pk=sessao)
    for c in request.user.cadeira_set.all():
        s.registrar_preseca(c)
    return HttpResponseRedirect(reverse('voting:home'))


@login_required
def loged_home(request):
    return render(request, 'voting/home.html', {
        'user': request.user,
        'there_is_sessao': Sessao.there_is_sessao_hoje(),
        'sessao_hoje': Sessao.sessao_hoje(),
    })

# def lista_de_votações_em_andamento(request):


# def telaDeVotação(request):
