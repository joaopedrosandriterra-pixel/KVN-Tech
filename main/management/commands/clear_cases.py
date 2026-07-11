from django.core.management.base import BaseCommand

from main.models import CaseStudy


class Command(BaseCommand):
    help = 'Remove todos os casos cadastrados'

    def handle(self, *args, **options):
        count, _ = CaseStudy.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(f'✅ {count} casos removidos com sucesso!'))
