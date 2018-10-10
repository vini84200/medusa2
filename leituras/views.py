from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotAllowed
from django.template import loader
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Livro, Leitura, Serie



# TODO: adicionar algum destaque para livros em leitura na lista de livros;
# TODO: MUITO NO FUTURO: adicionar foto da capa nos detalhes
# TODO: Adicionar pagina para cada serie.
# TODO: Implementar multiplos usuarios
# TODO: cadastrar livros;

def index(request):
    list_books = Livro.objects.all
    template = loader.get_template('leituras/index.html')
    context = {
        'list_books': list_books,
    }
    return HttpResponse(template.render(context, request))

# Livro

def livro_detalhes(request, livro_id):
    book = get_object_or_404(Livro, pk=livro_id)
    return render(request, 'leituras/detalheLivro.html', {'book': book, 'leituras': book.leitura_set.order_by('data')})

# Leitura:
@login_required
def leituras_list(request):
    list_readings = get_list_or_404(Leitura)
    return render(request, 'leituras/listLeituras.html', {'leituras': list_readings})

@login_required
def leitura_detalhes(request, leitura_id):
    leitura = get_object_or_404(Leitura, pk=leitura_id)
    atualizacoes = leitura.leitura_update_set.order_by('-data')
    return render(request, 'leituras/leitura.html', {'leitura': leitura, 'list_atualizacoes': atualizacoes})

@login_required
def leitura_add_view(request, livro_id):
    if not request.user.is_authenticated:
        return HttpResponse("Você precisa estar logado para criar uma leitura.")
    leitura = Leitura(livro=get_object_or_404(Livro, pk=livro_id), leitor=request.user)
    leitura.save()
    return HttpResponseRedirect(reverse('biblio:leitura_detalhes', args=(leitura.pk,)))

@login_required
def leitura_iniciar(request, leitura_id):
    leitura = get_object_or_404(Leitura, pk=leitura_id)
    leitura.iniciar_leitura()
    return HttpResponseRedirect(reverse('biblio:leitura_detalhes', args=(leitura.pk,)))

@login_required
def leitura_atualizar_post(request, leitura_id):
    leitura = get_object_or_404(Leitura, pk=leitura_id)
    pagina = request.POST['pagina']
    leitura.atualizar_leitura(int(pagina))
    return HttpResponseRedirect(reverse('biblio:leitura_detalhes', args=(leitura.pk,)))

@login_required
def leitura_finalizar(request, leitura_id):
    leitura = get_object_or_404(Leitura, pk=leitura_id)
    leitura.finaliza_leitura()
    return HttpResponseRedirect(reverse('biblio:leitura_detalhes', args=(leitura.pk,)))

@login_required
def leitura_abandona(request, leitura_id):
    leitura = get_object_or_404(Leitura, pk=leitura_id)
    leitura.abandonar_leitura()
    return HttpResponseRedirect(reverse('biblio:leitura_detalhes', args=(leitura.pk,)))

@login_required
def leitura_apagar(request, leitura_id):
    leitura = get_object_or_404(Leitura, pk=leitura_id)
    leitura.delete()
    return HttpResponseRedirect(reverse('biblio:index', ))

def series_list(request):
    series = Serie.objects.all()
    return render(request, 'leituras/series_list.html', {'series': series, })


def series_det(request, series_id):
    serie = get_object_or_404(Serie, pk=series_id)
    return render(request, 'leituras/serie.html', {'serie':serie,'livros': serie.livro_set.all()})
