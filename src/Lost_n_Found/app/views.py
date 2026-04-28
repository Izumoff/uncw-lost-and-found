"""
app/views.py
"""

from datetime import datetime
from django.utils import timezone

from django.contrib.admin.models import LogEntry
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

from .forms import (
    CampusUserRegistrationForm,
    FoundItemReportForm,
    RegistrationVerificationCodeForm,
)
from .models import Report


def home(request):
    """Renders the home page with summary statistics and recent reports."""
    assert isinstance(request, HttpRequest)

    # Summary statistics
    open_reports_count = Report.objects.filter(
        outcome=Report.OUTCOME_OPEN
    ).count()

    under_review_count = Report.objects.filter(
        status=Report.STATUS_PENDING
    ).count()

    resolved_count = Report.objects.filter(
        outcome=Report.OUTCOME_RESOLVED
    ).count()

    rejected_count = Report.objects.filter(
        status=Report.STATUS_REJECTED
    ).count()

    # Recent published reports (safe for public view)
    recent_reports = Report.objects.filter(
        is_published=True
    ).order_by('-created_at')[:3]

    return render(
        request,
        'app/index.html',
        {
            'title': 'Home Page',
            'year': datetime.now().year,

            # Summary
            'open_reports_count': open_reports_count,
            'under_review_count': under_review_count,
            'resolved_count': resolved_count,
            'rejected_count': rejected_count,

            # Recent reports
            'recent_reports': recent_reports,
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
    """Renders the reports list page with scope and filter handling."""
    assert isinstance(request, HttpRequest)

    scope = request.GET.get('scope', 'published')
    report_type = request.GET.get('report_type', '').strip()
    status = request.GET.get('status', '').strip()
    location = request.GET.get('location', '').strip()
    query = request.GET.get('query', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    reports = Report.objects.all()

    is_security_office_staff = request.user.is_authenticated and request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    if scope == 'mine' and request.user.is_authenticated:
        reports = reports.filter(user=request.user)

    elif scope == 'all':
        if not is_security_office_staff:
            reports = reports.filter(is_published=True)

    else:
        reports = reports.filter(is_published=True)

    allowed_report_types = [
        Report.REPORT_TYPE_FOUND,
        Report.REPORT_TYPE_LOST,
    ]
    if report_type in allowed_report_types:
        reports = reports.filter(report_type=report_type)

    allowed_statuses = [
        Report.STATUS_PENDING,
        Report.STATUS_APPROVED,
        Report.STATUS_REJECTED,
    ]
    if status in allowed_statuses:
        reports = reports.filter(status=status)

    if location:
        reports = reports.filter(location_text__icontains=location)

    if query:
        reports = reports.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location_text__icontains=query)
        )

    if date_from:
        reports = reports.filter(created_at__date__gte=date_from)

    if date_to:
        reports = reports.filter(created_at__date__lte=date_to)

    reports = reports.order_by('-created_at')

    return render(
        request,
        'app/reports.html',
        {
            'title': 'Reports',
            'year': datetime.now().year,
            'reports': reports,
            'current_scope': scope,
            'current_report_type': report_type,
            'current_status': status,
            'current_location': location,
            'current_query': query,
            'current_date_from': date_from,
            'current_date_to': date_to,
            'IS_SECURITY_OFFICE_STAFF': is_security_office_staff,
        }
    )


def report_detail(request, report_id):
    """Renders the report detail page with access control."""
    assert isinstance(request, HttpRequest)

    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.is_authenticated and request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

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
def admin_console(request):
    """Renders the admin console main page."""
    assert isinstance(request, HttpRequest)

    if not request.user.is_superuser:
        return redirect('reports')

    return render(
        request,
        'app/admin_console.html',
        {
            'title': 'Admin Console',
            'year': datetime.now().year,
        }
    )


@login_required
def admin_reports(request):
    """Renders the admin console reports page with no filtering restrictions."""
    assert isinstance(request, HttpRequest)

    is_campus_administrator = request.user.is_superuser

    if not is_campus_administrator:
        return redirect('reports')

    reports = Report.objects.all().order_by('-created_at')

    return render(
        request,
        'app/reports.html',
        {
            'title': 'Admin Console: All Reports',
            'year': datetime.now().year,
            'reports': reports,
            'current_scope': 'all',
            'current_report_type': '',
            'current_status': '',
            'current_location': '',
            'current_query': '',
            'current_date_from': '',
            'current_date_to': '',
            'IS_SECURITY_OFFICE_STAFF': False,
            'IS_ADMIN_CONSOLE': True,
        }
    )


@login_required
def admin_users(request):
    """Renders and processes the admin console users management page."""
    assert isinstance(request, HttpRequest)

    if not request.user.is_superuser:
        return redirect('reports')

    allowed_group_names = [
        'Campus Community User',
        'Security Office Staff',
    ]

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        group_name = request.POST.get('group_name', '').strip()

        target_user = get_object_or_404(User, id=user_id)

        if group_name in allowed_group_names:
            target_group = get_object_or_404(Group, name=group_name)
            target_user.groups.clear()
            target_user.groups.add(target_group)

            logger.info(
                f"Admin {request.user.id} changed role for user {target_user.id} to {group_name}"
            )


            return redirect(f"{reverse('admin_users')}?updated=1")

    users = User.objects.filter(is_superuser=False).order_by('username')

    return render(
        request,
        'app/admin_users.html',
        {
            'title': 'Admin Console: Manage Users & Roles',
            'year': datetime.now().year,
            'users': users,
            'allowed_group_names': allowed_group_names,
            'role_updated': request.GET.get('updated') == '1',
        }
    )


@login_required
def admin_activity(request):
    """Renders the admin console system activity page."""
    assert isinstance(request, HttpRequest)

    if not request.user.is_superuser:
        return redirect('reports')

    activity_logs = Report.objects.select_related('user').order_by('-created_at')[:50]

    return render(
        request,
        'app/admin_activity.html',
        {
            'title': 'Admin Console: System Activity',
            'year': datetime.now().year,
            'activity_logs': activity_logs,
            'IS_REPORT_ACTIVITY': True,
        }
    )


@login_required
def admin_usage_monitoring(request):
    """Renders the admin console usage monitoring page."""
    assert isinstance(request, HttpRequest)

    if not request.user.is_superuser:
        return redirect('reports')

    report_stats = {
        'total_reports': Report.objects.count(),
        'total_found_reports': Report.objects.filter(
            report_type=Report.REPORT_TYPE_FOUND
        ).count(),
        'total_lost_reports': Report.objects.filter(
            report_type=Report.REPORT_TYPE_LOST
        ).count(),
        'published_reports': Report.objects.filter(
            is_published=True
        ).count(),
        'approved_reports': Report.objects.filter(
            status=Report.STATUS_APPROVED
        ).count(),
        'pending_reports': Report.objects.filter(
            status=Report.STATUS_PENDING
        ).count(),
        'rejected_reports': Report.objects.filter(
            status=Report.STATUS_REJECTED
        ).count(),
        'resolved_reports': Report.objects.filter(
            outcome=Report.OUTCOME_RESOLVED
        ).count(),
        'closed_reports': Report.objects.filter(
            outcome=Report.OUTCOME_CLOSED
        ).count(),
    }

    user_stats = {
        'total_users': User.objects.count(),
        'total_superusers': User.objects.filter(is_superuser=True).count(),
        'total_campus_users': User.objects.filter(
            groups__name='Campus Community User'
        ).distinct().count(),
        'total_security_staff': User.objects.filter(
            groups__name='Security Office Staff'
        ).distinct().count(),
    }

    activity_logs_count = LogEntry.objects.count()
    latest_activity = LogEntry.objects.order_by('-action_time').first()

    activity_stats = {
        'total_activity_logs': activity_logs_count,
        'latest_activity_time': latest_activity.action_time if latest_activity else None,
    }

    return render(
        request,
        'app/admin_usage_monitoring.html',
        {
            'title': 'Admin Console: Usage Monitoring',
            'year': datetime.now().year,
            'report_stats': report_stats,
            'user_stats': user_stats,
            'activity_stats': activity_stats,
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
        'app/report_form.html',
        {
            'title': 'Create Found Item Report',
            'year': datetime.now().year,
            'form': form,
            'success': request.GET.get('success') == '1',
        }
    )


@login_required
def create_lost_report(request):
    """Renders and processes the lost item report creation page."""
    assert isinstance(request, HttpRequest)

    if request.method == 'POST':
        form = FoundItemReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.report_type = Report.REPORT_TYPE_LOST
            report.save()
            return redirect(f"{reverse('create_lost_report')}?success=1")
    else:
        form = FoundItemReportForm()

    return render(
        request,
        'app/report_form.html',
        {
            'title': 'Create Lost Item Report',
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
        'app/report_form.html',
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
        'app/report_form.html',
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

    if request.method != 'POST':
        return redirect('reports')

    report = get_object_or_404(Report, id=report_id)

    is_security_office_staff = request.user.groups.filter(
        name='Security Office Staff'
    ).exists()

    if not is_security_office_staff:
        return redirect('reports')

    new_status = request.POST.get('status')

    allowed_statuses = [
        Report.STATUS_PENDING,
        Report.STATUS_APPROVED,
        Report.STATUS_REJECTED,
    ]

    if (
        new_status in allowed_statuses and
        report.outcome == Report.OUTCOME_OPEN
    ):
        report.status = new_status


        if new_status == Report.STATUS_APPROVED:
            report.is_published = True
            report.published_at = timezone.now()
        else:
            report.is_published = False
            report.published_at = None


        logger.info(
            f"User {request.user.id} changed status of report {report.id} to {new_status}"
        )
        report.save()

    return redirect(f"{reverse('report_detail', args=[report.id])}?status_updated=1")


@login_required
def resolve_report(request, report_id):
    """Allows Security Office Staff to mark an approved open report as resolved."""
    assert isinstance(request, HttpRequest)

    if request.method != 'POST':
        return redirect('reports')

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
        logger.info(
            f"User {request.user.id} resolved report {report.id}"
        )
        report.save()

    return redirect(f"{reverse('report_detail', args=[report.id])}?resolved=1")


@login_required
def close_report(request, report_id):
    """Allows Security Office Staff to mark an approved open report as closed."""
    assert isinstance(request, HttpRequest)

    if request.method != 'POST':
        return redirect('reports')

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

        logger.info(
            f"User {request.user.id} closed report {report.id}"
        )

        report.save()

    return redirect(f"{reverse('report_detail', args=[report.id])}?closed=1")


@login_required
def close_own_report(request, report_id):
    """Allows a campus user to close their own lost item report."""
    assert isinstance(request, HttpRequest)

    if request.method != 'POST':
        return redirect('reports')

    report = get_object_or_404(Report, id=report_id)

    if report.user != request.user:
        return redirect('reports')

    if report.report_type != Report.REPORT_TYPE_LOST:
        return redirect('reports')

    if report.outcome != Report.OUTCOME_OPEN:
        return redirect('report_detail', report_id=report.id)

    report.outcome = Report.OUTCOME_CLOSED

    logger.info(
        f"User {request.user.id} closed own report {report.id}"
    )

    report.save()

    return redirect(f"{reverse('report_detail', args=[report.id])}?closed=1")


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