import requests
from bs4 import BeautifulSoup

# Test valid login
url = 'http://127.0.0.1:8000/sacco_users/login/'
data = {'id_number': 'countynavi@2025', 'password': 'mwascaras'}
response = requests.post(url, data=data, allow_redirects=False)

print(f"Valid login status code: {response.status_code}")
if response.status_code == 302:
    print("Redirected to dashboard - Login successful")
elif response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    error = soup.find('div', class_='alert-danger')
    if error:
        print(f"Error message: {error.text.strip()}")
    else:
        print("No error message found")
else:
    print(f"Unexpected status code: {response.status_code}")

# Test invalid login
data_invalid = {'id_number': 'invalid', 'password': 'wrong'}
response_invalid = requests.post(url, data=data_invalid, allow_redirects=False)

print(f"\nInvalid login status code: {response_invalid.status_code}")
if response_invalid.status_code == 200:
    soup = BeautifulSoup(response_invalid.text, 'html.parser')
    error = soup.find('div', class_='alert-danger')
    if error:
        print(f"Error message: {error.text.strip()}")
    else:
        print("No error message found")
else:
    print(f"Unexpected status code: {response_invalid.status_code}")
