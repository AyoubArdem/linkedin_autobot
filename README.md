# linkedin-autobot

[![PyPI](https://img.shields.io/pypi/v/linkedin-autobot.svg)](https://pypi.org/project/linkedin-autobot/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://www.apache.org/licenses/LICENSE-2.0)

`linkedin-autobot` helps you collect LinkedIn profile data, analyze leads, and automate outreach.

## Install

```bash
pip install linkedin-autobot
```

For local browser automation, install automation dependencies manually:

```bash
pip install "linkedin-autobot[automation]"
python -m playwright install chromium
```

## Choose Your Mode

1. Hosted mode: recommended for production (stable, backend-driven).
2. Local bot mode: runs browser automation on the user machine.
3. Colab/Jupyter mode: use async bot (`AsyncLinkedInBot`).

## Environment Variables

Hosted:

- `LINKEDIN_AUTOBOT_BASE_URL`
- `LINKEDIN_AUTOBOT_API_KEY` (optional if your backend does not require it)

Local bot:

- `LINKEDIN_EMAIL`
- `LINKEDIN_PASSWORD`
- `GMAIL_APP_PASSWORD` (optional, for automatic 2FA email verification handling)

Analytics (optional):

- `GOOGLE_API_KEY`

## 2FA Email Verification Handling

When LinkedIn requires email verification (common in automated login scenarios), the bot can automatically fetch and submit the verification code from your Gmail inbox.

**Setup:**

1. Enable 2-Step Verification on your Google account: https://myaccount.google.com/security
2. Generate a Gmail App Password: https://myaccount.google.com/apppasswords
3. Set `GMAIL_APP_PASSWORD` environment variable or pass it to `LinkedInBot`:

```python
with LinkedInBot.from_env(headless=False) as bot:
    # Automatically handles 2FA if LinkedIn requires verification
    bot.login()
```

**How it works:**
- Detects LinkedIn's verification challenge
- Connects to Gmail IMAP
- Fetches the 6-digit code from LinkedIn's verification email
- Automatically enters the code and continues login

**See also:** [2FA_EMAIL_VERIFICATION_GUIDE.md](./2FA_EMAIL_VERIFICATION_GUIDE.md) for detailed setup and troubleshooting.

## Tutorial: Hosted Client

### 1) Create client with `from_env(...)`

```python
from linkedin_autobot import LinkedInAutobotClient

client = LinkedInAutobotClient.from_env()
```

### 2) Collect profile by name with `collect_profile_by_name(name)`

```python
profile = client.collect_profile_by_name("Satya Nadella")
print(profile.profile_url, profile.full_name, profile.title)
```

### 3) Collect profile by URL with `collect_profile_by_url(profile_url)`

```python
profile = client.collect_profile_by_url("https://www.linkedin.com/in/satyanadella/")
print(profile.full_name, profile.location)
```

### 4) Analyze profile with `analyze_profile(profile, prompt)`

```python
analysis = client.analyze_profile(
    profile,
    prompt="Score this lead and suggest the best outreach angle."
)
print(analysis.score, analysis.decision_maker_level)
```

### 5) Send outreach with `send_connection_request(profile_url, message=None)`

```python
sent = client.send_connection_request(
    "https://www.linkedin.com/in/satyanadella/",
    message="Hi Satya, I would love to connect."
)
print(sent)
```

## Tutorial: Local Bot

### 1) Install local requirements, then create bot with `from_env(...)` and login with `login()`

```python
from linkedin_autobot import LinkedInBot

with LinkedInBot.from_env(headless=False) as bot:
    bot.login()
```

## Tutorial: Colab / Jupyter (Async)

In notebook environments, use `AsyncLinkedInBot` (not `LinkedInBot` sync API).

```python
import asyncio
from linkedin_autobot import AsyncLinkedInBot

async def run():
    async with AsyncLinkedInBot.from_env(headless=True) as bot:
        await bot.login()
        profile = await bot.collect_profile_by_name("Satya Nadella")
        print(profile.profile_url, profile.full_name)

await run()
```

### 2) Open a profile with `visit_profile(profile_url)`

```python
with LinkedInBot.from_env(headless=False) as bot:
    bot.login()
    bot.visit_profile("https://www.linkedin.com/in/satyanadella/")
```

### 3) Find profile URL with `find_profile_url_by_name(name)`

```python
with LinkedInBot.from_env(headless=False) as bot:
    bot.login()
    profile_url = bot.find_profile_url_by_name("Satya Nadella")
    print(profile_url)
```

### 4) Collect profile with `collect_profile(profile_url)`

```python
with LinkedInBot.from_env(headless=False) as bot:
    bot.login()
    profile = bot.collect_profile("https://www.linkedin.com/in/satyanadella/")
    print(profile.full_name, profile.title)
```

### 5) Collect by name with `collect_profile_by_name(name)`

```python
with LinkedInBot.from_env(headless=False) as bot:
    bot.login()
    profile = bot.collect_profile_by_name("Satya Nadella")
    print(profile.profile_url)
```

### 6) Send request with `send_connection_request(profile_url, message=None)`

```python
with LinkedInBot.from_env(headless=False) as bot:
    bot.login()
    sent = bot.send_connection_request(
        "https://www.linkedin.com/in/satyanadella/",
        message="Hi Satya, let's connect."
    )
    print(sent)
```

### 7) Close bot manually with `close()`

```python
from linkedin_autobot import LinkedInBot

bot = LinkedInBot.from_env(headless=False)
bot.login()
# ... your actions ...
bot.close()
```

## Tutorial: Local Analytics Engine

### Analyze with `LeadAnalyticsEngine.analyze(profile, prompt)`

```python
from linkedin_autobot import LeadAnalyticsEngine, LinkedInProfile

profile = LinkedInProfile(
    profile_url="https://www.linkedin.com/in/example/",
    full_name="Jane Founder",
    title="Founder & CEO",
    about="B2B growth and sales.",
)

engine = LeadAnalyticsEngine()  # uses GOOGLE_API_KEY if available
result = engine.analyze(profile, "Score this lead and propose outreach.")
print(result.score, result.insights_strategic)
```

## Tutorial: Django Helpers

### `profile_from_lead_model(lead)`

```python
from linkedin_autobot.django import profile_from_lead_model

profile = profile_from_lead_model(lead_instance)
```

### `analyze_lead_model(lead, prompt, api_key=None)`

```python
from linkedin_autobot.django import analyze_lead_model

analysis = analyze_lead_model(lead_instance, "Score this lead.")
print(analysis.score)
```

## Data Models

- `LinkedInCredentials(email, password)`
- `LinkedInProfile(...)`
- `AnalysisResult(...)`

## Exceptions

- `LinkedinAutobotError`
- `MissingDependencyError`
- `AuthenticationError`
- `ScrapingError`

## Practical Notes

- `LinkedInBot.login()` performs preflight checks and raises clear instructions when Chromium is missing.
- If local browser automation is blocked by OS permissions, use hosted mode.
- For production-grade stability, hosted mode is recommended.
