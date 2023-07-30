from rest_framework import viewsets
from .serializers import *
from rest_framework import status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields =['is_online', 'course_type', 'price', 'categories__title']
    search_fields = ['title', 'description']
    def get_queryset(self):
        queryset = self.queryset
        keywords = self.request.query_params.get('keywords', None)
        if keywords is not None:
            queryset = queryset.filter(keywords__icontains=keywords)
        return queryset


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'description']