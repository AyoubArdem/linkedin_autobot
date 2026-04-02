# linkedin-autobot

`linkedin-autobot` is a Python SDK for LinkedIn lead generation workflows.

Created by Ayoub Ardem.

GitHub documentation and project page:

https://github.com/AyoubArdem/linkedin_autobot

## What It Does

- Collect LinkedIn profile data from a profile URL or a person name
- Return structured fields like title, location, about, and experience
- Send LinkedIn connection requests
- Analyze leads and recommend outreach strategies

## Product Style

This package is designed to work well in a hosted-SDK model:

- users install the package from PyPI
- the package talks to a private backend
- the sensitive implementation can stay private

It can also be used locally for direct automation workflows.

## Install

```bash
pip install linkedin-autobot
```

Optional extras:

```bash
pip install "linkedin-autobot[automation]"
pip install "linkedin-autobot[analytics]"
```

## Public Imports

Main public imports:

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

## API Reference

### `LinkedInAutobotClient`

Hosted SDK client for calling your private backend.

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

### `LinkedInBot`

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

### `LeadAnalyticsEngine`

Local analysis engine.

Constructor:

```python
LeadAnalyticsEngine(api_key: str | None = None, model: str = "gemini-1.5-pro")
```

Methods:

- `analyze(profile: LinkedInProfile, prompt: str) -> AnalysisResult`

### `LinkedInCredentials`

Input schema for local bot authentication.

Fields:

- `email: str`
- `password: str`

### `LinkedInProfile`

Structured lead/profile object returned by collection methods.

Fields:

- `profile_url: str`
- `full_name: str`
- `title: str`
- `location: str`
- `about: str`
- `experience: str`
- `status: str`
- `metadata: dict[str, str]`

### `AnalysisResult`

Structured analysis object returned by analytics methods.

Fields:

- `score: float`
- `insights_strategic: str`
- `recommended_outreach_ways: str`
- `decision_maker_level: str`
- `raw_response: str`

## Hosted SDK Example

```python
from linkedin_autobot import LinkedInAutobotClient

client = LinkedInAutobotClient(
    base_url="https://your-backend-domain.com",
    api_key="your-api-key",
)

profile = client.collect_profile_by_name("Satya Nadella")
analysis = client.analyze_profile(
    profile,
    prompt="Score this lead and recommend outreach.",
)

print(profile.title)
print(analysis.score)
```

## Local Example

```python
from linkedin_autobot import LinkedInBot, LinkedInCredentials

credentials = LinkedInCredentials(
    email="your_login@example.com",
    password="your_password",
)

bot = LinkedInBot(credentials)
bot.login()
profile = bot.collect_profile_by_name("Satya Nadella")
bot.close()

print(profile.profile_url)
print(profile.title)
```

## Main Features

- Hosted SDK client support
- Local Playwright automation support
- Structured lead profile schema
- Lead scoring and analytics support
- API-key friendly backend integration
