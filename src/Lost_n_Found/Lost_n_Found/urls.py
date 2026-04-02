"""
urls.py
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('reports/', views.reports, name='reports'),
    path('reports/<int:report_id>/', views.report_detail, name='report_detail'),
    path('reports/<int:report_id>/edit/found/', views.edit_found_report, name='edit_found_report'),
    path('reports/<int:report_id>/edit/lost/', views.edit_lost_report, name='edit_lost_report'),

    path('reports/create/found/', views.create_found_report, name='create_found_report'),


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
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
]