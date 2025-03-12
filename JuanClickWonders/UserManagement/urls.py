from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/',
         views.TokenRefreshView.as_view(), name='refresh-token'),
    path('auth/forgot-password/',
         views.ForgotPasswordView.as_view(), name='forgot-password'),
    path("auth/reset-password/",
         views.ResetPasswordView.as_view(), name="reset-password"),
    path('user/', views.UserView.as_view(), name='user-retrieve'),
    path('user/update-password/', views.UpdatePasswordView.as_view(),
         name='user-update-password'),
    path('user/delete/', views.DeleteUserView.as_view(), name='user-delete'),
    path('profile/', views.UserProfileView.as_view(),
         name='profile-retrieve'),
    path('profile/update/', views.UpdateProfileView.as_view(),
         name='profile-update'),

]
