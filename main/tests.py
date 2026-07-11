from django.test import TestCase

from .models import CaseStudy, Project


class PageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Transformamos ideias em realidade')
        self.assertContains(response, 'href="/sobre/"')
        self.assertContains(response, 'href="/laboratorio/"')
        self.assertContains(response, 'href="/faq/"')
        self.assertContains(response, 'href="/cases/"')

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

    def test_faq_page_loads(self):
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Perguntas Frequentes')
        self.assertContains(response, 'Quanto custa um site?')

    def test_cases_page_public(self):
        response = self.client.get('/cases/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cases de desenvolvimento')

    def test_case_detail_public(self):
        case = CaseStudy.objects.create(
            title='Sistema para Padaria',
            slug='sistema-para-padaria',
            client_name='Padaria Pão Quente',
            segment='Alimentação',
            challenge='Controle manual de pedidos.',
            solution='Sistema web para gestão dos pedidos.',
            results='Atendimento mais rápido.',
            testimonial='O sistema facilitou muito nossa rotina.',
            testimonial_author='João Silva',
            visible=True,
        )

        response = self.client.get(case.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sistema para Padaria')
        self.assertContains(response, 'Padaria Pão Quente')

    def test_about_page_loads(self):
        response = self.client.get('/sobre/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Desenvolvedores focados em soluções reais')

    def test_laboratory_page_loads(self):
        response = self.client.get('/laboratorio/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projetos em andamento, ideias em evolução')
