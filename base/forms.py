from django import forms
from .models import Pessoa, Endereco

class PessoaForm(forms.ModelForm):
    detalhes = forms.CharField(required=False)
    necessidades = forms.CharField(required=False)
    class Meta:
        model = Pessoa
        fields = ['nome', 'cpf', 'data_nasc', 'genero', 'deficiencia','detalhes', 'necessidades']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'bairro', 'regiao']