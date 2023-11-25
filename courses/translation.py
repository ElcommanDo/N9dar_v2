# yourapp/translation.py

from modeltranslation.translator import translator, TranslationOptions
from .models import Course, Lesson, Article

class CourseTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'objectives', 'curriculum', 'target_audience')

translator.register(Course, CourseTranslationOptions)


class LessonTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(Lesson, LessonTranslationOptions)

class ArticleTranslationOptions(TranslationOptions):
    fields = ('title', 'content')

translator.register(Article, ArticleTranslationOptions)