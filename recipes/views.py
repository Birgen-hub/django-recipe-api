from rest_framework import viewsets, mixins, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeReadSerializer, RecipeWriteSerializer

class BaseRecipeAttrViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TagViewSet(BaseRecipeAttrViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class IngredientViewSet(BaseRecipeAttrViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def _params_to_ints(self, qs):
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user).order_by('-id')
        
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids).distinct()
        
        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids).distinct()

        return queryset.prefetch_related('tags', 'ingredients')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
