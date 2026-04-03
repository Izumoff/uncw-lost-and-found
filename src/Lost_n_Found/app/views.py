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
    """Renders the report detail page with access control."""
    assert isinstance(request, HttpRequest)

    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.is_authenticated and request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    # Allow access if published, owner, or security office staff.
    if not report.is_published:
        if not request.user.is_authenticated:
            return redirect('reports')

        if report.user != request.user and not is_security_office_staff:
            return redirect('reports')

    return render(
        request,
        'app/report_detail.html',
        {
            'title': report.title,
            'year': datetime.now().year,
            'report': report,
            'IS_SECURITY_OFFICE_STAFF': is_security_office_staff,
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


@login_required
def edit_found_report(request, report_id):
    """Renders and processes editing of a user's own found item report."""
    assert isinstance(request, HttpRequest)

    report = get_object_or_404(Report, id=report_id)

    if report.user != request.user:
        return redirect('reports')

    if report.report_type != Report.REPORT_TYPE_FOUND:
        return redirect('reports')

    if report.is_published:
        return redirect('reports')

    if request.method == 'POST':
        form = FoundItemReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('edit_found_report', args=[report.id])}?updated=1")
    else:
        form = FoundItemReportForm(instance=report)

    return render(
        request,
        'app/found_report_create.html',
        {
            'title': 'Edit Found Item Report',
            'year': datetime.now().year,
            'form': form,
            'success': False,
        }
    )


@login_required
def edit_lost_report(request, report_id):
    """Renders and processes editing of a user's own lost item report."""
    assert isinstance(request, HttpRequest)

    report = get_object_or_404(Report, id=report_id)

    if report.user != request.user:
        return redirect('reports')

    if report.report_type != Report.REPORT_TYPE_LOST:
        return redirect('reports')

    if report.is_published:
        return redirect('reports')

    if request.method == 'POST':
        form = FoundItemReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('edit_lost_report', args=[report.id])}?updated=1")
    else:
        form = FoundItemReportForm(instance=report)

    return render(
        request,
        'app/found_report_create.html',
        {
            'title': 'Edit Lost Item Report',
            'year': datetime.now().year,
            'form': form,
            'success': False,
        }
    )


@login_required
def change_report_status(request, report_id):
    """Processes security office staff status updates for a report."""
    assert isinstance(request, HttpRequest)

    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    if not is_security_office_staff:
        return redirect('reports')

    if request.method == 'POST':
        new_status = request.POST.get('status')

        allowed_statuses = [
            Report.STATUS_PENDING,
            Report.STATUS_APPROVED,
            Report.STATUS_REJECTED,
        ]

        if new_status in allowed_statuses:
            report.status = new_status
            report.save()

    return redirect('report_detail', report_id=report.id)


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