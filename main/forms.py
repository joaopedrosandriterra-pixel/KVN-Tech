from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(
        label='Nome completo',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Nome completo'}),
    )
    email = forms.EmailField(
        label='Confirmação por e-mail',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
    )

    class Meta:
        model = User
        fields = ['full_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Nome de usuário'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Senha'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirme a senha'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['full_name']
        if commit:
            user.save()
        return user
