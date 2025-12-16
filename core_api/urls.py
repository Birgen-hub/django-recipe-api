from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/auth/', include('knox.urls')),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/recipes/', include('recipes.urls')),
    path('api/v1/inventory/', include('inventory.urls')),
]
