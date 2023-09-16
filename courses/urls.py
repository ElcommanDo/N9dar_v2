from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('categories', CategoryViewSet)
router.register('courses', CourseViewSet)
router.register('Article', ArticleViewset)

router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'replies', ReplyViewSet, basename='reply')


urlpatterns = [
   
    path('', include(router.urls)),
    

]

