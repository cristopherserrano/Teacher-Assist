from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('authToken/', views.CreateTokenView.as_view(), name='authToken'),
    path('self/', views.ManageUserView.as_view(), name='self'),
]
