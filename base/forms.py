from django import forms
from .models import Pessoa, Endereco

class PessoaForm(forms.ModelForm):
    class Meta:
        model = Pessoa
        fields = ['nome', 'cpf', 'data_nasc', 'genero', 'deficiencia', 'necessidades']

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['logradouro', 'bairro', 'regiao']