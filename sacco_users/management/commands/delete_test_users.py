from django.core.management.base import BaseCommand
from sacco_users.models import SaccoUser

class Command(BaseCommand):
    help = 'Delete test users'

    def handle(self, *args, **options):
        test_id_numbers = ['ADMIN001', 'ADMIN002', 'REG001', '12345678']  # id_numbers from test files
        deleted_count = 0
        for id_number in test_id_numbers:
            try:
                user = SaccoUser.objects.get(id_number=id_number)
                user.delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted test user with id_number {id_number}'))
                deleted_count += 1
            except SaccoUser.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Test user with id_number {id_number} does not exist'))
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_count} test users'))
