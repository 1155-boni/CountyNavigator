"""
URL configuration for CountyNavigator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.static import serve
from django.shortcuts import redirect
from pathlib import Path
from sacco_users.views import login_view, dashboard_view

BASE_DIR = Path(__file__).resolve().parent.parent

urlpatterns = [
    path('', login_view, name='home'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('sacco_users/', include('sacco_users.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=str(BASE_DIR / "static"))
    # serve any .well-known requests from static/.well-known
    urlpatterns += [
        path('.well-known/<path:path>', serve, {'document_root': str(BASE_DIR / 'static' / '.well-known')}),
        path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': str(BASE_DIR / 'static')}),
    ]
