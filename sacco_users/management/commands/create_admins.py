from django.core.management.base import BaseCommand
from sacco_users.models import SaccoUser

class Command(BaseCommand):
    help = 'Create admin users'

    def handle(self, *args, **options):
        # Create main admin
        if not SaccoUser.objects.filter(id_number='countynavi@2025').exists():
            admin = SaccoUser.objects.create_superuser(
                id_number='countynavi@2025',
                email='countynavigators@gmail.com',
                password='mwascaras',
                first_name='County',
                last_name='Navigator'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin user'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
