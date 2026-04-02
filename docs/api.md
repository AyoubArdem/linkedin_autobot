# API Reference

[Back to README](../README.md)

## Public Imports

```python
from linkedin_autobot import (
    AnalysisResult,
    LeadAnalyticsEngine,
    LinkedInAutobotClient,
    LinkedInBot,
    LinkedInCredentials,
    LinkedInProfile,
)
```

## `LinkedInAutobotClient`

Hosted SDK client for calling a private backend.

Constructor:

```python
LinkedInAutobotClient(
    base_url: str | None = None,
    api_key: str | None = None,
    timeout: float = 30.0,
)
```

Methods:

- `collect_profile_by_name(name: str) -> LinkedInProfile`
- `collect_profile_by_url(profile_url: str) -> LinkedInProfile`
- `analyze_profile(profile: LinkedInProfile, prompt: str) -> AnalysisResult`
- `send_connection_request(profile_url: str, message: str | None = None) -> bool`

## `LinkedInBot`

Local Playwright automation client.

Constructor:

```python
LinkedInBot(credentials: LinkedInCredentials, headless: bool = False)
```

Methods:

- `login() -> None`
- `visit_profile(profile_url: str) -> None`
- `find_profile_url_by_name(name: str) -> str`
- `collect_profile(profile_url: str) -> LinkedInProfile`
- `collect_profile_by_name(name: str) -> LinkedInProfile`
- `send_connection_request(profile_url: str, message: str | None = None) -> bool`
- `close() -> None`

## `LeadAnalyticsEngine`

Local analysis engine.

Constructor:

```python
LeadAnalyticsEngine(api_key: str | None = None, model: str = "gemini-1.5-pro")
```

Methods:

- `analyze(profile: LinkedInProfile, prompt: str) -> AnalysisResult`

## `LinkedInCredentials`

Fields:

- `email: str`
- `password: str`

## `LinkedInProfile`

Fields:

- `profile_url: str`
- `full_name: str`
- `title: str`
- `location: str`
- `about: str`
- `experience: str`
- `status: str`
- `metadata: dict[str, str]`

## `AnalysisResult`

Fields:

- `score: float`
- `insights_strategic: str`
- `recommended_outreach_ways: str`
- `decision_maker_level: str`
- `raw_response: str`

Package page:

[linkedin-autobot on PyPI](https://pypi.org/project/linkedin-autobot/)
