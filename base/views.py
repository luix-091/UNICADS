from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.urls import reverse
from .models import Pessoa, Endereco
from .forms import PessoaForm, EnderecoForm
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@login_required(login_url="login/")
def home(request):
    return render(request, 'home.html')

@login_required(login_url="login/")
def pessoas(request):
    pessoas_list = Pessoa.objects.all().order_by('nome')
    pesquisa = request.GET.get('pesquisa')

    if pesquisa:
        pessoas_list = pessoas_list.filter(
            Q(nome__icontains=pesquisa) | 
            Q(cpf__icontains=pesquisa) | 
            Q(data_nasc__icontains=pesquisa) |
            Q(genero__icontains=pesquisa) |
            Q(endereco__logradouro__icontains=pesquisa) |
            Q(endereco__regiao__icontains=pesquisa) |
            Q(endereco__bairro__icontains=pesquisa)
        )

    paginator = Paginator(pessoas_list, 12)
    pagina = request.GET.get('pagina')
    try:
        pessoas = paginator.page(pagina)
    except PageNotAnInteger:
        pessoas = paginator.page(1)
    except EmptyPage:
        pessoas = paginator.page(paginator.num_pages)
    
    for pessoa in pessoas:
        data_nasc_formatada = pessoa.data_nasc.strftime('%d/%m/%Y')
        pessoa.data_nasc = datetime.strptime(data_nasc_formatada, '%d/%m/%Y')
    
    return render(request, 'pessoas.html', {'pessoas': pessoas})

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
            deficiencias = request.POST.getlist('deficiencias')
            defi = ''
            for deficiencia in deficiencias:
                defi += f',{deficiencia}'
            defi = defi[1:]
            pessoa.deficiencias = defi
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
                if created:
                    if not Pessoa.objects.filter(endereco=pessoa.endereco).exclude(id=pessoa.id).exists():
                        pessoa.endereco.delete()
                else:
                    if pessoa.endereco:
                        pessoa.endereco.delete()
                pessoa.endereco = endereco
            deficiencias = request.POST.getlist('deficiencias')
            defi = ''
            for deficiencia in deficiencias:
                defi += f',{deficiencia}'
            defi = defi[1:]
            pessoa.deficiencias = defi
            pessoa.save()
            return redirect('pessoas')
    
    form_pessoa = PessoaForm(request.POST, instance=pessoa)
    form_endereco = EnderecoForm(request.POST, instance=pessoa.endereco)
    return render(request, 'editar.html', {'form_pessoa': form_pessoa, 'form_endereco': form_endereco, 'pessoa': pessoa, 'bairros':[bairro[0] for bairro in Endereco.BAIRROS_CHOICES]})

