from django import forms
from .models import Pessoa, Endereco
from datetime import date

class PessoaForm(forms.ModelForm):
    detalhes = forms.CharField(required=False)
    necessidades = forms.CharField(required=False)
    
    def clean_data_nasc(self):
        data_nasc = self.cleaned_data.get('data_nasc')
        if data_nasc and (data_nasc > date.today()) or data_nasc.year < 1900:
            raise forms.ValidationError('A data de nascimento não pode ser posterior à data atual ou anterior a 1900.')
        return data_nasc

    class Meta:
        model = Pessoa
        fields = ['nome', 'cpf', 'data_nasc', 'genero', 'deficiencias','detalhes', 'necessidades']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'bairro', 'regiao']