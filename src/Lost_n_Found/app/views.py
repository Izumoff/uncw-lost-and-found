"""
app/views.py
"""

from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import (
    CampusUserRegistrationForm,
    FoundItemReportForm,
    RegistrationVerificationCodeForm,
)
from .models import Report


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )


def reports(request):
    """Renders the published reports list page."""
    assert isinstance(request, HttpRequest)

    published_reports = Report.objects.filter(is_published=True)

    return render(
        request,
        'app/reports.html',
        {
            'title': 'Published Reports',
            'year': datetime.now().year,
            'reports': published_reports,
        }
    )


def report_detail(request, report_id):
    """Renders the published report detail page."""
    assert isinstance(request, HttpRequest)

    report = get_object_or_404(
        Report,
        id=report_id,
        is_published=True
    )

    return render(
        request,
        'app/report_detail.html',
        {
            'title': report.title,
            'year': datetime.now().year,
            'report': report,
        }
    )


@login_required
def create_found_report(request):
    """Renders and processes the found item report creation page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = FoundItemReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.report_type = Report.REPORT_TYPE_FOUND
            report.save()
            return redirect(f"{reverse('create_found_report')}?success=1")
    else:
        form = FoundItemReportForm()

    return render(
        request,
        'app/found_report_create.html',
        {
            'title': 'Create Found Item Report',
            'year': datetime.now().year,
            'form': form,
            'success': request.GET.get('success') == '1',
        }
    )


def register(request):
    """Renders and processes the campus user registration page."""
    assert isinstance(request, HttpRequest)

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CampusUserRegistrationForm(request.POST)
        if form.is_valid():
            request.session['pending_registration'] = {
                'username': form.cleaned_data['username'],
                'email': form.cleaned_data['email'],
                'password': form.cleaned_data['password1'],
            }
            return redirect('register_verify')
    else:
        form = CampusUserRegistrationForm()

    return render(
        request,
        'app/register.html',
        {
            'title': 'Register',
            'year': datetime.now().year,
            'form': form,
        }
    )


def register_verify(request):
    """Renders and processes the placeholder registration verification page."""
    assert isinstance(request, HttpRequest)

    if request.user.is_authenticated:
        return redirect('home')

    pending_registration = request.session.get('pending_registration')
    if not pending_registration:
        return redirect('register')

    if request.method == 'POST':
        form = RegistrationVerificationCodeForm(request.POST)
        if form.is_valid():
            username = pending_registration['username']
            email = pending_registration['email']
            password = pending_registration['password']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            campus_user_group, _ = Group.objects.get_or_create(
                name='Campus Community User'
            )
            user.groups.add(campus_user_group)

            del request.session['pending_registration']

            return redirect(
                f"{reverse('login')}?registered=1"
            )
    else:
        form = RegistrationVerificationCodeForm()

    return render(
        request,
        'app/register_verify.html',
        {
            'title': 'Verify Registration',
            'year': datetime.now().year,
            'form': form,
            'email': pending_registration['email'],
            'message': 'Email code sending is not implemented in this stage.',
        }
    )