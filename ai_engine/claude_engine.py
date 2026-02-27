import requests
import re
import json5
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are CIAgent, an elite market intelligence analyst.

You MUST output strictly valid JSON.
No markdown.
No commentary.
No explanations.
Only raw JSON.
"""


def build_research_prompt(
    query: str,
    sector: Optional[str],
    region: Optional[str],
    depth: str
) -> str:

    context_parts = []

    if sector:
        context_parts.append(f"Industry Sector: {sector}")
    if region:
        context_parts.append(f"Target Region: {region}")

    context_parts.append(f"Depth: {depth}")

    context = "\n".join(context_parts)

    return f"""
{SYSTEM_PROMPT}

Research:

QUERY: {query}

CONTEXT:
{context}

Return JSON with this structure:
{{
  "executive_summary": "...",
  "market_overview": {{
    "market_size": "...",
    "growth_rate": "...",
    "key_trends": [],
    "target_segments": [],
    "geographic_focus": "..."
  }},
  "competitors": [],
  "signals": [],
  "recommendations": [],
  "risk_factors": [],
  "opportunities": [],
  "conclusion": "..."
}}
"""


async def generate_market_report(
    query: str,
    sector: Optional[str] = None,
    region: Optional[str] = None,
    depth: str = "standard"
) -> dict:

    prompt = build_research_prompt(query, sector, region, depth)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "gemma:2b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 700,
                "temperature": 0.2
            }
        },
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    raw_text = response.json()["response"].strip()

    # Extract JSON block
    match = re.search(r'\{.*\}', raw_text, re.DOTALL)
    if not match:
        raise Exception(f"No valid JSON found:\n{raw_text}")

    json_candidate = match.group(0)

    # Remove invalid backslash escapes
    json_candidate = re.sub(r'\\(?!["\\/bfnrtu])', '', json_candidate)

    # Remove trailing commas (very common local model issue)
    json_candidate = re.sub(r',\s*}', '}', json_candidate)
    json_candidate = re.sub(r',\s*]', ']', json_candidate)

    try:
        return json5.loads(json_candidate)
    except Exception as e:
        print("FAILED JSON5 PARSE:\n", json_candidate)
        raise e