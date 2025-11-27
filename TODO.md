# TODO: Fix 500 Server Error After Login

## Steps to Complete

- [ ] Add namespace 'sacco_users' to the include in CountyNavigator/urls.py
- [ ] Remove duplicate 'login' and 'dashboard' paths from root URLs in CountyNavigator/urls.py
- [ ] Change root 'home' to redirect to namespaced login in CountyNavigator/urls.py
- [ ] Update {% url %} tags in templates/dashboard.html to use 'sacco_users:...'
- [ ] Update {% url %} tags in templates/add_user.html to use 'sacco_users:...'
- [ ] Update {% url %} tags in templates/edit_user.html to use 'sacco_users:...'
- [ ] Update {% url %} tags in templates/delete_user.html to use 'sacco_users:...'
- [ ] Update hardcoded href and {% url %} in templates/base.html to use 'sacco_users:...'
- [ ] Update redirects in sacco_users/views.py to use namespaced URLs
- [ ] Fix test_dashboard.py to use 'id_number' instead of 'username' in POST data
- [ ] Update scan_view redirect in sacco_users/views.py to use reverse for consistency
- [ ] Test the application to ensure login and dashboard work without 500 error
