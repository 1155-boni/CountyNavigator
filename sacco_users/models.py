from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
import qrcode
from io import BytesIO

class SaccoUser(AbstractUser):
    # Personal Information
    middle_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    id_number = models.CharField(max_length=20, unique=True)
    membership_number = models.CharField(max_length=20, blank=True)
    county = models.CharField(max_length=50, blank=True)
    sub_county = models.CharField(max_length=50, blank=True)
    ward = models.CharField(max_length=50, blank=True)
    stage = models.CharField(max_length=50, blank=True)

    # Next of Kin
    next_of_kin_first_name = models.CharField(max_length=30, blank=True)
    next_of_kin_last_name = models.CharField(max_length=30, blank=True)
    next_of_kin_id_number = models.CharField(max_length=20, blank=True)
    next_of_kin_phone = models.CharField(max_length=15, blank=True)

    # Work Information
    stage_chairman_first_name = models.CharField(max_length=30, blank=True)
    stage_chairman_last_name = models.CharField(max_length=30, blank=True)
    stage_chairman_phone = models.CharField(max_length=15, blank=True)
    ward_chairman_first_name = models.CharField(max_length=30, blank=True)
    ward_chairman_last_name = models.CharField(max_length=30, blank=True)
    ward_chairman_phone = models.CharField(max_length=15, blank=True)
    sub_county_chairman_first_name = models.CharField(max_length=30, blank=True)
    sub_county_chairman_last_name = models.CharField(max_length=30, blank=True)
    sub_county_chairman_phone = models.CharField(max_length=15, blank=True)

    # Motor Bike Information
    motor_bike_model = models.CharField(max_length=50, blank=True)
    motor_bike_registration_number = models.CharField(max_length=20, blank=True)
    motor_bike_color = models.CharField(max_length=20, blank=True)

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
