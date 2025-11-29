from django.core.management.base import BaseCommand
from sacco_users.models import SaccoUser

class Command(BaseCommand):
    help = 'Regenerate QR codes for all users using Cloudinary'

    def handle(self, *args, **options):
        users = SaccoUser.objects.all()
        for user in users:
            self.stdout.write(f'Regenerating QR code for user {user.id}: {user.first_name} {user.last_name}')
            user.generate_qr_code()
            user.save()
        self.stdout.write(self.style.SUCCESS('Successfully regenerated QR codes for all users'))
