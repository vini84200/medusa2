import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestEditora:
    sch = 'leituras.Editora'

    def test_init(self):
        """Testa se uma instancia foi criada."""
        obj = mixer.blend(self.sch)
        assert obj.pk == 1, 'Deve criar instancia'

    def test_string(self):
        """Testa se o __str__() retorna valor correto"""
        obj = mixer.blend(self.sch, nome="Parabolias")
        assert obj.__str__() is "Parabolias"


class TestAutor:
    sch = 'leituras.Autor'

    def test_init(self):
        """Testa se uma instancia foi criada."""
        obj = mixer.blend(self.sch)
        assert obj.pk == 1, 'Deve criar instancia'

    def test_string(self):
        """Testa se o __str__() retorna no formato SOBRENOME, NOME"""
        obj = mixer.blend(self.sch, nome="Nomezinho", sobrenome="Das Laranjeiras")
        assert obj.__str__() == "Das Laranjeiras, Nomezinho"


class TestSerie:
    sch = 'leituras.Serie'

    def test_init(self):
        """Testa se uma instancia foi criada."""
        obj = mixer.blend(self.sch)
        assert obj.pk == 1, 'Deve criar instancia'

    def test_string(self):
        """Testa se o __str__() retorna o titulo da serie"""
        obj = mixer.blend(self.sch, titulo="Parabolias")
        assert obj.__str__() is "Parabolias"

    def test_get_livros_vazio(self):
        """Testa a função de obter os livros da serie, sendo que esta não possui livros."""
        obj = mixer.blend(self.sch)
        assert len(obj.get_livros()) is 0

    def test_get_livros_varios(self):
        """Testa a função get_livros(), com diversos livros"""
        # TODO: VERIFICAR SE OS LIVROS ESTÃO REALMENTE APARECENDO

        obj = mixer.blend(self.sch)
        l1 = mixer.blend("leituras.Livro", serie=obj)
        l2 = mixer.blend("leituras.Livro", serie=obj)
        assert len(obj.get_livros()) is 2, 'Devem haver dois livros na serie'


class TestLivro:
    sch = 'leituras.Livro'

    def test_init(self):
        """Testa se uma instancia foi criada."""
        obj = mixer.blend(self.sch)
        assert obj.pk == 1, 'Deve criar instancia'

    def test_string(self):
        """Testa se o __str__() retorna no formato TITULO, por SOBRENOME, NOME"""
        autor = mixer.blend('leituras.Autor', nome='Agape', sobrenome='Garismo')
        obj = mixer.blend(self.sch, titulo="Cafeinas", autor=autor)
        assert obj.__str__() == "Cafeinas, por Garismo, Agape"

    def _test_get_leituras_vazio(self):
        """Deve retornar vazio se não houverem leituras"""
        assert False, "Não Implementado"

    def test_set_lido(self):
        """Testa o funcionamento da função"""
        obj = mixer.blend(self.sch)
        obj.set_lido(True)
        assert obj.lido is True, "O valor deve ser o mesmo que o setado."
        obj.set_lido(False)
        assert obj.lido is False, "O valor deve ser o mesmo que o setado."


class TestLeitura:
    sch = 'leituras.Leitura'
    lu = 'leituras.Leitura_Update'

    def test_init(self):
        """Testa se uma instancia foi criada."""
        obj = mixer.blend(self.sch)
        assert obj.pk == 1, 'Deve criar instancia'

    def test_string(self):
        """Testa se o __str__() retorna no formato TITULO, por SOBRENOME, NOME"""
        autor = mixer.blend('leituras.Autor', nome='Agape', sobrenome='Garismo')
        livro = mixer.blend('leituras.Livro', titulo="Cafeinas", autor=autor)
        obj = mixer.blend(self.sch, livro=livro)
        assert obj.__str__() == "Leitura de Cafeinas, por Garismo, Agape"

    def test_is_iniciado(self):
        obj = mixer.blend(self.sch)
        assert obj.is_iniciado() is False
        lu = mixer.blend(self.lu, leitura=obj)
        assert obj.is_iniciado() is True

    def test_status(self):
        obj = mixer.blend(self.sch)
        assert obj.status() == 'Não iniciada', 'Antes que uma atualização seja feita, o resultado deve ser não iniciado.'
        luIniciado = mixer.blend(self.lu, tipo='IN', leitura=obj)
        assert obj.status() == 'Iniciada'
        luEmLeitura = mixer.blend(self.lu, tipo='LD', leitura=obj)
        assert obj.status() == 'Em leitura'
        luFinalizada = mixer.blend(self.lu, tipo='FN', leitura=obj)
        assert obj.status() == 'Finalizada'

        # Testa para Abandono
        objb = mixer.blend(self.sch)
        luIniciadob = mixer.blend(self.lu, tipo='IN', leitura=objb)
        luEmLeiturab = mixer.blend(self.lu, tipo='LD', leitura=objb)
        luAbandonadab = mixer.blend(self.lu, tipo='AB', leitura=objb)
        assert objb.status() == 'Abadonada'
