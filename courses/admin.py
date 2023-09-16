from django.contrib import admin
from .models import *
from parler.admin import TranslatableAdmin
# Register your models here.

admin.site.register([Course, Tag, Category])

@admin.register(Article)
class WeekAdmin(TranslatableAdmin):
   
   pass
