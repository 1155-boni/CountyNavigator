# TODO: Fix Login Not Directing to Dashboard

## Completed Tasks
- [x] Analyzed login view and identified incorrect redirect URL name
- [x] Updated login_view in sacco_users/views.py to redirect to 'sacco_users:dashboard' instead of 'dashboard'
- [x] Updated test_dashboard.py to use correct URLs (/sacco_users/login/ and /sacco_users/dashboard/) and login data ('id_number' instead of 'username')

## Next Steps
- [ ] Test the login functionality to ensure it now redirects to dashboard
- [ ] Run the updated tests to verify they pass
- [ ] If issues persist, check for any other URL mismatches in the codebase
