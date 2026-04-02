# Examples

## Collect by Name with Hosted SDK

```python
from linkedin_autobot import LinkedInAutobotClient

client = LinkedInAutobotClient(
    base_url="https://your-backend-domain.com",
    api_key="your-api-key",
)

profile = client.collect_profile_by_name("Satya Nadella")
print(profile.full_name)
print(profile.title)
print(profile.location)
```

## Collect by Profile URL

```python
from linkedin_autobot import LinkedInAutobotClient

client = LinkedInAutobotClient(
    base_url="https://your-backend-domain.com",
    api_key="your-api-key",
)

profile = client.collect_profile_by_url("https://www.linkedin.com/in/example/")
print(profile.about)
```

## Analyze a Profile

```python
from linkedin_autobot import LinkedInAutobotClient

client = LinkedInAutobotClient(
    base_url="https://your-backend-domain.com",
    api_key="your-api-key",
)

profile = client.collect_profile_by_name("Jane Founder")
result = client.analyze_profile(
    profile,
    prompt="Score this lead and recommend outreach.",
)

print(result.score)
print(result.insights_strategic)
print(result.decision_maker_level)
```

## Local Bot Example

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
```
