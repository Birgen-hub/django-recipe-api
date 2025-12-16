from rest_framework import viewsets, permissions, authentication
from .models import InventoryItem
from .serializers import InventoryItemSerializer

class InventoryItemViewSet(viewsets.ModelViewSet):
    serializer_class = InventoryItemSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(user=self.request.user).select_related('ingredient').order_by('ingredient__name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
