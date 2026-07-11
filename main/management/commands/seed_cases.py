from django.core.management.base import BaseCommand

from main.models import CaseStudy, Technology


class Command(BaseCommand):
    help = 'Popula o banco com casos de exemplo para demonstração'

    def handle(self, *args, **options):
        # Criar tecnologias se não existirem
        django, _ = Technology.objects.get_or_create(name='Django', defaults={'color': '#092e20'})
        postgresql, _ = Technology.objects.get_or_create(name='PostgreSQL', defaults={'color': '#336791'})
        docker, _ = Technology.objects.get_or_create(name='Docker', defaults={'color': '#2496ed'})
        tailwind, _ = Technology.objects.get_or_create(name='Tailwind CSS', defaults={'color': '#38b2ac'})
        kotlin, _ = Technology.objects.get_or_create(name='Kotlin', defaults={'color': '#7f52ff'})

        # Criar casos de exemplo
        cases = [
            {
                'title': 'Sistema para Padaria Pão Quente',
                'client_name': 'Padaria Pão Quente',
                'segment': 'Alimentação',
                'challenge': 'A padaria realizava o controle de pedidos manualmente, utilizando papel.\n\nIsso gerava:\n- demora no atendimento\n- perda de pedidos\n- dificuldade para acompanhar vendas',
                'solution': 'A KVN Tech desenvolveu um sistema web com:\n- Cadastro de produtos\n- Controle de pedidos\n- Painel administrativo\n- Histórico de vendas\n- Relatórios',
                'results': '✔ Atendimento mais rápido\n✔ Redução de erros\n✔ Organização dos pedidos\n✔ Melhor controle do estoque',
                'testimonial': 'O sistema facilitou muito nossa rotina. Agora consigo acompanhar todos os pedidos em tempo real.',
                'testimonial_author': 'João Silva, proprietário',
                'gallery_description': 'Imagens do painel administrativo, tela de pedidos, relatórios de vendas.',
                'visible': True,
                'featured': True,
                'technologies': [django, postgresql, docker, tailwind],
            },
            {
                'title': 'App Mobile para Consultório Médico',
                'client_name': 'Consultório Médico Saúde Plus',
                'segment': 'Saúde',
                'challenge': 'O consultório recebia muitas ligações para agendamento e tinha dificuldade em gerenciar as filas de espera.\n\nProblemas:\n- ausências de pacientes\n- agendamentos duplicados\n- comunicação desorganizada',
                'solution': 'Desenvolvemos um aplicativo mobile que permite:\n- Agendamento de consultas via app\n- Notificações automáticas de confirmação\n- Histórico de consultas\n- Teleconsulta integrada',
                'results': '✔ Redução de 40% em faltas\n✔ Melhor organização de agenda\n✔ Comunicação padronizada\n✔ Satisfação do paciente aumentada',
                'testimonial': 'O aplicativo revolucionou nosso fluxo de atendimento. Os pacientes agora confirmam presença automaticamente.',
                'testimonial_author': 'Dra. Maria Santos, gerente',
                'gallery_description': 'Telas do aplicativo mobile, histórico de pacientes, notificações em tempo real.',
                'visible': True,
                'featured': True,
                'technologies': [kotlin, docker],
            },
            {
                'title': 'Plataforma de E-commerce para Loja Online',
                'client_name': 'Loja Moda Trend',
                'segment': 'Varejo',
                'challenge': 'A loja vendia apenas presencialmente e queria expandir para o digital.\n\nNecessidade:\n- plataforma de vendas online\n- integração com estoque\n- pagamento seguro\n- gestão de pedidos',
                'solution': 'Criamos uma plataforma completa com:\n- Catálogo de produtos responsivo\n- Carrinho de compras inteligente\n- Integração com gateway de pagamento\n- Painel de gestão de pedidos\n- Relatórios de vendas',
                'results': '✔ Aumento de 300% em vendas no primeiro mês\n✔ Redução de erros em processamento\n✔ Melhor acompanhamento de pedidos\n✔ Expansão para novos mercados',
                'testimonial': 'Ultrapassamos nossas expectativas. A plataforma é intuitiva e os clientes adoram.',
                'testimonial_author': 'Carlos Mendes, proprietário',
                'gallery_description': 'Página inicial da loja, catálogo de produtos, checkout, painel administrativo.',
                'visible': True,
                'featured': False,
                'technologies': [django, postgresql, docker, tailwind],
            },
        ]

        for case_data in cases:
            techs = case_data.pop('technologies')
            case, created = CaseStudy.objects.get_or_create(
                title=case_data['title'],
                defaults=case_data
            )
            case.technologies.set(techs)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Case criado: {case.title}'))
            else:
                self.stdout.write(f'• Case já existe: {case.title}')

        self.stdout.write(self.style.SUCCESS('\n✅ Seed de cases concluído com sucesso!'))
