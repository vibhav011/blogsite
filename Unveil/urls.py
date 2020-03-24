from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup, name='signup'),
    path('temporary-page1/', views.signuprequest, name='signuprequest'),
    path('temporary-page2/', views.loginrequest, name='loginrequest'),
    path('blogs/<int:blogid>/', views.showBlog, name='blogs'),
    path('create-blog', views.createBlog, name='createblog'),
    path('ajax/create-blog-request', views.createBlogRequest, name='createblogrequest'),
    path('editblog/<int:blogid>/', views.editBlog, name='editblog'),
    path('ajax/edit-blog-request', views.editBlogRequest, name='editblogrequest'),
    path('ajax/delete-blog-request', views.deleteBlogRequest, name='deleteblogrequest'),
]
