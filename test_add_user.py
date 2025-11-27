import os
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CountyNavigator.settings')
django.setup()

User = get_user_model()

def test_add_user_view():
    client = Client()

    # Test GET request
    response = client.get(reverse('add_user'))
    print(f"GET /add-user/ status: {response.status_code}")
    assert response.status_code == 302  # Redirect to login since not authenticated

    # Create a superuser for testing
    if not User.objects.filter(username='testadmin').exists():
        User.objects.create_superuser('testadmin', 'admin@test.com', 'password123')

    # Login
    client.login(username='testadmin', password='password123')

    # Test GET request after login
    response = client.get(reverse('add_user'))
    print(f"GET /add-user/ after login status: {response.status_code}")
    assert response.status_code == 200

    # Check if form fields are in the response
    content = response.content.decode('utf-8')
    assert 'middle_name' in content
    assert 'membership_number' in content
    assert 'next_of_kin_first_name' in content
    assert 'stage_chairman_first_name' in content
    assert 'motor_bike_model' in content
    print("All new form fields are present in the template.")

    # Test POST request with new fields
    data = {
        'username': 'testuser',
        'first_name': 'John',
        'middle_name': 'Doe',
        'last_name': 'Smith',
        'email': 'john@example.com',
        'phone': '1234567890',
        'id_number': '12345678',
        'membership_number': 'MEM001',
        'county': 'Nairobi',
        'sub_county': 'Westlands',
        'ward': 'Parklands',
        'stage': 'Stage 1',
        'next_of_kin_first_name': 'Jane',
        'next_of_kin_last_name': 'Smith',
        'next_of_kin_id_number': '87654321',
        'next_of_kin_phone': '0987654321',
        'stage_chairman_first_name': 'Chairman',
        'stage_chairman_last_name': 'One',
        'stage_chairman_phone': '1111111111',
        'ward_chairman_first_name': 'Chairman',
        'ward_chairman_last_name': 'Two',
        'ward_chairman_phone': '2222222222',
        'sub_county_chairman_first_name': 'Chairman',
        'sub_county_chairman_last_name': 'Three',
        'sub_county_chairman_phone': '3333333333',
        'motor_bike_model': 'Honda',
        'motor_bike_registration_number': 'KAA 123A',
        'motor_bike_color': 'Blue',
        'password': 'password123'
    }

    response = client.post(reverse('add_user'), data)
    print(f"POST /add-user/ status: {response.status_code}")

    if response.status_code == 302:  # Redirect on success
        print("User created successfully, redirecting to dashboard.")
        # Check if user was created
        user = User.objects.filter(username='testuser').first()
        if user:
            print(f"User created: {user.first_name} {user.middle_name} {user.last_name}")
            print(f"Membership Number: {user.membership_number}")
            print(f"Next of Kin: {user.next_of_kin_first_name} {user.next_of_kin_last_name}")
            print(f"Motor Bike: {user.motor_bike_model} {user.motor_bike_registration_number}")
            # Check QR code
            if user.qr_code:
                print("QR code generated successfully.")
            else:
                print("QR code not generated.")
        else:
            print("User not found in database.")
    else:
        print(f"Error creating user: {response.content.decode('utf-8')}")

if __name__ == '__main__':
    test_add_user_view()
    print("Testing completed.")
