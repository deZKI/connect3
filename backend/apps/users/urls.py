from django.urls import path

from .api.views import UserRegistrationView, UserDetailView

app_name = 'users'
urlpatterns = [
    path('<int:pk>/', UserDetailView.as_view(), name='detail'),
    path('register/', UserRegistrationView.as_view(), name='register')
]
