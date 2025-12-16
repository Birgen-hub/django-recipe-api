from rest_framework import serializers
from .models import InventoryItem
from recipes.serializers import IngredientSerializer

class InventoryItemSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(read_only=True)
    ingredient_id = serializers.PrimaryKeyRelatedField(
        queryset=InventoryItem.ingredient.field.related_model.objects.all(),
        source='ingredient',
        write_only=True
    )
    
    class Meta:
        model = InventoryItem
        fields = ('id', 'ingredient', 'ingredient_id', 'quantity', 'unit')
        read_only_fields = ('id', 'ingredient')
        
    def validate(self, data):
        user = self.context['request'].user
        ingredient = data.get('ingredient')
        
        if self.instance:
            qs = InventoryItem.objects.filter(user=user, ingredient=ingredient).exclude(pk=self.instance.pk)
        else:
            qs = InventoryItem.objects.filter(user=user, ingredient=ingredient)
            
        if qs.exists():
            raise serializers.ValidationError("This ingredient is already in your inventory.")
        
        return data
