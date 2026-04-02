from dataclasses import dataclass, field


@dataclass(slots=True)
class LinkedInCredentials:
    email: str
    password: str


@dataclass(slots=True)
class LinkedInProfile:
    profile_url: str
    full_name: str = ""
    title: str = ""
    location: str = ""
    about: str = ""
    experience: str = ""
    status: str = "new"
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class AnalysisResult:
    score: float
    insights_strategic: str
    recommended_outreach_ways: str
    decision_maker_level: str
    raw_response: str = ""
