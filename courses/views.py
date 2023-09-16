from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework import status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters

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



class ArticleFilter(django_filters.FilterSet):
    tags = django_filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags',
        to_field_name='name',
        conjoined=True
    )

    class Meta:
        model = Article
        fields = ['tags']

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__name__in=value)

    @property
    def qs(self):
        qs = super().qs
        if self.form.cleaned_data['tags']:
            qs = self.filter_tags(qs, 'tags', self.form.cleaned_data['tags'])
        return qs
    

class ArticleViewset(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tags', 'category__title']
    search_fields = ['translations__title']
    
    def create(self, request, *args, **kwargs):

        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            instance = serializer.save()
            instance.create_translation('ar', title=request.data['title_ar'],
                                        content= request.data['content_ar'])
            instance.create_translation('en', title=request.data['title_en'],
                                        content= request.data['content_en'])
            instance.create_translation('fr', title=request.data['title_fr'],
                                        content= request.data['content_fr'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class CommentViewSet(viewsets.ModelViewSet):
    queryset = ArticleComment.objects.all()
    serializer_class = CommentSerializer



class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer