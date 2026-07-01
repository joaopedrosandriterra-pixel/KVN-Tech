from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Project, RoadmapItem, Technology


class LaboratoryTests(TestCase):
    def setUp(self):
        django, _ = Technology.objects.get_or_create(name='Django')
        self.project = Project.objects.create(
            title='Sistema de Gestão',
            short_description='Sistema empresarial com método documentado.',
            full_description='Projeto vivo com roadmap, diário e tecnologias.',
            status=Project.Status.DEVELOPMENT,
            progress=70,
            visible=True,
        )
        self.project.technologies.add(django)
        RoadmapItem.objects.create(
            project=self.project,
            title='Backend',
            description='Criando API.',
            status=RoadmapItem.Status.DONE,
            order=1,
        )

    def test_laboratory_lists_visible_projects(self):
        Project.objects.create(
            title='Projeto oculto',
            short_description='Nao deve aparecer.',
            full_description='Privado.',
            visible=False,
        )

        response = self.client.get(reverse('laboratory'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sistema de Gestão')
        self.assertContains(response, '70%')
        self.assertContains(response, 'Django')
        self.assertNotContains(response, 'Projeto oculto')

    def test_project_detail_shows_roadmap_and_stats(self):
        response = self.client.get(self.project.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Projeto vivo com roadmap')
        self.assertContains(response, 'Backend')
        self.assertContains(response, '1/1')

    def test_panel_requires_staff_user(self):
        response = self.client.get(reverse('panel'))
        self.assertEqual(response.status_code, 302)

        User.objects.create_user(username='client', password='StrongPass123!')
        self.client.login(username='client', password='StrongPass123!')
        response = self.client.get(reverse('panel'))
        self.assertEqual(response.status_code, 302)

        staff = User.objects.create_user(username='staff', password='StrongPass123!', is_staff=True)
        self.client.force_login(staff)
        response = self.client.get(reverse('panel'))
        self.assertEqual(response.status_code, 200)
