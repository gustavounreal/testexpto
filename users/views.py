from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from django.shortcuts import render
from datetime import date
from .models import DadosUsuario, CadastroVendas, Boleto
from .forms import DadosUsuarioForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal



@login_required
def home(request):
    try:
        dados_usuario = DadosUsuario.objects.get(user=request.user)
    except DadosUsuario.DoesNotExist:
        dados_usuario = None

    if request.method == 'POST':
        form = DadosUsuarioForm(request.POST, instance=dados_usuario)
        if form.is_valid():
            dados_usuario = form.save(commit=False)
            dados_usuario.user = request.user  # Ensure the user field is set
            dados_usuario.save()
            return redirect('home')
    else:
        form = DadosUsuarioForm(instance=dados_usuario)

    saldo_atual = 1000.00  # Example current balance, you should get this from your database or business logic

    context = {
        'form': form,
        'dados_usuario': dados_usuario,
        'saldo_atual': saldo_atual,
    }
    return render(request, 'home.html', context)

@login_required
def dashboard(request):
    # Exemplo de dados para tarefas e projetos
    tasks = {
        'pendentes': 5,
        'atrasadas': 2,
        'lista': [
            {'id': 1, 'descricao': 'Tarefa 1', 'status': 'Incomplete', 'data_vencimento': date(2024, 11, 1)},
            {'id': 2, 'descricao': 'Tarefa 2', 'status': 'To Do', 'data_vencimento': date(2024, 11, 2)},
            # Adicione mais tarefas conforme necessário
        ]
    }
    projects = {
        'em_andamento': 3,
        'atrasados': 1
    }
    shift_schedule = [
        {'data': '2024-11-01', 'dia_da_semana': 'Segunda-feira', 'horario': '08:00 - 17:00'},
        {'data': '2024-11-02', 'dia_da_semana': 'Terça-feira', 'horario': '08:00 - 17:00'},
        # Adicione mais turnos conforme necessário
    ]
    hoje = date.today()

    context = {
        'tasks': tasks,
        'projects': projects,
        'shift_schedule': shift_schedule,
        'hoje': hoje
    }
    return render(request, 'users/dashboard.html', context)

def redirect_to_login(request):
    return redirect('account_login')

@login_required
def cadastrar_dados_usuario(request):
    if request.method == 'POST':
        form = DadosUsuarioForm(request.POST)
        if form.is_valid():
            dados_usuario = form.save(commit=False)
            dados_usuario.user = request.user
            dados_usuario.save()
            return redirect('dados_usuario')
    else:
        form = DadosUsuarioForm()
    return render(request, 'cadastrar_dados_usuario.html', {'form': form})

@login_required
def alterar_dados_usuario(request):
    try:
        dados_usuario = DadosUsuario.objects.get(user=request.user)
    except DadosUsuario.DoesNotExist:
        return redirect('cadastrar_dados_usuario')

    if request.method == 'POST':
        form = DadosUsuarioForm(request.POST, instance=dados_usuario)
        if form.is_valid():
            form.save()
            return redirect('dados_usuario')
    else:
        form = DadosUsuarioForm(instance=dados_usuario)
    return render(request, 'alterar_dados_usuario.html', {'form': form})

@login_required
def atualizar_dados_usuario(request):
    try:
        dados_usuario = DadosUsuario.objects.get(user=request.user)
    except DadosUsuario.DoesNotExist:
        dados_usuario = DadosUsuario(user=request.user)

    if request.method == 'POST':
        form = DadosUsuarioForm(request.POST, instance=dados_usuario)
        if form.is_valid():
            dados_usuario = form.save(commit=False)
            dados_usuario.user = request.user  # Assegura que o campo user está definido
            dados_usuario.save()
            return redirect('perfil_usuario')  # Redireciona para a página de perfil do usuário
    else:
        form = DadosUsuarioForm(instance=dados_usuario)

    return render(request, 'users/home.html', {'form': form, 'dados_usuario': dados_usuario})

@login_required
def perfil_usuario(request):
    try:
        dados_usuario = DadosUsuario.objects.get(user=request.user)
    except DadosUsuario.DoesNotExist:
        dados_usuario = None

    context = {
        'dados_usuario': dados_usuario,
    }

    return render(request, 'users/home.html', context)



@login_required
def cadastro_clientes(request):
    return render(request, 'cadastroClientes.html')

@login_required
def buscar_vendedor(request):
    cpf = request.GET.get('cpf')
    try:
        vendedor = DadosUsuario.objects.get(cpf=cpf)
        return JsonResponse({'nome': vendedor.nome_completo})
    except DadosUsuario.DoesNotExist:
        return JsonResponse({'nome': None})
    
@login_required
def buscar_vendedor(request):
    cpf = request.GET.get('cpf')
    try:
        vendedor = DadosUsuario.objects.get(cpf=cpf)
        return JsonResponse({'nome': vendedor.nome_completo})
    except DadosUsuario.DoesNotExist:
        return JsonResponse({'nome': None})


