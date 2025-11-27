from django.core.management.base import BaseCommand
from sacco_users.models import SaccoUser

class Command(BaseCommand):
    help = 'Create admin users'

    def handle(self, *args, **options):
        # Create Admin1
        if not SaccoUser.objects.filter(username='Admin1').exists():
            admin1 = SaccoUser.objects.create_superuser(
                username='Admin1',
                email='county@gmail.com',
                password='AdminPass123',
                id_number='ADMIN001',
                first_name='Admin',
                last_name='One'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin Admin1'))
        else:
            self.stdout.write(self.style.WARNING('Admin1 already exists'))

        # Create Admin2
        if not SaccoUser.objects.filter(username='Admin2').exists():
            admin2 = SaccoUser.objects.create_superuser(
                username='Admin2',
                email='county@gmail.com',
                password='AdminPass123',
                id_number='ADMIN002',
                first_name='Admin',
                last_name='Two'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created admin Admin2'))
        else:
            self.stdout.write(self.style.WARNING('Admin2 already exists'))
