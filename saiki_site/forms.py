from django import forms
from .models import Jogador

class JogadorForm(forms.ModelForm):
    #name_password = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = Jogador
        fields = ['name_public', 'name_user', 'name_email', 'name_password']
        labels = {
            'name_public': 'Nome Público',
            'name_user': 'Nome de Usuário',
            'name_email': 'Email',
            'name_password': 'Senha',
        }
        widgets = {
            'name_public': forms.TextInput(attrs={'class': 'form-login-field', 'placeholder': 'Nome Público de Usuário'}),
            'name_user': forms.TextInput(attrs={'class': 'form-login-field', 'placeholder': 'Nome de Usuário'}),
            'name_email': forms.EmailInput(attrs={'class': 'form-login-field', 'placeholder': 'E-mail'}),
            'name_password': forms.PasswordInput(attrs={'class': 'form-login-field', 'placeholder': 'Senha'})
        }

    def save(self, commit=True):
        jogador = super().save(commit=False)
        jogador.set_password(self.cleaned_data['name_password'])
        if commit:
            jogador.save()
        return jogador

class JogadorLoginForm(forms.Form):
    name_user = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-login-field', 'placeholder': 'Nome de Usuário'}), label="Nome de Usuário")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-login-field', 'placeholder': 'Senha'}), label="Senha")
    
class MessageForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Digite sua mensagem...'}), max_length=1000)
