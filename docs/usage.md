# Usage Guide

[Back to README](../README.md)

## Hosted SDK Mode

Hosted SDK mode is the recommended setup if you want:

- a public PyPI package
- a private backend
- private implementation details

Example:

```python
from linkedin_autobot import LinkedInAutobotClient

client = LinkedInAutobotClient(
    base_url="https://your-backend-domain.com",
    api_key="your-api-key",
)

profile = client.collect_profile_by_name("Satya Nadella")
print(profile.title)

analysis = client.analyze_profile(
    profile,
    prompt="Score this lead and recommend outreach.",
)
print(analysis.score)
```

## Local Mode

Local mode runs automation directly on the user's machine.

Example:

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

## Backend Authentication

Hosted endpoints are designed to work with API keys.

Expected header:

```http
Authorization: Bearer <api_key>
```

Package page:

[linkedin-autobot on PyPI](https://pypi.org/project/linkedin-autobot/)
