from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet

router = DefaultRouter()
router.register('items', InventoryItemViewSet, basename='inventory-item')

app_name = 'inventory'

urlpatterns = [
    path('', include(router.urls)),
]
