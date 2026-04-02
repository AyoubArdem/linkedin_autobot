from django.test import TestCase

from accounts.models import User, WorkSpace

from .models import LeadInteraction, LeadTAG, Leads


class AutomationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="strongpass123",
            name="Workspace Owner",
        )
        self.workspace = WorkSpace.objects.create(name="Growth", owner=self.user)

    def test_create_lead(self):
        lead = Leads.objects.create(
            workspace=self.workspace,
            full_name="Jane Doe",
            url="https://www.linkedin.com/in/jane-doe/",
            title="Founder",
            location="Casablanca",
        )

        self.assertEqual(lead.status, "new")
        self.assertEqual(str(lead), "Jane Doe")

    def test_tag_can_attach_to_lead(self):
        lead = Leads.objects.create(
            workspace=self.workspace,
            full_name="Jane Doe",
            url="https://www.linkedin.com/in/jane-doe/",
        )
        tag = LeadTAG.objects.create(name="Priority", workspace=self.workspace)
        tag.leads.add(lead)

        self.assertEqual(tag.leads.count(), 1)

    def test_interaction_points_to_lead(self):
        lead = Leads.objects.create(
            workspace=self.workspace,
            full_name="Jane Doe",
            url="https://www.linkedin.com/in/jane-doe/",
        )
        interaction = LeadInteraction.objects.create(
            workspace=self.workspace,
            lead=lead,
            message="Nice to connect with you.",
        )

        self.assertEqual(interaction.lead, lead)