@login_required(login_url='login/')
def relatorio(request):
    pessoas = Pessoa.objects.all()
    total_pessoas = '{:,}'.format(pessoas.count()).replace(',', '.')
    selected_bairros = request.GET.getlist('bairros')
    selected_deficiencias = request.GET.getlist('deficiencias')

    bairros_com_data = []
    deficiencias_com_data = []

    deficiencias_por_bairro = {
        'Física': [],
        'Visual': [],
        'Auditiva': [],
        'Intelectual': [],
        'Psicossocial': []
    }
    bairro_por_deficiencia = {
        'Água Verde': [],
        'Águas Claras': [],
        'Amizade': [],
        'Barra do Rio Cerro': [],
        'Barra do Rio Molha': [],
        'Boa Vista': [],
        'Braço Ribeirão Cavalo': [],
        'Centenário': [],
        'Centro': [],
        'Chico de Paulo': [],
        'Czerniewicz': [],
        'Estrada Nova': [],
        'Ilha da Figueira': [],
        'Jaraguá 84': [],
        'Jaraguá 99': [],
        'Jaraguá Esquerdo': [],
        'João Pessoa': [],
        'Nereu Ramos': [],
        'Nova Brasília': [],
        'Parque Malwee': [],
        'Rau': [],
        'Ribeirão Cavalo': [],
        'Rio Cerro I': [],
        'Rio Cerro II': [],
        'Rio da Luz': [],
        'Rio Molha': [],
        'Santa Luzia': [],
        'Santo Antônio': [],
        'São Luís': [],
        'Tifa Martins': [],
        'Tifa Monos': [],
        'Três Rios do Norte': [],
        'Três Rios do Sul': [],
        'Vieira': [],
        'Vila Baependi': [],
        'Vila Lalau': [],
        'Vila Lenzi': [],
        'Vila Nova': []
    }

    CORES = {
        'Água Verde': 'rgba(255, 156, 156, 0.7)',
        'Águas Claras': 'rgba(230, 109, 69, 0.7)',
        'Amizade': 'rgba(255, 141, 48, 0.7)',
        'Barra do Rio Cerro': 'rgba(255, 189, 48, 0.7)',
        'Barra do Rio Molha': 'rgba(242, 242, 131, 0.7)',
        'Boa Vista': 'rgba(168, 89, 106, 0.7)',
        'Braço Ribeirão Cavalo': 'rgba(201, 242, 131, 0.7)',
        'Centenário': 'rgba(69, 240, 12, 0.7)',
        'Centro': 'rgba(12, 240, 103, 0.7)',
        'Chico de Paulo': 'rgba(215, 215, 219, 0.7)',
        'Czerniewicz': 'rgba(67, 156, 240, 0.7)',
        'Estrada Nova': 'rgba(131, 142, 230, 0.7)',
        'Ilha da Figueira': 'rgba(33, 58, 255, 0.7)',
        'Jaraguá 84': 'rgba(171, 140, 222, 0.7)',
        'Jaraguá 99': 'rgba(149, 86, 209, 0.7)',
        'Jaraguá Esquerdo': 'rgba(179, 7, 247, 0.7)',
        'João Pessoa': 'rgba(214, 122, 250, 0.7)',
        'Nereu Ramos': 'rgba(220, 79, 227, 0.7)',
        'Nova Brasília': 'rgba(252, 161, 3, 0.7)',
        'Parque Malwee': 'rgba(196, 245, 2, 0.7)',
        'Rau': 'rgba(250, 102, 218, 0.7)',
        'Ribeirão Cavalo': 'rgba(255, 161, 235, 0.7)',
        'Rio Cerro I': 'rgba(255, 3, 141, 0.7)',
        'Rio Cerro II': 'rgba(247, 77, 145, 0.7)',
        'Rio da Luz': 'rgba(156, 20, 74, 0.7)',
        'Rio Molha': 'rgba(156, 20, 47, 0.7)',
        'Santa Luzia': 'rgba(255, 61, 100, 0.7)',
        'Santo Antônio': 'rgba(255, 0, 0, 0.7)',
        'São Luís': 'rgba(36, 150, 91, 0.7)',
        'Tifa Martins': 'rgba(102, 125, 113, 0.7)',
        'Tifa Monos': 'rgba(216, 237, 95, 0.7)',
        'Três Rios do Norte': 'rgba(173, 90, 17, 0.7)',
        'Três Rios do Sul': 'rgba(7, 115, 113, 0.7)',
        'Vieira': 'rgba(159, 237, 236, 0.7)',
        'Vila Baependi': 'rgba(15, 189, 90, 0.7)',
        'Vila Lalau': 'rgba(35, 66, 84, 0.7)',
        'Vila Lenzi': 'rgba(154, 83, 176, 0.7)',
        'Vila Nova': 'rgba(255, 77, 231, 0.7)'
    }



       
    if selected_bairros:
        selected_deficiencias = None
        for bairro in selected_bairros:
            pessoas_bairro = pessoas.filter(endereco__bairro__icontains=bairro)
            if pessoas_bairro.exists():
                bairros_com_data.append(bairro)
                for deficiencia in deficiencias_por_bairro.keys():
                    deficiencias_por_bairro[deficiencia].append(pessoas_bairro.filter(deficiencias__icontains=deficiencia).count())
    if selected_deficiencias:
        selected_bairros = None
        for deficiencia in selected_deficiencias:
            pessoas_deficiencia = pessoas.filter(deficiencias__icontains=deficiencia)
            if pessoas_deficiencia.exists():
                deficiencias_com_data.append(deficiencia)
                for bairro in bairro_por_deficiencia.keys():
                    bairro_por_deficiencia[bairro].append(pessoas_deficiencia.filter(endereco__bairro__icontains=bairro).count())
                
    context = {
        'pessoas': pessoas,
        'total_pessoas': total_pessoas,
        'bairros': [bairro[0] for bairro in Endereco.BAIRROS_CHOICES],
        'selected_bairros': selected_bairros,
        'deficiencias': ['Auditiva', 'Física', 'Visual', 'Intelectual', 'Psicossocial'],
        'selected_deficiencias': selected_deficiencias,
        'bairros_com_data': bairros_com_data,
        'deficiencia_com_data': deficiencias_com_data,
        'deficiencia_por_bairro': deficiencias_por_bairro,
        'bairro_por_deficiencia': bairro_por_deficiencia,
        'bairros_keys': [bairro for bairro in bairro_por_deficiencia.keys()],
        'cores_bairros': CORES
    }


    context.update(deficiencias_por_bairro)
    context.update(bairro_por_deficiencia)

    return render(request, 'relatorios.html', context)

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
    return render(request, 'login.html', {'erro_login': erro_login, 'login': True})

def deslogar(request):
    logout(request)
    return redirect('login')