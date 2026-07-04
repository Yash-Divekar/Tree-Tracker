from django.contrib import admin
from .models import *
# Register your models here.
class display_list(admin.ModelAdmin):
    list_display = ('species' , 'latitude' , 'longitude' ,  'tree_height', 'spreading', 'trunk_damage')
    
    list_filter = ['species', 'spreading']
    search_fields = ['species', 'spreading']
    
admin.site.register(Survey , display_list)