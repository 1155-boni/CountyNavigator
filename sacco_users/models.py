from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO

class SaccoUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    id_number = models.CharField(max_length=20, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='sacco_users',
        related_query_name='sacco_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='sacco_users',
        related_query_name='sacco_user',
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def generate_qr_code(self):
        # Generate QR code image pointing to /users/<id>
        url = f"/users/{self.id}/"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        self.qr_code.save(f'qr_{self.id}.png', ContentFile(buffer.getvalue()), save=False)
