# linkedin-autobot

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Status](https://img.shields.io/badge/status-alpha-orange.svg)](#roadmap)

`linkedin-autobot` is a Python toolkit and backend-oriented project for LinkedIn lead generation workflows.

Created by Ayoub Ardem.

It helps you:

- find LinkedIn profiles from a person's name
- collect title, location, about, and experience
- send connection requests
- analyze leads with heuristics or LLMs
- expose a hosted SDK pattern for private backend products

## Contents

- Overview
- Product Model
- Repository Layout
- Quick Start
- SDK Usage
- Backend API
- Environment Variables
- Roadmap

## Overview

This repository contains two layers:

- `src/linkedin_autobot/`: the installable Python package
- `LinkedinAutoBot/`: the Django backend project

The package can be used either:

- as a hosted SDK client that talks to your private backend
- or as a local toolkit for direct automation and analysis

If you want a company-style public product with private implementation, the hosted SDK approach is the recommended one.

## Product Model

Recommended production model:

1. Keep the source repository private.
2. Publish the Python package publicly to PyPI.
3. Run the Django project as a private backend.
4. Let users access the product through API keys and the public SDK.

That gives you:

- a public install experience
- a private implementation
- centralized control over scraping, throttling, analytics, and future billing

## Repository Layout

- `src/linkedin_autobot/client.py`: hosted SDK client for calling the backend
- `src/linkedin_autobot/bot.py`: direct Playwright automation client
- `src/linkedin_autobot/analytics.py`: local analysis engine
- `src/linkedin_autobot/schemas.py`: typed data models
- `LinkedinAutoBot/accounts/`: authentication, users, workspaces, memberships
- `LinkedinAutoBot/automation/`: lead collection and connection workflows
- `LinkedinAutoBot/analytics/`: lead analysis and scoring workflows

## Quick Start

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project with development extras:

```bash
pip install -e .[django,automation,analytics,dev]
```

Move into the Django project folder:

```bash
cd LinkedinAutoBot
```

Run migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

## SDK Usage

Hosted SDK client:

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

Local direct usage:

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

## Backend API

Main hosted endpoints:

- `POST /api/automation/profiles/collect-by-name/`
- `POST /api/automation/profiles/collect/`
- `POST /api/automation/outreach/send-connection-request/`
- `POST /api/analytics/analyze/`

These endpoints are designed for the hosted SDK client and protected with API-key authentication.

Authorization format:

```http
Authorization: Bearer <api_key>
```

## Environment Variables

Use `.env.example` as a starting point.

Important variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `GOOGLE_API_KEY`
- `LINKEDIN_EMAIL`
- `LINKEDIN_PASSWORD`
- `LINKEDIN_AUTOBOT_BASE_URL`
- `LINKEDIN_AUTOBOT_API_KEY`

## Roadmap

- Improve person matching with company and location filters
- Add batch lead collection and analysis
- Add a CLI for hosted and local flows
- Separate the public SDK from the private backend more cleanly
- Publish a public docs site alongside the PyPI package
