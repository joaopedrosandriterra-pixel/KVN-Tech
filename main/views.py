from django.shortcuts import render


def home(request):
    projects = [
        {
            'title': 'Sistema Web com Django',
            'summary': 'Painel administrativo, autenticação e fluxo de dados organizado.',
            'tech': ['Django', 'PostgreSQL', 'Docker'],
        },
        {
            'title': 'Automação de processos',
            'summary': 'Scripts e integrações para reduzir esforço manual e ganhar agilidade.',
            'tech': ['Python', 'APIs', 'Linux'],
        },
        {
            'title': 'Experiência em Roblox',
            'summary': 'Sistemas, NPCs, combate e UI com foco em gameplay e performance.',
            'tech': ['Roblox', 'Lua', 'UI'],
        },
    ]

    services = [
        'Sites institucionais e landing pages',
        'Sistemas web e APIs',
        'Aplicativos mobile com Kotlin',
        'Automações, Docker e infraestrutura',
    ]

    return render(request, 'index.html', {'projects': projects, 'services': services})


def about(request):
    return render(request, 'about.html')


def laboratory(request):
    return render(request, 'laboratory.html')
