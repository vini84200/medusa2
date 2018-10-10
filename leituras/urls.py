from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'biblio'
urlpatterns = [
    path('', views.index, name='index'),
    path('livro/<int:livro_id>',               views.livro_detalhes, name='livro_detalhes'),
    # Leituras
    path('leituras',                           views.leituras_list,          name='list_leituras'),
    path('leitura/<int:leitura_id>',           views.leitura_detalhes,       name='leitura_detalhes'),
    path('leitura/add/<int:livro_id>',         views.leitura_add_view,       name='leitura_add'),
    path('leitura/iniciar/<int:leitura_id>',   views.leitura_iniciar,        name='leitura_iniciar'),
    path('leitura/atualizar/<int:leitura_id>', views.leitura_atualizar_post, name='leitura_atualizar'),
    path('leitura/delete/<int:leitura_id>',    views.leitura_apagar,         name='leitura_delete'),

    path('series',                             views.series_list, name='series_list'),
    path('serie/<int:series_id>',              views.series_det,  name='series_det')
]