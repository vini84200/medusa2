from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
class Editora(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    class Meta:
        ordering =['nome']


class Autor(models.Model):
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    # function getName():
    # nome+", "+sobrenome

    def __str__(self):
        return self.sobrenome.__str__() + ", " + self.nome.__str__()

    class Meta:
        ordering =['sobrenome','nome']

class Serie(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor,on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.titulo

    def get_livros(self):
        return self.livro_set.all()
    class Meta:
        ordering=['titulo']


class Livro(models.Model):
    titulo = models.CharField(max_length=200);
    isbn = models.CharField(max_length=13);
    autor = models.ForeignKey\
        (Autor, on_delete=models.CASCADE)
    paginas = models.IntegerField()
    editora = models.ForeignKey(Editora, on_delete=models.CASCADE,null=True, blank=True)
    serie = models.ForeignKey(Serie, on_delete=models.DO_NOTHING, null=True, default=None, blank=True)
    nSerie = models.IntegerField(null=True, default=0) ## Em 0, não possui um numero especifico, como um extra da série
    lido = models.BooleanField(default=False)

    def __str__(self):
        return self.titulo + ", por " + self.autor.__str__()

    def get_leituras(self):
        return self.leitura_set.order_by('-data')

    def set_lido(self, lido):
        self.lido = lido

    class Meta:
        ordering =['autor','serie','nSerie','titulo']


class Leitura(models.Model):
    livro = models.ForeignKey(Livro,
                              on_delete=models.CASCADE)
    data = models.DateTimeField('Data que a leitura foi criada', auto_now_add=True)
    dataUpdate = models.DateTimeField('Data em que a leitura foi atualizada', auto_now=True)
    leitor = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)

    # possTipos = (('IN', 'Iniciada'), ('LD', 'Em leitura'), ('FN', 'Finalizada'), ('AB', 'abadonada'))
    # tipo = models.CharField(max_length=2, choices=possTipos, default='IN')

    def __str__(self):
        return "Leitura de " + self.livro.__str__()
    def is_iniciado(self):
        if (self.leitura_update_set.order_by('data').last() == None):
            return False
        else:
            return True

    def status(self):
        if (self.leitura_update_set.order_by('data').last() == None):
            return 'Não iniciada'
        return self.leitura_update_set.order_by('data').last().get_tipo_display()

    def get_last_leitura(self):
        return self.leitura_update_set.order_by('data').last()

    def get_last_pagina(self):
        return self.get_last_leitura().pagina

    def get_porcentagem_leitura(self):
        return self.get_last_pagina()*100/self.livro.paginas

    def get_data_inicio(self):
        if (self.leitura_update_set.order_by('data').last() == None):
            return 'Não iniciado'
        return self.leitura_update_set.filter(tipo = 'IN').first().data

    def iniciar_leitura(self):
        l = Leitura_Update(tipo = 'IN', leitura=self, pagina=1)
        l.save()
        #self.tipo = 'IN'
        return l

    def atualizar_leitura(self, pagina):
        # FIXME: Adicionar testes
        # Fixme: se você adicionar uma atualização depois de terminar ele aceita
        if(pagina >= self.livro.paginas):
             l = Leitura_Update(tipo='FN', leitura=self, pagina=self.livro.paginas)
             #self.tipo = 'FN'
        else:
            if(pagina >= self.get_last_pagina() ):
                l = Leitura_Update(tipo='LD', leitura=self, pagina=pagina)
                #self.tipo = 'LD'
            else:
                l= Leitura_Update(tipo='LD', leitura=self, pagina = self.get_last_pagina())
                #self.tipo = 'LD'
        l.save()
        return l;

    def finaliza_leitura(self):
        l = Leitura_Update(tipo='FN', leitura=self, pagina=self.livro.paginas)
        #self.tipo = 'FN'

    def abandonar_leitura(self, pagina):
        l = Leitura_Update(tipo='AB', leitura=self, pagina=self.livro.paginas)
        #self.tipo = 'AB'


class Leitura_Update(models.Model):
    leitura = models.ForeignKey(Leitura, on_delete=models.CASCADE)
    possTipos = (('IN', 'Iniciada'),('LD','Em leitura'), ('FN', 'Finalizada'),('AB','Abadonada'))
    tipo = models.CharField(max_length=2, choices=possTipos, default='IN')
    pagina = models.IntegerField()
    data = models.DateTimeField('Data da atualização', default=timezone.now)
    def __str__(self):
        return self.leitura.livro.__str__ + ", Pagina " + self.pagina.__str__()
    def get_tipo(self):
        return self.get_tipo_display()


class Biblioteca(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    livros = models.ManyToManyField(Livro)
    name = models.CharField(max_length=70)

    def add_livro(self, livro):
        self.livros.add(livro)

    def __str__(self):
        return self.name.__str__()
