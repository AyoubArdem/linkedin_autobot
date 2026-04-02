import json
import os
import re


def get_lead_info(lead):
    return {
        "full_name": getattr(lead, "full_name", ""),
        "profile_url": getattr(lead, "url", getattr(lead, "profile_url", "")),
        "title": getattr(lead, "title", ""),
        "location": getattr(lead, "location", ""),
        "about": getattr(lead, "about", ""),
        "experience": getattr(lead, "experience", ""),
        "status": getattr(lead, "status", "new"),
        "score": getattr(lead, "score", 0),
    }


def _fallback_analysis(lead, prompt):
    title = (lead.title or "").lower()
    about = (lead.about or "").lower()
    experience = (lead.experience or "").lower()

    score = 50
    if any(word in title for word in ["founder", "ceo", "owner", "head", "director"]):
        score += 25
    if any(word in about for word in ["growth", "sales", "revenue", "b2b"]):
        score += 10
    if len(experience) > 80:
        score += 10

    score = max(0, min(score, 100))

    return {
        "score": score,
        "insights_strategic": (
            f"{lead.full_name} looks relevant for outreach based on title and profile context. "
            f"Prompt focus: {prompt}"
        ),
        "recommended_outreach_ways": (
            "Start with a personalized LinkedIn message referencing their role, then follow with a concise value proposition."
        ),
        "decision_maker_level": (
            "high" if score >= 75 else "medium" if score >= 55 else "low"
        ),
        "raw_response": json.dumps(
            {
                "source": "fallback",
                "lead": get_lead_info(lead),
                "prompt": prompt,
            }
        ),
    }


def _extract_json(text):
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


def create_agent(prompt, lead, api_key=None):
    lead_info = get_lead_info(lead)

    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("api_key")

    if not api_key:
        return _fallback_analysis(lead, prompt)

    try:
        from langchain.agents import create_agent as langchain_create_agent
        from langchain.tools import Tool
        from langchain_google_genai import ChatGoogleGenerativeAI
    except ImportError:
        return _fallback_analysis(lead, prompt)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.2,
        max_output_tokens=1024,
        api_key=api_key,
    )

    lead_tool = Tool(
        name="lead_database_lookup",
        func=lambda _: json.dumps(lead_info),
        description="Retrieve analytics-ready information about a LinkedIn lead from database.",
    )

    system_prompt = (
        "You analyze LinkedIn leads and return JSON with exactly these keys: "
        "score, insights_strategic, recommended_outreach_ways, decision_maker_level. "
        "Score must be a number from 0 to 100."
    )

    agent = langchain_create_agent(
        model=llm,
        tools=[lead_tool],
        system_prompt=system_prompt,
    )

    user_input = (
        f"Lead data: {json.dumps(lead_info)}\n"
        f"User prompt: {prompt}\n"
        "Return JSON only."
    )
    response = agent.invoke({"input": user_input})

    content = ""
    if isinstance(response, dict):
        content = response.get("output") or response.get("content") or str(response)
    else:
        content = getattr(response, "content", str(response))

    parsed = _extract_json(content)
    if not parsed:
        fallback = _fallback_analysis(lead, prompt)
        fallback["raw_response"] = content
        return fallback

    return {
        "score": float(parsed.get("score", 0)),
        "insights_strategic": parsed.get("insights_strategic", ""),
        "recommended_outreach_ways": parsed.get("recommended_outreach_ways", ""),
        "decision_maker_level": parsed.get("decision_maker_level", ""),
        "raw_response": content,
    }
