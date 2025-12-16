from django.db import models
from django.conf import settings
from recipes.models import Ingredient

class InventoryItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='inventory_items',
    )
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=50, blank=True)
    
    class Meta:
        unique_together = ('user', 'ingredient')
        verbose_name = 'Inventory Item'
        verbose_name_plural = 'Inventory Items'

    def __str__(self):
        return f'{self.ingredient.name} ({self.quantity} {self.unit})'
