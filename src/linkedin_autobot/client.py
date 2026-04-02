import json
import os
from dataclasses import asdict
from urllib import error, request

from .exceptions import LinkedinAutobotError
from .schemas import AnalysisResult, LinkedInProfile


class LinkedInAutobotClient:
    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
        self.base_url = (base_url or os.getenv("LINKEDIN_AUTOBOT_BASE_URL", "")).rstrip("/")
        self.api_key = api_key or os.getenv("LINKEDIN_AUTOBOT_API_KEY")
        self.timeout = timeout

        if not self.base_url:
            raise ValueError("A base_url is required for the hosted SDK client.")

    def collect_profile_by_name(self, name: str) -> LinkedInProfile:
        payload = self._post("/api/automation/profiles/collect-by-name/", {"name": name})
        return self._profile_from_payload(payload)

    def collect_profile_by_url(self, profile_url: str) -> LinkedInProfile:
        payload = self._post("/api/automation/profiles/collect/", {"profile_url": profile_url})
        return self._profile_from_payload(payload)

    def analyze_profile(self, profile: LinkedInProfile, prompt: str) -> AnalysisResult:
        payload = self._post(
            "/api/analytics/analyze/",
            {
                "profile": asdict(profile),
                "prompt": prompt,
            },
        )
        return AnalysisResult(
            score=float(payload.get("score", 0)),
            insights_strategic=payload.get("insights_strategic", ""),
            recommended_outreach_ways=payload.get("recommended_outreach_ways", ""),
            decision_maker_level=payload.get("decision_maker_level", ""),
            raw_response=payload.get("raw_response", ""),
        )

    def send_connection_request(self, profile_url: str, message: str | None = None) -> bool:
        payload = self._post(
            "/api/automation/outreach/send-connection-request/",
            {
                "profile_url": profile_url,
                "message": message,
            },
        )
        return bool(payload.get("sent", False))

    def _post(self, path: str, payload: dict):
        body = json.dumps(payload).encode("utf-8")
        endpoint = f"{self.base_url}{path}"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = request.Request(endpoint, data=body, headers=headers, method="POST")

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                content = response.read().decode("utf-8")
        except error.HTTPError as exc:
            message = exc.read().decode("utf-8", errors="replace")
            raise LinkedinAutobotError(
                f"Backend request failed with status {exc.code}: {message}"
            ) from exc
        except error.URLError as exc:
            raise LinkedinAutobotError(f"Could not reach backend at {endpoint}.") from exc

        if not content:
            return {}

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            raise LinkedinAutobotError("Backend returned invalid JSON.") from exc

    def _profile_from_payload(self, payload: dict) -> LinkedInProfile:
        return LinkedInProfile(
            profile_url=payload.get("profile_url", ""),
            full_name=payload.get("full_name", ""),
            title=payload.get("title", ""),
            location=payload.get("location", ""),
            about=payload.get("about", ""),
            experience=payload.get("experience", ""),
            status=payload.get("status", "new"),
            metadata=payload.get("metadata", {}) or {},
        )
