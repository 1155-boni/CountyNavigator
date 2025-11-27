import os
import django
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CountyNavigator.settings')
django.setup()

User = get_user_model()

def test_delete_user():
    # Create test users
    admin, created = User.objects.get_or_create(
        username='AdminDelete',
        defaults={'email': 'admin@delete.com', 'id_number': 'ADMINDEL', 'first_name': 'Admin', 'last_name': 'Delete'}
    )
    admin.set_password('AdminPass123')
    admin.is_superuser = True
    admin.save()

    # Create a regular user to delete
    user_to_delete, created = User.objects.get_or_create(
        username='user_to_delete',
        defaults={'email': 'delete@example.com', 'id_number': 'DEL001', 'first_name': 'To', 'last_name': 'Delete'}
    )
    user_to_delete.set_password('pass123')
    user_to_delete.save()

    # Create another regular user
    regular_user, created = User.objects.get_or_create(
        username='regular_delete',
        defaults={'email': 'regular@delete.com', 'id_number': 'REGDEL', 'first_name': 'Regular', 'last_name': 'Delete'}
    )
    regular_user.set_password('pass123')
    regular_user.save()

    client = Client()

    print("=== Testing Delete User Functionality ===")

    # Test 1: Admin login
    login_response = client.post('/sacco_users/login/', {'username': 'AdminDelete', 'password': 'AdminPass123'})
    print(f"Admin login status: {login_response.status_code}")
    assert login_response.status_code == 302, "Admin should be able to login"

    # Test 2: Access dashboard and check delete button is present
    dashboard_response = client.get('/sacco_users/dashboard/')
    print(f"Dashboard access status: {dashboard_response.status_code}")
    content = dashboard_response.content.decode()
    assert 'Delete' in content, "Delete button should be present in dashboard"
    assert 'user_to_delete' in content, "User to delete should be in dashboard"
    print("✓ Delete button present in dashboard")

    # Test 3: Access delete confirmation page
    delete_page_response = client.get(f'/sacco_users/delete-user/{user_to_delete.id}/')
    print(f"Delete page access status: {delete_page_response.status_code}")
    delete_content = delete_page_response.content.decode()
    assert 'Are you sure you want to delete this user?' in delete_content, "Confirmation message should be present"
    assert 'user_to_delete' in delete_content, "User name should be in confirmation page"
    print("✓ Delete confirmation page accessible")

    # Test 4: Confirm deletion
    delete_response = client.post(f'/sacco_users/delete-user/{user_to_delete.id}/')
    print(f"Delete POST status: {delete_response.status_code}")
    assert delete_response.status_code == 302, "Delete should redirect after success"

    # Check if user was actually deleted
    try:
        deleted_user = User.objects.get(id=user_to_delete.id)
        assert False, "User should have been deleted"
    except User.DoesNotExist:
        print("✓ User successfully deleted from database")

    # Test 5: Check redirect to dashboard after deletion
    assert delete_response.url == '/sacco_users/dashboard/', "Should redirect to dashboard"
    dashboard_after_delete = client.get('/sacco_users/dashboard/')
    content_after = dashboard_after_delete.content.decode()
    assert 'user_to_delete' not in content_after, "Deleted user should not appear in dashboard"
    assert 'User deleted successfully' in content_after, "Success message should be shown"
    print("✓ Redirect to dashboard with success message")

    # Test 6: Try to access delete page for non-existent user
    nonexistent_response = client.get('/sacco_users/delete-user/99999/')
    print(f"Non-existent user delete page status: {nonexistent_response.status_code}")
    assert nonexistent_response.status_code == 404, "Should return 404 for non-existent user"
    print("✓ 404 for non-existent user")

    # Test 7: Regular user cannot access delete
    client.logout()
    login_response = client.post('/sacco_users/login/', {'username': 'regular_delete', 'password': 'pass123'})
    assert login_response.status_code == 302, "Regular user login should work"

    delete_attempt = client.get(f'/sacco_users/delete-user/{regular_user.id}/')
    print(f"Regular user delete access status: {delete_attempt.status_code}")
    assert delete_attempt.status_code == 302, "Regular user should be redirected (no access)"
    print("✓ Regular user cannot access delete functionality")

    # Test 8: Test API delete endpoint still works
    client.logout()
    login_response = client.post('/sacco_users/login/', {'username': 'AdminDelete', 'password': 'AdminPass123'})
    assert login_response.status_code == 302, "Admin login for API test"

    # Create another user for API test
    api_user, created = User.objects.get_or_create(
        username='api_delete_user',
        defaults={'email': 'api@delete.com', 'id_number': 'APIDEL', 'first_name': 'API', 'last_name': 'Delete'}
    )
    api_user.set_password('pass123')
    api_user.save()

    # Get token for API
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(admin)
    token = str(refresh.access_token)

    import requests
    headers = {'Authorization': f'Bearer {token}'}
    api_delete_response = requests.delete(f'http://127.0.0.1:8000/sacco_users/api/users/{api_user.id}/', headers=headers)
    print(f"API delete status: {api_delete_response.status_code}")
    assert api_delete_response.status_code == 204, "API delete should return 204"
    print("✓ API delete endpoint still works")

    print("\n=== All Delete User Tests Passed! ===")

if __name__ == '__main__':
    test_delete_user()
