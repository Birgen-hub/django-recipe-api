from rest_framework import serializers

from core_api.settings import AUTH_USER_MODEL
from .models import Tag, Ingredient, Recipe

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""
    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""
    class Meta:
        model = Ingredient
        fields = ('id', 'name')
        read_only_fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""
    # Note: Tags and Ingredients are read-only here, only showing their IDs.
    # The detail serializer will expand them.
    class Meta:
        model = Recipe
        fields = ('id', 'title', 'time_minutes', 'price', 'link')
        read_only_fields = ('id',)


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for a recipe detail view"""
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ('description', 'tags', 'ingredients')

class RecipeImageSerializer(serializers.Serializer):
    """Serializer for uploading images to recipes"""
    image = serializers.ImageField(required=True)
