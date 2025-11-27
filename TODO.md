# TODO: Implement QR Scanner for Easy Access

## Tasks:
- [x] Add URL for scan view in sacco_users/urls.py
- [x] Implement QR scanner in templates/scan.html using Instascan library
- [x] Add "Scan QR" button in templates/dashboard.html
- [x] Modify scan_view in sacco_users/views.py to handle POST requests and redirect to user profile
- [x] Add option for scanning QR code from uploaded image file
- [ ] Test the scanner functionality

# TODO: Add Delete User Feature

## Tasks:
- [ ] Add delete_user_view in sacco_users/views.py
- [ ] Add URL path for delete-user/<int:pk>/ in sacco_users/urls.py
- [ ] Add Delete button in templates/dashboard.html with confirmation
- [ ] Test delete functionality
