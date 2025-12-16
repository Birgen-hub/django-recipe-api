from django.contrib import admin
from .models import Tag, Ingredient, Recipe

admin.site.register(Tag)
admin.site.register(Ingredient)

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_minutes', 'price',)
    filter_horizontal = ('tags', 'ingredients',)
