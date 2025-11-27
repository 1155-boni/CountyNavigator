import os
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CountyNavigator.settings')
django.setup()

User = get_user_model()

def test_dashboard():
    # Create test users
    admin1, created = User.objects.get_or_create(
        username='Admin1',
        defaults={'email': 'county@gmail.com', 'id_number': 'ADMIN001', 'first_name': 'Admin', 'last_name': 'One'}
    )
    admin1.set_password('AdminPass123')
    admin1.is_superuser = True
    admin1.save()

    admin2, created = User.objects.get_or_create(
        username='Admin2',
        defaults={'email': 'county@gmail.com', 'id_number': 'ADMIN002', 'first_name': 'Admin', 'last_name': 'Two'}
    )
    admin2.set_password('AdminPass123')
    admin2.is_superuser = True
    admin2.save()

    # Create a regular user
    regular_user, created = User.objects.get_or_create(
        username='regular',
        defaults={'email': 'regular@example.com', 'id_number': 'REG001', 'first_name': 'Regular', 'last_name': 'User'}
    )
    regular_user.set_password('pass123')
    regular_user.save()

    client = Client()

    # Test admin1 login and dashboard
    login_response = client.post('/login/', {'username': 'Admin1', 'password': 'AdminPass123'})
    print(f"Admin1 login status: {login_response.status_code}")

    dashboard_response = client.get('/dashboard/')
    print(f"Admin1 dashboard status: {dashboard_response.status_code}")
    content = dashboard_response.content.decode()
    print("Admin1 sees Admin2 in dashboard:", 'Admin2' in content)
    print("Admin1 sees regular user in dashboard:", 'regular' in content)

    # Test admin2 login and dashboard
    client.logout()
    login_response = client.post('/login/', {'username': 'Admin2', 'password': 'AdminPass123'})
    print(f"Admin2 login status: {login_response.status_code}")

    dashboard_response = client.get('/dashboard/')
    print(f"Admin2 dashboard status: {dashboard_response.status_code}")
    content = dashboard_response.content.decode()
    print("Admin2 sees Admin1 in dashboard:", 'Admin1' in content)
    print("Admin2 sees regular user in dashboard:", 'regular' in content)

    # Test regular user login and dashboard
    client.logout()
    login_response = client.post('/login/', {'username': 'regular', 'password': 'pass123'})
    print(f"Regular user login status: {login_response.status_code}")

    dashboard_response = client.get('/dashboard/')
    print(f"Regular user dashboard status: {dashboard_response.status_code}")
    content = dashboard_response.content.decode()
    print("Regular user sees Admin1 in dashboard:", 'Admin1' in content)
    print("Regular user sees Admin2 in dashboard:", 'Admin2' in content)
    print("Regular user sees self in dashboard:", 'regular' in content)

if __name__ == '__main__':
    test_dashboard()
