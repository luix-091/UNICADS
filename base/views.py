from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Pessoa, Endereco
from .forms import PessoaForm, EnderecoForm
from datetime import datetime

# Create your views here.
@login_required(login_url="login/")
def home(request):
    return render(request, 'home.html')

@login_required(login_url="login/")
def pessoas(request):
    pessoas = Pessoa.objects.all()
    pesquisa = request.GET.get('pesquisa')

    if pesquisa:
        pessoas = pessoas.filter(
            Q(nome__icontains=pesquisa) | 
            Q(cpf__icontains=pesquisa) | 
            Q(data_nasc__icontains=pesquisa) |
            Q(genero__icontains=pesquisa) |
            Q(endereco__logradouro__icontains=pesquisa) |
            Q(endereco__regiao__icontains=pesquisa) |
            Q(endereco__bairro__icontains=pesquisa)
        )
    
    for pessoa in pessoas:
        data_nasc_formatada = pessoa.data_nasc.strftime('%d/%m/%Y')
        pessoa.data_nasc = datetime.strptime(data_nasc_formatada, '%d/%m/%Y')
    return render(request, 'pessoas.html', {'pessoas':pessoas})

@login_required(login_url='login/')
def cad_pessoa(request):
    if request.method == 'POST':
        form_pessoa = PessoaForm(request.POST)
        form_endereco = EnderecoForm(request.POST)
        if form_pessoa.is_valid():
            pessoa = form_pessoa.save(commit=False)
            if form_endereco.is_valid():
                endereco_data = form_endereco.cleaned_data
                endereco, created = Endereco.objects.get_or_create(
                    logradouro=endereco_data['logradouro'],
                    bairro=endereco_data['bairro'],
                    regiao=endereco_data['regiao']
                )
                pessoa.endereco = endereco
            pessoa.save()
            return redirect('pessoas')
    return render(request, 'cadastro.html', {'bairros': [bairro[0] for bairro in Endereco.BAIRROS_CHOICES]})


@login_required(login_url="login/")
def apagar_pessoa(request, pessoa_id):
    pessoa = get_object_or_404(Pessoa, id=pessoa_id)
    if request.method == 'POST':
        pessoa.delete()
    return redirect('pessoas')

@login_required(login_url='login/')
def editar_pessoa(request, pessoa_id):
    pessoa = Pessoa.objects.get(id=pessoa_id)
    if request.method == 'POST':
        form_pessoa = PessoaForm(request.POST, instance=pessoa)
        if pessoa.endereco:
            form_endereco = EnderecoForm(request.POST, instance=pessoa.endereco)
        else:
            form_endereco = EnderecoForm(request.POST)
        if form_pessoa.is_valid():
            pessoa = form_pessoa.save(commit=False)
            if form_endereco.is_valid():
                endereco_data = form_endereco.cleaned_data
                endereco, created = Endereco.objects.get_or_create(
                        logradouro=endereco_data['logradouro'],
                        bairro=endereco_data['bairro'],
                        regiao=endereco_data['regiao']
                )
                pessoa.endereco = endereco
            pessoa.save()
            return redirect('pessoas')
    
    form_pessoa = PessoaForm(request.POST, instance=pessoa)
    form_endereco = EnderecoForm(request.POST, instance=pessoa.endereco)
    return render(request, 'editar.html', {'form_pessoa': form_pessoa, 'form_endereco': form_endereco, 'pessoa': pessoa, 'bairros':[bairro[0] for bairro in Endereco.BAIRROS_CHOICES]})

@login_required(login_url='login/')
def relatorio(request):

    pessoas = Pessoa.objects.all()
    total_pessoas = '{:,}'.format(Pessoa.objects.all().count()).replace(',', '.')

    selected_bairros = request.GET.getlist('bairros')
    bairros_com_data = []
    
    deficiencia_fisica_por_bairro = []
    deficiencia_visual_por_bairro = []
    deficiencia_auditiva_por_bairro = []
    deficiencia_intelectual_por_bairro = []
    deficiencia_psicossocial_por_bairro = []

    if selected_bairros:
        for bairro in selected_bairros:
            if Pessoa.objects.filter(Q(endereco__bairro__icontains=bairro)).count() > 0:
                bairros_com_data.append(bairro)
                deficiencia_fisica_por_bairro.append(Pessoa.objects.filter(
                Q(endereco__bairro__icontains=bairro) &
                Q(deficiencia__icontains='Física')
                ).count())
                deficiencia_visual_por_bairro.append(Pessoa.objects.filter(
                Q(endereco__bairro__icontains=bairro) &
                Q(deficiencia__icontains='Visual')
                ).count())
                deficiencia_auditiva_por_bairro.append(Pessoa.objects.filter(
                Q(endereco__bairro__icontains=bairro) &
                Q(deficiencia__icontains='Auditiva')
                ).count())
                deficiencia_intelectual_por_bairro.append(Pessoa.objects.filter(
                Q(endereco__bairro__icontains=bairro) &
                Q(deficiencia__icontains='Intelectual')
                ).count())
                deficiencia_psicossocial_por_bairro.append(Pessoa.objects.filter(
                Q(endereco__bairro__icontains=bairro) &
                Q(deficiencia__icontains='Psicossocial')
                ).count())

    return render(request, 'relatorios.html', {'pessoas': pessoas, 'total_pessoas': total_pessoas, 'bairros': [bairro[0] for bairro in Endereco.BAIRROS_CHOICES], 'selected_bairros': selected_bairros, 'bairros_com_data':bairros_com_data, 'deficiencia_fisica_por_bairro': deficiencia_fisica_por_bairro,'deficiencia_auditiva_por_bairro': deficiencia_auditiva_por_bairro,'deficiencia_visual_por_bairro': deficiencia_visual_por_bairro,'deficiencia_intelectual_por_bairro': deficiencia_intelectual_por_bairro,'deficiencia_psicossocial_por_bairro': deficiencia_psicossocial_por_bairro})


def logar(request):
    erro_login = None
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('user'), password=request.POST.get('senha'))
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                return redirect('home')
        else:
            erro_login = 'Credenciais incorretas. Por favor, tente novamente.'
    return render(request, 'login.html', {'erro_login': erro_login})

def deslogar(request):
    logout(request)
    return redirect('login')