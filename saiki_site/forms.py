from django import forms
from .models import Jogador

class JogadorForm(forms.ModelForm):
    name_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Jogador
        fields = ['name_public', 'name_user', 'name_email', 'name_password']
        labels = {
            'name_public': 'Nome Público',
            'name_user': 'Nome de Usuário',
            'name_email': 'Email',
            'name_password': 'Senha',
        }

    def save(self, commit=True):
        jogador = super().save(commit=False)
        jogador.set_password(self.cleaned_data['name_password'])
        if commit:
            jogador.save()
        return jogador

class JogadorLoginForm(forms.Form):
    name_user = forms.CharField(label="Nome de Usuário")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")