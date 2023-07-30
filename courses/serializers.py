# serializers.py
from rest_framework import serializers
from .models import Course, Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    courses_count = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'title', 'parent', 'children']

    def get_children(self, obj):
        children_qs = obj.children.all()
        serializer = self.__class__(children_qs, many=True)
        return serializer.data
    
    def get_courses_count(self, obj):
        return obj.num_courses
    

class CourseSerializer(serializers.ModelSerializer):
    
    def duration(self, obj):
        return f'{obj.get_duration}'

    def get_total_students(self, obj):
        return f'{obj.get_total_students}'

    def get_total_lessons(self, obj):
        return obj.get_lessons

    def get_total_course_reviews(self, obj):
        return obj.get_course_reviews
    

    get_duration = serializers.SerializerMethodField(method_name='duration')
    get_total_students = serializers.SerializerMethodField(method_name='duration')
    get_total_lessons = serializers.SerializerMethodField(method_name='duration')
    class Meta:
        model = Course
        fields = '__all__'
        

