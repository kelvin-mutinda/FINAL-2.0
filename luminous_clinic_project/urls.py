# luminous_clinic_project/luminous_clinic_project/urls.py
from django.urls import path, include
from django.contrib.auth import views as auth_views
from luminous_clinic.views import login_view, register

urlpatterns = [
    path('', include('luminous_clinic.urls')),  # Include the luminous_clinic app URLs under a subpath
    path('login/', login_view, name='login'),  # Use custom login view
    path('register/', register, name='register'),  # Use custom register view
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),  # Redirect to landing page after logout
]