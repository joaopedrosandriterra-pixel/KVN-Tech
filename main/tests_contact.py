from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Contact


class ContactTests(TestCase):
    def setUp(self):
        self.active_user = User.objects.create_user(
            username='active_user',
            email='active@example.com',
            password='StrongPass123!',
            is_active=True
        )
        self.inactive_user = User.objects.create_user(
            username='inactive_user',
            email='inactive@example.com',
            password='StrongPass123!',
            is_active=False
        )
        self.staff_user = User.objects.create_user(
            username='staff_user',
            email='staff@example.com',
            password='StrongPass123!',
            is_active=True,
            is_staff=True
        )

    def test_contact_page_unauthenticated_shows_login_warning(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Deseja solicitar um orçamento?')
        self.assertContains(response, 'você precisa estar cadastrado e logado')
        self.assertNotContains(response, 'id="service"')  # Form shouldn't be visible

    def test_contact_page_active_user_shows_form(self):
        self.client.force_login(self.active_user)
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'id="service"')
        self.assertContains(response, 'value="active_user"')  # Prefilled name
        self.assertContains(response, 'value="active@example.com"')  # Prefilled email

    def test_submit_contact_unauthenticated_fails(self):
        response = self.client.post(reverse('contact'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'service': 'Desenvolvimento Web',
            'budget': 'Até R$500',
            'deadline': '30 dias',
            'message': 'Description of the site',
            'accept_contact': 'on'
        })
        self.assertRedirects(response, reverse('login'))
        self.assertEqual(Contact.objects.count(), 0)


    def test_submit_contact_success_with_dynamic_data(self):
        self.client.force_login(self.active_user)
        response = self.client.post(reverse('contact'), {
            'name': 'João Silva',
            'company': 'Clínica X',
            'email': 'joao@example.com',
            'phone': '11999999999',
            'service': 'Desenvolvimento Web',
            'budget': 'R$500-1.500',
            'deadline': '30 dias',
            'message': 'Gostaria de um site com 5 páginas e logo.',
            'accept_contact': 'on',
            'web_pages': '5 páginas',
            'web_domain': 'Sim',
            'web_visual_identity': 'Não'
        })
        # Check redirection back to contact
        self.assertRedirects(response, reverse('contact'))
        
        # Verify db record creation
        self.assertEqual(Contact.objects.count(), 1)
        contact = Contact.objects.first()
        self.assertEqual(contact.name, 'João Silva')
        self.assertEqual(contact.company, 'Clínica X')
        self.assertEqual(contact.email, 'joao@example.com')
        self.assertEqual(contact.phone, '11999999999')
        self.assertEqual(contact.service, 'Desenvolvimento Web')
        self.assertEqual(contact.budget, 'R$500-1.500')
        self.assertEqual(contact.deadline, '30 dias')
        self.assertEqual(contact.message, 'Gostaria de um site com 5 páginas e logo.')
        
        # Verify dynamic fields structure
        self.assertEqual(contact.dynamic_data, {
            'Quantas páginas?': '5 páginas',
            'Já possui domínio?': 'Sim',
            'Tem identidade visual?': 'Não'
        })

    def test_panel_lists_solicitations_for_staff(self):
        Contact.objects.create(
            name='Maria Santos',
            email='maria@example.com',
            service='Roblox',
            budget='Até R$500',
            deadline='Urgente',
            message='Jogo Roblox simples.',
            dynamic_data={'Tipo do jogo?': 'Obby', 'Scripts?': 'Sim'}
        )
        # Verify staff access
        self.client.force_login(self.staff_user)
        response = self.client.get(reverse('panel'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maria Santos')
        self.assertContains(response, 'Roblox')
        self.assertContains(response, 'data-budget="Até R$500"')

    def test_delete_solicitation_via_panel(self):
        contact = Contact.objects.create(
            name='Excluir Teste',
            email='delete@example.com',
            service='API',
            budget='Até R$500',
            deadline='Sem urgência',
            message='API integration.'
        )
        self.assertEqual(Contact.objects.count(), 1)
        
        # Access as staff and post deletion
        self.client.force_login(self.staff_user)
        response = self.client.post(reverse('delete_contact', args=[contact.id]))
        self.assertRedirects(response, reverse('panel'))
        self.assertEqual(Contact.objects.count(), 0)
