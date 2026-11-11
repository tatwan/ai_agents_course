import random
from pathlib import Path

from dotenv import dotenv_values
from google.adk.agents import Agent
from google.adk.integrations.openai import OpenAIResponsesLlm
from google.adk.workflow import START, Workflow

# The model name comes from models.env at the repository folder
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "models.env").exists())
MODEL = dotenv_values(ROOT / "models.env")["MODEL_DEFAULT"]

CITIES = ["Amman", "Cape Town", "Kyoto", "Marrakesh", "Mexico City", "Reykjavik"]


def pick_city() -> str:
    """Pick the destination at random."""
    return random.choice(CITIES)


plan_agent = Agent(
    name="plan_agent",
    model=OpenAIResponsesLlm(model=MODEL),
    instruction=(
        "You get the name of a city. Name the city, then suggest one thing "
        "to do there on a free afternoon, in a single sentence."
    ),
)

root_agent = Workflow(
    name="surprise_trip",
    edges=[(START, pick_city, plan_agent)],
)
