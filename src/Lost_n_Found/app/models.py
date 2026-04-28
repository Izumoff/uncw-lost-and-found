"""
app/models.py
"""

from django.conf import settings
from django.db import models


class Report(models.Model):
    REPORT_TYPE_LOST = "lost"
    REPORT_TYPE_FOUND = "found"

    REPORT_TYPE_CHOICES = [
        (REPORT_TYPE_LOST, "Lost"),
        (REPORT_TYPE_FOUND, "Found"),
    ]

    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    OUTCOME_OPEN = 'open'
    OUTCOME_RESOLVED = 'resolved'
    OUTCOME_CLOSED = 'closed'

    OUTCOME_CHOICES = [
        (OUTCOME_OPEN, 'Open'),
        (OUTCOME_RESOLVED, 'Resolved'),
        (OUTCOME_CLOSED, 'Closed'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reports",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    report_type = models.CharField(max_length=10, choices=REPORT_TYPE_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    outcome = models.CharField(
        max_length=20,
        choices=OUTCOME_CHOICES,
        default=OUTCOME_OPEN,
    )
    location_text = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title