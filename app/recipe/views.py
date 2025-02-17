"""
Views for the recipe API
"""
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
from . import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for recipe API management"""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated users"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create new recipe"""
        serializer.save(user=self.request.user)


class BaseRecipeAttributeViewSet(
        mixins.DestroyModelMixin,
        mixins.UpdateModelMixin,
        mixins.ListModelMixin,
        viewsets.GenericViewSet
    ):
    """Base view for recipe attributes"""
    autentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class TagViewSet(BaseRecipeAttributeViewSet):
    """Manange tags in the database"""

    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttributeViewSet):
    """manage ingredients in the database"""

    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