def is_funcionario(user):
    return user.groups.filter(name='funcionarios').exists()

@user_passes_test(is_funcionario)
def cadastro_vendas(request):
    if request.method == 'POST':
        nome_completo = request.POST['nome_completo']
        cpf = request.POST['cpf']
        email = request.POST['email']
        telefone = request.POST['telefone']
        rua = request.POST['rua']
        numero = request.POST['numero']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        cep = request.POST['cep']
        valor_venda = float(request.POST['valor_venda'].replace('R$', '').replace('.', '').replace(',', '.'))
        quantidade_boletos = int(request.POST['quantidade_boletos'])
        data_vencimento = request.POST['data_vencimento']
        descricao_venda = request.POST['descricao_venda']
        forma_pagamento = request.POST['forma_pagamento']
        chave_pix = request.POST.get('chave_pix', '')
        observacoes = request.POST.get('observacoes', '')
        cpf_vendedor = request.POST['cpf_vendedor']
        
        try:
            vendedor = DadosUsuario.objects.get(cpf=cpf_vendedor)
        except DadosUsuario.DoesNotExist:
            messages.error(request, 'Vendedor não encontrado.')
            return redirect('cadastro_clientes')
        
        valor_por_boleto = valor_venda / quantidade_boletos
        
        venda = CadastroVendas(
            nome_completo=nome_completo,
            cpf=cpf,
            email=email,
            telefone=telefone,
            rua=rua,
            numero=numero,
            bairro=bairro,
            cidade=cidade,
            estado=estado,
            cep=cep,
            vendedor=vendedor,
            valor_venda=valor_venda,
            quantidade_boletos=quantidade_boletos,
            valor_por_boleto=valor_por_boleto,
            descricao_venda=descricao_venda,
            forma_pagamento=forma_pagamento,
            chave_pix=chave_pix,
            data_vencimento=data_vencimento,
            observacoes=observacoes
        )
        venda.save()
        messages.success(request, 'Cadastro realizado com sucesso!')
        return redirect('cadastro_clientes')
    return render(request, 'users/cadastroClientes.html')
@login_required
def no_access(request):
    messages.error(request, 'Você não tem acesso a esta página.')
    return redirect('home')


@login_required
def minhas_vendas(request):
    usuario = request.user
    vendas = CadastroVendas.objects.filter(vendedor__user=usuario)
    boletos = Boleto.objects.filter(venda__vendedor__user=usuario)
    valor_total_venda = sum(boleto.valor for boleto in boletos)
    total_boletos = boletos.count()
    boletos_pagos = boletos.filter(status_pagamento='pago')
    boletos_pendentes = boletos.filter(status_pagamento='pendente')
    total_boletos_pagos = sum(boleto.valor for boleto in boletos_pagos)
    total_boletos_pendentes = sum(boleto.valor for boleto in boletos_pendentes)
    comissao = valor_total_venda * Decimal('0.05')  # Calcula 5% do valor total da venda
    quantidade_vendas = vendas.count()
    
    context = {
        'vendas': vendas,
        'boletos': boletos,
        'valor_total_venda': valor_total_venda,
        'total_boletos': total_boletos,
        'boletos_pagos': boletos_pagos.count(),
        'boletos_pendentes': boletos_pendentes.count(),
        'total_boletos_pagos': total_boletos_pagos,
        'total_boletos_pendentes': total_boletos_pendentes,
        'comissao': comissao,
        'quantidade_vendas': quantidade_vendas,
        'historico_pagamentos': boletos_pagos,
    }
    return render(request, 'users/minhasVendas.html', context)

@login_required
def buscar_boletos(request):
    cpf = request.GET.get('cpf')
    boletos_data = []
    cliente = None
    if cpf:
        try:
            cliente = CadastroVendas.objects.filter(cpf=cpf).first()
            vendas = CadastroVendas.objects.filter(cpf=cpf)
            for venda in vendas:
                boletos = Boleto.objects.filter(venda=venda).order_by('data_vencimento')
                for boleto in boletos:
                    boletos_data.append({
                        'id': boleto.id,
                        'status': boleto.status_pagamento,
                        'data_vencimento': boleto.data_vencimento
                    })
        except CadastroVendas.DoesNotExist:
            pass
    context = {'boletos': boletos_data, 'cliente': cliente}
    return render(request, 'users/painel_Alteracoes_Venda.html', context)


@login_required
@require_POST
def alterar_status_boleto(request, boleto_id):
    status = request.POST.get('status')
    try:
        boleto = Boleto.objects.get(id=boleto_id)
        boleto.status_pagamento = status
        boleto.save()
        messages.success(request, 'Status do boleto alterado com sucesso.')
    except Boleto.DoesNotExist:
        messages.error(request, 'Boleto não encontrado.')
    return redirect(request.META.get('HTTP_REFERER', 'buscar_boletos'))