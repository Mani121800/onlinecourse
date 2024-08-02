from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView
from . import views 


urlpatterns = [
       
    path('signup/',views.SignupPage,name='signup'),
    path('login/',views.LoginPage,name='login'),
    path('course/', views.course_detail, name='course_detail'),



    path('password_reset/', CustomPasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', success_url=reverse_lazy('password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
        path('logout/', views.LogoutPage, name='logout'),



]