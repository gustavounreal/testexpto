from django import forms
from .models import DadosUsuario

class DadosUsuarioForm(forms.ModelForm):
    class Meta:
        model = DadosUsuario
        fields = ['nome_completo', 'cpf', 'endereco', 'cep', 'email', 'banco', 'agencia', 'conta', 'pix', 'whatsapp']