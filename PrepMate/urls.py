from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('<int:comp_id>/post',views.post,name="post"),
    path('meet/', views.meet,name="meet"),
    path('login/', views.login_view,name="login"),
    path('profile/',views.profile,name="profile"),
    path('register/', views.registration,name="registration"),
    path('logout/', views.logout_view,name="logout"),
    path('position/',views.byPosition,name="position"),
    path('getData/',views.getData,name="getData"),
    path('getAnalysis/',views.getAnalysis,name="getAnalysis"),
    path('company/',views.byCompany,name="company"),
    path('profile/',views.profile,name="profile"),
    path('about/',views.about,name="about"),
    path('getGD/<int:gd_id>',views.getGD,name="getGD"),
    path('analysis/<int:interview_id>', views.everyAnalysis, name="interview_analysis"),
    path('gd/', include('base.urls')),
    path('coding/', include('coding.urls'),name="coding"),
    path('resume/', include('resume_checker.urls'),name="resume"),
    
]