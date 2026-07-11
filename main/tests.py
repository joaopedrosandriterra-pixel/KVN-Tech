from django.test import TestCase

from .models import Project


class PageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Transformamos ideias em realidade')
        self.assertContains(response, 'href="/sobre/"')
        self.assertContains(response, 'href="/laboratorio/"')

    def test_home_page_shows_visible_projects_from_database(self):
        Project.objects.create(
            title='Sistema de Gestão',
            slug='sistema-de-gestao',
            short_description='Painel completo para operação diaria.',
            full_description='Sistema completo para gestão empresarial.',
            visible=True,
        )

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sistema de Gestão')
        self.assertContains(response, 'Painel completo para operação diaria.')

    def test_about_page_loads(self):
        response = self.client.get('/sobre/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Desenvolvedores focados em soluções reais')

    def test_laboratory_page_loads(self):
        response = self.client.get('/laboratorio/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projetos em andamento, ideias em evolução')
