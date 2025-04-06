from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="coding"),
    path("question/<int:question_id>",views.question,name="question"),
    path("question/run_code/",views.run_code,name="run_code"),
]
