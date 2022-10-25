from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(next_page='index'), name= 'login'),
    path('logout/', views.LogoutView.as_view(next_page='login'), name= 'logout'),
    path('', views.index, name='index'),
    path('activate/<uidb64>/<token>/', views.Activation.as_view(), name='activate'),
    path('create-newsletter/', views.PubCreate.as_view(), name='create-newsletter'),
]
