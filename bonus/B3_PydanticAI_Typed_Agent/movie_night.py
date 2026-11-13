"""Movie night: the agent from notebook 1 in one file, so it can run as a terminal chat or a web chat.

Terminal chat:  python movie_night.py
Web chat:       uvicorn movie_night:app --host 127.0.0.1 --port 7932    (from this folder)
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Literal
import os

from dotenv import dotenv_values
from pydantic import BaseModel
from pydantic_ai import Agent, ModelRetry, RunContext

# The model name comes from models.env and the key from the environment or .env, as in the notebooks
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "models.env").exists())
settings = dotenv_values(ROOT / "models.env")
local = dotenv_values(ROOT / ".env")
settings.update({name: value for name, value in local.items() if name in settings and value})
os.environ.setdefault("OPENAI_API_KEY", local.get("OPENAI_API_KEY") or "")

# The house rule: the youngest age that may watch each rating
MIN_AGE = {"G": 0, "PG": 8, "PG-13": 13, "R": 17}


class MoviePick(BaseModel):
    title: str
    age_rating: Literal["G", "PG", "PG-13", "R"]
    minutes: int


@dataclass
class Viewer:
    age: int


agent = Agent(
    "openai:" + settings["MODEL_DEFAULT"],
    name="Movie night",
    output_type=MoviePick,
    deps_type=Viewer,
    model_settings={"openai_reasoning_effort": settings["REASONING_EFFORT"] or None, "timeout": 60},
)


@agent.tool
def allowed_ratings(ctx: RunContext[Viewer]) -> list[str]:
    """The age ratings tonight's youngest viewer may watch."""
    return [rating for rating, age in MIN_AGE.items() if age <= ctx.deps.age]


@agent.output_validator
def check_age(ctx: RunContext[Viewer], pick: MoviePick) -> MoviePick:
    if MIN_AGE[pick.age_rating] > ctx.deps.age:
        raise ModelRetry(f"{pick.title} is rated {pick.age_rating}, and the youngest viewer is {ctx.deps.age}. "
                         f"Pick a film rated {' or '.join(allowed_ratings(ctx))}.")
    return pick


# Who is watching tonight: the youngest person on the sofa is 9
TONIGHT = Viewer(age=9)

# The web chat: a web app that uvicorn can serve
app = agent.to_web(deps=TONIGHT)

if __name__ == "__main__":
    # The terminal chat
    agent.to_cli_sync(deps=TONIGHT, prog_name="movie-night")
