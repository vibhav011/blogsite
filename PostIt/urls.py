from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('temporaryPage1/', views.signuprequest, name='signuprequest'),
    path('temporaryPage2/', views.loginrequest, name='loginrequest'),
    path('blogs/<int:blogid>/', views.showBlog, name='blogs'),
    path('create-blog', views.createBlog, name='createblog'),
]
