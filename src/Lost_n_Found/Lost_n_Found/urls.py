"""
urls.py
"""

from datetime import datetime
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),

    path('reports/', views.reports, name='reports'),

    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/<int:report_id>/edit/found/', views.edit_found_report, name='edit_found_report'),
    path('reports/<int:report_id>/edit/lost/', views.edit_lost_report, name='edit_lost_report'),

    path('reports/<int:report_id>/status/', views.change_report_status, name='change_report_status'),
    path('reports/<int:report_id>/resolve/', views.resolve_report, name='resolve_report'),
    path('reports/<int:report_id>/close/', views.close_report, name='close_report'),
    path('reports/<int:report_id>/close-own/', views.close_own_report, name='close_own_report'),

    path('reports/create/found/', views.create_found_report, name='create_found_report'),
    path('reports/create/lost/', views.create_lost_report, name='create_lost_report'),

    path('admin-console/', views.admin_console, name='admin_console'),
    path('admin-console/reports/', views.admin_reports, name='admin_reports'),
    path('admin-console/users/', views.admin_users, name='admin_users'),
    path('admin-console/activity/', views.admin_activity, name='admin_activity'),
    path('admin-console/usage/', views.admin_usage_monitoring, name='admin_usage_monitoring'),

    path('register/', views.register, name='register'),
    path('register/verify/', views.register_verify, name='register_verify'),
    path(
        'login/',
        LoginView.as_view(
            template_name='app/login.html',
            authentication_form=forms.BootstrapAuthenticationForm,
            redirect_authenticated_user=True,
            extra_context={
                'title': 'Log in',
                'year': datetime.now().year,
            }
        ),
        name='login'
    ),
    path(
        'password-reset/',
        PasswordResetView.as_view(
            template_name='app/password_reset_form.html',
            email_template_name='app/password_reset_email.html',
            subject_template_name='app/password_reset_subject.txt',
            success_url='/password-reset/done/',
            extra_context={
                'title': 'Reset password',
                'year': datetime.now().year,
            }
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        PasswordResetDoneView.as_view(
            template_name='app/password_reset_done.html',
            extra_context={
                'title': 'Password reset sent',
                'year': datetime.now().year,
            }
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(
            template_name='app/password_reset_confirm.html',
            success_url='/reset/done/',
            extra_context={
                'title': 'Set new password',
                'year': datetime.now().year,
            }
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(
            template_name='app/password_reset_complete.html',
            extra_context={
                'title': 'Password reset complete',
                'year': datetime.now().year,
            }
        ),
        name='password_reset_complete'
    ),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]