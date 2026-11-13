"""The reporter's tool, in the form a JSON crew project loads: a BaseTool subclass in tools/."""
import json

from crewai.tools import BaseTool

RESULT_SHEET = {
    "Northside Falcons": {
        "played": "Friday",
        "opponent": "Riverside Otters",
        "score": "Falcons 2, Otters 3",
        "falcons_goals": "Lina Haddad (2)",
        "winning_goal": "Otters, in minute 88",
    }
}


class MatchResult(BaseTool):
    name: str = "match_result"
    description: str = "Look up the result of a school team's latest match on the result sheet."

    def _run(self, team: str) -> str:
        print(f"TOOL CALLED: match_result({team})")
        if team not in RESULT_SHEET:
            return f"no match on the result sheet for {team}"
        return json.dumps(RESULT_SHEET[team])
