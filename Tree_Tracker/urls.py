from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Tree_Tracker_app.urls'),name='Tree_Tracker_app')
]
