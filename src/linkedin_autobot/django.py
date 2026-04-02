from .analytics import LeadAnalyticsEngine
from .schemas import LinkedInProfile


def profile_from_lead_model(lead) -> LinkedInProfile:
    return LinkedInProfile(
        profile_url=lead.url,
        full_name=lead.full_name,
        title=getattr(lead, "title", ""),
        location=getattr(lead, "location", ""),
        about=getattr(lead, "about", ""),
        experience=getattr(lead, "experience", ""),
        status=getattr(lead, "status", "new"),
    )


def analyze_lead_model(lead, prompt: str, api_key: str | None = None):
    engine = LeadAnalyticsEngine(api_key=api_key)
    return engine.analyze(profile_from_lead_model(lead), prompt)
