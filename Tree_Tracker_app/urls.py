from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index,name='Home'),
    path('add',views.add,name='add'),
    path('fake',views.facker,name='faker'),
    path('survey_pdf',views.survey_pdf,name='survey_pdf'),
    path('map1' , views.map1 , name='map1')
]