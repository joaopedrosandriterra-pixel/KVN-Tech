import os
from unittest.mock import patch

from django.test import TestCase

from kvntech import settings as project_settings


class PageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Transformo ideias em realidade')
        self.assertContains(response, 'href="/sobre/"')
        self.assertContains(response, 'href="/laboratorio/"')

    def test_about_page_loads(self):
        response = self.client.get('/sobre/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Desenvolvedor focado em soluções reais')

    def test_laboratory_page_loads(self):
        response = self.client.get('/laboratorio/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projetos em andamento, ideias em evolução')
