from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('register/', views.register, name='register'),
    path('todo/', views.home, name='todo'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('delete-task/<str:name>/', views.DeleteTask, name='delete'),
    path('update/<str:name>/', views.Update, name='update'),
    path('edit/<int:id>/', views.edit_task, name='edit'),
]