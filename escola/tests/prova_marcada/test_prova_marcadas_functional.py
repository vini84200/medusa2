import logging
import time

import pytest


@pytest.mark.selenium_test
@pytest.mark.live_server_no_flush
def test_ver_datas_e_marcar_uma(dummy_professor, live_server, browser):
    # A Joana, uma professora de sua escola, precisa marcar uma prova com sua turma, ela entra na sua plataforma,
    # ela observa que está na página inicial já que havia logado anteriormente. Ela abre a vê na página inicial uma
    # lista de turmas do dia num painel com título escrito ’Resumo de Hoje’, com um subpainel ‘Turmas de Hoje’.
    # Ela aperta no primeiro botão ‘Química/203’ e é levada a uma página onde ela pode ver algumas informações, e em um
    # painel lateral ela vê um botão ‘Escolher data para marcar prova’, ela clica ali e é levada a uma página com título
    # ‘Datas livres da 203’ e embaixo há um calendário, o mês é o mesmo que o atual, datas passadas estão em cinza, já a
    # data atual em azul, as datas que o professor tem aula com a  turma em verde, já outras datas em branco.
    # Se houvesse alguma prova marcada estaria em vermelho. Cada data tem espaço para seus eventos, como provas, e
    # um botão escrito ‘Marcar prova’. Joana clica no botão do dia da próxima aula, e então a página é redirecionada
    # para uma página com título Marcar uma prova’, há alguns campos, o da data e da matéria já estão preenchidos com
    # os valores corretos, ela preenche o resto, como o nome de ‘Prova de Química’, preenche a descrição com ‘Prova
    # simples de Quimica’, e clica no botão ‘Marcar’. Ela é redirecionada a pagina inicial. Patricia abre um segundo
    # browser, e loga no seu usuario, ela está na sua pagina inicial, no final da pagina na lista de provas,
    # ela vê a prova que foi adicionada na lista.
    pass
