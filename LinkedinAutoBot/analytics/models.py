from django.db import models

from accounts.models import User
from automation.models import Leads


class LLM(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="lead_analyses",
    )
    lead = models.ForeignKey(
        Leads,
        on_delete=models.CASCADE,
        related_name="analyses",
    )
    score = models.FloatField(default=0)
    insights_strategic = models.TextField(blank=True, null=True)
    recommended_outreach_ways = models.TextField(blank=True, null=True)
    decision_maker_level = models.CharField(max_length=100, blank=True, null=True)
    prompt = models.TextField(blank=True, null=True)
    raw_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "lead"],
                name="unique_analysis_per_user_and_lead",
            )
        ]

    def __str__(self):
        return f"{self.lead.full_name} score {self.score}"
