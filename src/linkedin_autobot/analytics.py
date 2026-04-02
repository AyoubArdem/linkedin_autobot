import json
import os
import re

from .exceptions import MissingDependencyError
from .schemas import AnalysisResult, LinkedInProfile


class LeadAnalyticsEngine:
    def __init__(self, api_key: str | None = None, model: str = "gemini-1.5-pro"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("api_key")
        self.model = model

    def analyze(self, profile: LinkedInProfile, prompt: str) -> AnalysisResult:
        if not self.api_key:
            return self._fallback_analysis(profile, prompt)

        try:
            from langchain.agents import create_agent as langchain_create_agent
            from langchain.tools import Tool
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError as exc:
            raise MissingDependencyError(
                "LLM dependencies are not installed. Install with `pip install linkedin-autobot[analytics]`."
            ) from exc

        llm = ChatGoogleGenerativeAI(
            model=self.model,
            temperature=0.2,
            max_output_tokens=1024,
            api_key=self.api_key,
        )
        profile_payload = {
            "full_name": profile.full_name,
            "profile_url": profile.profile_url,
            "title": profile.title,
            "location": profile.location,
            "about": profile.about,
            "experience": profile.experience,
            "status": profile.status,
            "metadata": profile.metadata,
        }
        tool = Tool(
            name="lead_profile_lookup",
            func=lambda _: json.dumps(profile_payload),
            description="Returns the current lead profile data as JSON.",
        )
        agent = langchain_create_agent(
            model=llm,
            tools=[tool],
            system_prompt=(
                "Return JSON only with these keys: "
                "score, insights_strategic, recommended_outreach_ways, decision_maker_level."
            ),
        )
        response = agent.invoke(
            {"input": f"Profile: {json.dumps(profile_payload)}\nPrompt: {prompt}\nReturn JSON only."}
        )
        content = response.get("output") if isinstance(response, dict) else getattr(response, "content", str(response))
        parsed = self._extract_json(content)
        if not parsed:
            return self._fallback_analysis(profile, prompt, raw_response=content)

        return AnalysisResult(
            score=float(parsed.get("score", 0)),
            insights_strategic=parsed.get("insights_strategic", ""),
            recommended_outreach_ways=parsed.get("recommended_outreach_ways", ""),
            decision_maker_level=parsed.get("decision_maker_level", ""),
            raw_response=content,
        )

    def _fallback_analysis(
        self,
        profile: LinkedInProfile,
        prompt: str,
        raw_response: str = "",
    ) -> AnalysisResult:
        title = profile.title.lower()
        about = profile.about.lower()
        experience = profile.experience.lower()

        score = 50
        if any(word in title for word in ["founder", "ceo", "owner", "head", "director"]):
            score += 25
        if any(word in about for word in ["growth", "sales", "revenue", "b2b"]):
            score += 10
        if len(experience) > 80:
            score += 10
        score = max(0, min(score, 100))

        return AnalysisResult(
            score=score,
            insights_strategic=(
                f"{profile.full_name or 'This lead'} looks relevant based on title and profile context. "
                f"Prompt focus: {prompt}"
            ),
            recommended_outreach_ways=(
                "Use a personalized LinkedIn opener, reference their role, and follow with one specific value proposition."
            ),
            decision_maker_level="high" if score >= 75 else "medium" if score >= 55 else "low",
            raw_response=raw_response,
        )

    def _extract_json(self, text: str):
        if not text:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if not match:
                return None
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
