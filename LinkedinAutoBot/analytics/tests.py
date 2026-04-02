from django.test import TestCase

from accounts.models import User, WorkSpace
from automation.models import Leads

from .llm import create_agent
from .models import LLM


class AnalyticsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="analytics@example.com",
            password="strongpass123",
            name="Analytics User",
        )
        self.workspace = WorkSpace.objects.create(name="Analytics", owner=self.user)
        self.lead = Leads.objects.create(
            workspace=self.workspace,
            full_name="Jane Founder",
            url="https://www.linkedin.com/in/jane-founder/",
            title="Founder",
            location="Casablanca",
            about="Focused on B2B growth and revenue systems.",
            experience="Built and scaled multiple outbound teams over ten years.",
        )

    def test_create_agent_fallback_returns_expected_keys(self):
        result = create_agent(prompt="Score this lead", lead=self.lead, api_key="")

        self.assertIn("score", result)
        self.assertIn("insights_strategic", result)
        self.assertIn("recommended_outreach_ways", result)
        self.assertIn("decision_maker_level", result)

    def test_analysis_model_can_store_result(self):
        analysis = LLM.objects.create(
            user=self.user,
            lead=self.lead,
            score=82,
            insights_strategic="Strong fit",
            recommended_outreach_ways="Personalized outreach",
            decision_maker_level="high",
        )

        self.assertEqual(analysis.lead, self.lead)
        self.assertEqual(str(analysis), "Jane Founder score 82")
