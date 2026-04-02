from django.db import models

from accounts.models import WorkSpace


class Leads(models.Model):
    STATUS_CHOICES = [
        ("new", "NEW"),
        ("contacted", "CONTACTED"),
        ("converted", "CONVERTED"),
    ]

    workspace = models.ForeignKey(
        WorkSpace,
        on_delete=models.CASCADE,
        related_name="leads",
    )
    full_name = models.CharField(max_length=255)
    url = models.URLField()
    title = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)
    experience = models.TextField(blank=True)
    about = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "url"],
                name="unique_lead_url_per_workspace",
            )
        ]

    def __str__(self):
        return self.full_name


class LeadInteraction(models.Model):
    workspace = models.ForeignKey(
        WorkSpace,
        on_delete=models.CASCADE,
        related_name="interactions",
    )
    lead = models.ForeignKey(
        Leads,
        on_delete=models.CASCADE,
        related_name="interactions",
    )
    message = models.TextField(blank=True, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(blank=True, null=True)
    response_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.lead.full_name} interaction at {self.sent_at}"


class LeadTAG(models.Model):
    name = models.CharField(max_length=50)
    workspace = models.ForeignKey(
        WorkSpace,
        on_delete=models.CASCADE,
        related_name="lead_tags",
    )
    leads = models.ManyToManyField(Leads, related_name="tags", blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "name"],
                name="unique_tag_name_per_workspace",
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.workspace.name})"
