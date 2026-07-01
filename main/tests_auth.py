from unittest.mock import patch

from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import SignUpForm


class SignUpFormTests(TestCase):
    def test_email_is_unique_case_insensitive(self):
        User.objects.create_user(username='existing', email='User@Example.com', password='secret12345')

        form = SignUpForm(data={
            'full_name': 'Novo Usuario',
            'username': 'novo',
            'email': 'user@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_full_name_is_split_into_first_and_last_name(self):
        form = SignUpForm(data={
            'full_name': 'Maria Silva Souza',
            'username': 'maria',
            'email': 'maria@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()

        self.assertEqual(user.first_name, 'Maria')
        self.assertEqual(user.last_name, 'Silva Souza')
        self.assertEqual(user.email, 'maria@example.com')


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class AuthFlowTests(TestCase):
    def test_signup_creates_inactive_user_and_sends_activation_email(self):
        response = self.client.post(reverse('signup'), {
            'full_name': 'Ana Teste',
            'username': 'ana',
            'email': 'ana@example.com',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertEqual(response.status_code, 200)
        user = User.objects.get(username='ana')
        self.assertFalse(user.is_active)
        self.assertContains(response, 'ana@example.com')

    def test_signup_rolls_back_user_when_email_fails(self):
        with patch('main.views.EmailMessage.send', side_effect=RuntimeError('smtp down')):
            response = self.client.post(reverse('signup'), {
                'full_name': 'Erro Email',
                'username': 'erro',
                'email': 'erro@example.com',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='erro').exists())

    def test_activation_enables_inactive_user(self):
        user = User.objects.create_user(
            username='inactive',
            email='inactive@example.com',
            password='StrongPass123!',
            is_active=False,
        )
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        response = self.client.get(reverse('activate', args=[uidb64, token]))
        user.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(user.is_active)

    def test_login_uses_safe_next_url_only(self):
        User.objects.create_user(username='safe', password='StrongPass123!')

        response = self.client.post(
            f"{reverse('login')}?next=/laboratorio/",
            {'username': 'safe', 'password': 'StrongPass123!'},
        )
        self.assertRedirects(response, '/laboratorio/')

        self.client.logout()
        response = self.client.post(
            f"{reverse('login')}?next=https://evil.example/",
            {'username': 'safe', 'password': 'StrongPass123!'},
        )
        self.assertRedirects(response, '/')

    def test_logout_requires_post(self):
        User.objects.create_user(username='logout-user', password='StrongPass123!')
        self.client.login(username='logout-user', password='StrongPass123!')

        get_response = self.client.get(reverse('logout'))
        self.assertEqual(get_response.status_code, 405)

        post_response = self.client.post(reverse('logout'))
        self.assertRedirects(post_response, '/')
