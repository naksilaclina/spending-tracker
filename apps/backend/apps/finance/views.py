from apps.core.views import UserOwnedModelViewSet
from apps.finance.models import Category, Template
from apps.finance.serializers import CategorySerializer, TemplateSerializer


class CategoryViewSet(UserOwnedModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TemplateViewSet(UserOwnedModelViewSet):
    queryset = Template.objects.select_related("category")
    serializer_class = TemplateSerializer
