
from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user_auth.urls')),
    path('dashboard/', include('user_dashboard.urls')),
    # ... baaki urls ...
    path('api/', include('core_api.urls')),
    path('', lambda request: redirect('dashboard/')),
]
