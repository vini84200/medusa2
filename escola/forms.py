from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class CriarTurmaForm(forms.Form):
    numero = forms.IntegerField(label="Numero da Turma:",
                                      help_text="Coloque o numero da turma. Exs. 101, 303, 203, 204")
    ano = forms.IntegerField(label="Ano:", help_text="Ano de atividade dessa turma. Exs. 2018, 2019")

    def clean_numero(self):
        data = self.cleaned_data['numero']
        # Checks if it is zero or negative.
        if data <= 0:
            raise ValidationError(_('Numero invalido, por  favor informe um numero positivo'))

        return data

    def clean_ano(self):
        data = self.cleaned_data['ano']
        # Checks if it is zero or negative.
        if data <= 1940:
            raise ValidationError(_('Ano invalido, por  favor informe um ano depois de 1940.'))

        return data