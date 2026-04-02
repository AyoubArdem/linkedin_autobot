class LinkedinAutobotError(Exception):
    """Base exception for the linkedin_autobot package."""


class MissingDependencyError(LinkedinAutobotError):
    """Raised when an optional dependency is required but unavailable."""


class AuthenticationError(LinkedinAutobotError):
    """Raised when LinkedIn authentication fails."""


class ScrapingError(LinkedinAutobotError):
    """Raised when profile data cannot be collected reliably."""
