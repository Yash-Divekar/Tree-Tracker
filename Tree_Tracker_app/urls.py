from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='Home'),
    path('add/',views.add,name='add'),
    path('species/',views.species,name='species'),
    path('survey_pdf',views.survey_pdf,name='survey_pdf'),
]