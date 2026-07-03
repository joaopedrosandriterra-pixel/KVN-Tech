from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.functions import Lower
from .models import Contact


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
        email = self.cleaned_data.get('email', '').strip().lower()
        if User.objects.annotate(email_lower=Lower('email')).filter(email_lower=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data['full_name'].strip()
        first_name, _, last_name = full_name.partition(' ')
        user.email = self.cleaned_data['email']
        user.first_name = first_name
        user.last_name = last_name
        if commit:
            user.save()
        return user

class ContactForm(forms.ModelForm):
    """Form for handling contact submissions with validation."""
    accept_contact = forms.BooleanField(required=True, label='Aceito ser contatado')

    class Meta:
        model = Contact
        fields = [
            'name', 'company', 'email', 'phone', 'service',
            'budget', 'deadline', 'message', 'dynamic_data'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'autocomplete': 'name'}),
            'company': forms.TextInput(attrs={'autocomplete': 'organization'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
            'phone': forms.TextInput(attrs={'autocomplete': 'tel'}),
            'service': forms.Select(),
            'budget': forms.Select(),
            'deadline': forms.Select(),
            'message': forms.Textarea(),
        }

    def clean(self):
        cleaned = super().clean()
        required_fields = ['name', 'email', 'service', 'budget', 'deadline', 'message']
        for field in required_fields:
            if not cleaned.get(field):
                self.add_error(field, 'Este campo é obrigatório.')
        return cleaned
