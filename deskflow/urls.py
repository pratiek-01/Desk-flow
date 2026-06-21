from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # Django's built-in admin panel
    path('', include('core.urls')),    # our app's urls
]
