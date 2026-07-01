from datetime import date

from django.db import migrations


def seed_projects(apps, schema_editor):
    Technology = apps.get_model('main', 'Technology')
    Project = apps.get_model('main', 'Project')
    RoadmapItem = apps.get_model('main', 'RoadmapItem')
    ProjectUpdate = apps.get_model('main', 'ProjectUpdate')

    techs = {}
    for name, color in [
        ('Django', '#22d3ee'),
        ('PostgreSQL', '#38bdf8'),
        ('Docker', '#60a5fa'),
        ('React', '#67e8f9'),
        ('Roblox', '#f87171'),
        ('Lua', '#a78bfa'),
    ]:
        techs[name], _ = Technology.objects.get_or_create(name=name, defaults={'color': color})

    nexus, _ = Project.objects.get_or_create(
        slug='nexus-erp',
        defaults={
            'title': 'Nexus ERP',
            'short_description': 'Sistema empresarial em Django com login, dashboard, PostgreSQL e fluxo de deploy documentado.',
            'full_description': 'Este sistema está sendo construído com Django, PostgreSQL e Docker. O processo documenta planejamento, autenticação, dashboard, API e deploy para demonstrar como um produto real evolui do zero até a entrega.',
            'status': 'development',
            'progress': 80,
            'visible': True,
            'featured': True,
        },
    )
    nexus.technologies.set([techs['Django'], techs['PostgreSQL'], techs['Docker'], techs['React']])

    for order, title, description, status in [
        (1, 'Planejamento', 'Escopo, telas principais e estrutura de dados.', 'done'),
        (2, 'Backend', 'Models, autenticação e regras principais.', 'done'),
        (3, 'Dashboard', 'Primeiras telas internas do sistema.', 'in_progress'),
        (4, 'Deploy', 'Publicação e ajustes finais de produção.', 'pending'),
    ]:
        RoadmapItem.objects.get_or_create(
            project=nexus,
            title=title,
            defaults={'description': description, 'status': status, 'order': order},
        )

    for created_at, title, content in [
        (date(2026, 6, 30), 'Sistema de login implementado', 'Autenticação, cadastro e ativação de conta foram organizados para dar base ao painel.'),
        (date(2026, 7, 1), 'PostgreSQL conectado', 'Ambiente com banco relacional e Docker preparado para evolução do projeto.'),
    ]:
        ProjectUpdate.objects.get_or_create(
            project=nexus,
            title=title,
            defaults={'content': content, 'created_at': created_at},
        )

    combat, _ = Project.objects.get_or_create(
        slug='combate-roblox',
        defaults={
            'title': 'Combate Roblox',
            'short_description': 'Sistema de combate com estados, feedback visual, balanceamento e evolução por etapas.',
            'full_description': 'Experiência interativa em Roblox focada em combate responsivo, organização de scripts, feedback de interface e testes incrementais. O roadmap mostra o processo de construção antes da versão final.',
            'status': 'beta',
            'progress': 60,
            'visible': True,
            'featured': False,
        },
    )
    combat.technologies.set([techs['Roblox'], techs['Lua']])

    for order, title, description, status in [
        (1, 'Protótipo', 'Movimentos e primeiro fluxo de ataque.', 'done'),
        (2, 'Sistema de dano', 'Regras de hitbox e estados de personagem.', 'done'),
        (3, 'Interface', 'Feedback visual para vida, combo e recarga.', 'in_progress'),
        (4, 'Balanceamento', 'Ajustes finos depois dos testes.', 'pending'),
    ]:
        RoadmapItem.objects.get_or_create(
            project=combat,
            title=title,
            defaults={'description': description, 'status': status, 'order': order},
        )

    ProjectUpdate.objects.get_or_create(
        project=combat,
        title='Protótipo jogável',
        defaults={
            'content': 'Primeira versão funcional com ataque básico, detecção de colisão e organização dos módulos.',
            'created_at': date(2026, 7, 1),
        },
    )


def unseed_projects(apps, schema_editor):
    Project = apps.get_model('main', 'Project')
    Project.objects.filter(slug__in=['nexus-erp', 'combate-roblox']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_projects, unseed_projects),
    ]
