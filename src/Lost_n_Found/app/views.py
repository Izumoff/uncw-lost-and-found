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
    """Renders the reports list page with scope filtering."""
    assert isinstance(request, HttpRequest)

    scope = request.GET.get('scope', 'published')

    reports = Report.objects.all()

    is_security_office_staff = request.user.is_authenticated and request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    # Scope filtering
    if scope == 'mine' and request.user.is_authenticated:
        reports = reports.filter(user=request.user)

    elif scope == 'all':
        if is_security_office_staff:
            reports = reports
        else:
            reports = reports.filter(is_published=True)

    else:
        # Default: published only
        reports = reports.filter(is_published=True)

    return render(
        request,
        'app/reports.html',
        {
            'title': 'Reports',
            'year': datetime.now().year,
            'reports': reports,
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
    """Renders and processes editing of a found item report."""
    assert isinstance(request, HttpRequest)

    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    if report.user != request.user and not is_security_office_staff:
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
    """Renders and processes editing of a lost item report."""
    assert isinstance(request, HttpRequest)

    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    if report.user != request.user and not is_security_office_staff:
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
            report.is_published = (new_status == Report.STATUS_APPROVED)
            report.save()

    return redirect(f"{reverse('report_detail', args=[report.id])}?status_updated=1")



@login_required
def resolve_report(request, report_id):
    """Allows Security Office Staff to mark an approved open report as resolved."""
    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    if not is_security_office_staff:
        return redirect('reports')

    if (
        report.status == Report.STATUS_APPROVED and
        report.outcome == Report.OUTCOME_OPEN
    ):
        report.outcome = Report.OUTCOME_RESOLVED
        report.save()

    return redirect(f'/reports/{report.id}/?resolved=1')


@login_required
def close_report(request, report_id):
    """Allows Security Office Staff to mark an approved open report as closed."""
    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    if not is_security_office_staff:
        return redirect('reports')

    if (
        report.status == Report.STATUS_APPROVED and
        report.outcome == Report.OUTCOME_OPEN
    ):
        report.outcome = Report.OUTCOME_CLOSED
        report.save()

    return redirect(f'/reports/{report.id}/?closed=1')


@login_required
def close_report(request, report_id):
    """Allows Security Office Staff to mark a report as closed."""
    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    if not is_security_office_staff:
        return redirect('reports')

    if report.status not in ['resolved', 'closed']:
        report.status = 'closed'
        report.save()

    return redirect(f'/reports/{report.id}/?closed=1')






















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