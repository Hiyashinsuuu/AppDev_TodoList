
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views
from .views import TodoViewSet, UserRegistrationView, UserLoginView

router = DefaultRouter()
router.register(r'todos', TodoViewSet, basename='todo')
router.register(r'register', UserRegistrationView, basename='register')
router.register(r'login', UserLoginView, basename='login')

urlpatterns = [
    path('', views.home, name='home-page'),
    path('api/', include(router.urls)),  # Include the API routes
    path('todo/', views.home, name='todo'),
    path('logout/', views.LogoutView, name='logout'),
    path('edit/<int:id>/', views.edit_task, name='edit'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]