# store_project/urls.py
from django.contrib import admin
from django.urls import path, include
from catalog import views as catalog_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), 
    path('register/', catalog_views.register, name='register'),
    
    # Add the home route here:
    path('', catalog_views.store_home, name='home'),
]