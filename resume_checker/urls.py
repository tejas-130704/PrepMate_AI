from django.urls import path
from . import views
urlpatterns = [
    path("",views.resume_home,name="resume"),
    path("getResume_data/",views.getResume_data,name="getResume_data"), 
]
