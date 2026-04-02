# linkedin-autobot

[![PyPI](https://img.shields.io/pypi/v/linkedin-autobot.svg)](https://pypi.org/project/linkedin-autobot/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-green.svg)](https://www.apache.org/licenses/LICENSE-2.0)

`linkedin-autobot` is a Python SDK for LinkedIn lead generation workflows.

Created by Ayoub Ardem.

## What It Does

- Collect LinkedIn profile data from a profile URL or a person name
- Return structured fields like title, location, about, and experience
- Send LinkedIn connection requests
- Analyze leads and recommend outreach strategies

## Product Model

`linkedin-autobot` is designed to work well in a hosted-SDK model:

- users install the package from PyPI
- the SDK talks to a private backend
- the sensitive implementation can stay private

This public repository is intended for documentation, examples, and product information.

## Install

```bash
pip install linkedin-autobot
```

Optional extras:

```bash
pip install "linkedin-autobot[automation]"
pip install "linkedin-autobot[analytics]"
```

## Documentation

- [Usage Guide](docs/usage.md)
- [API Reference](docs/api.md)
- [Examples](docs/examples.md)
- [PyPI Package](https://pypi.org/project/linkedin-autobot/)

## Get linkedin-autobot on PyPI

Visit the package page:

[linkedin-autobot on PyPI](https://pypi.org/project/linkedin-autobot/)

## Main Features

- Hosted SDK client support
- Local Playwright automation support
- Structured lead profile schema
- Lead scoring and analytics support
- API-key friendly backend integration

## Notes

- Hosted SDK mode is the recommended setup for private-source products
- Local automation requires valid LinkedIn credentials
- LinkedIn selectors may need updates when LinkedIn changes its UI
