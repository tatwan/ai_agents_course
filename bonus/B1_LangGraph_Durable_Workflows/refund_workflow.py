"""The refund graph taught in B1, importable again after the kernel restarts."""
from pathlib import Path
import json
import operator
from typing import Annotated, Literal, TypedDict

from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

ATTEMPTS = Path(__file__).parent / 'outputs' / 'review_attempts.json'

class RefundState(TypedDict):
    case_id: str
    amount_usd: float
    days_since_purchase: int
    item_opened: bool
    signals: Annotated[list[str], operator.add]
    audit_log: Annotated[list[str], operator.add]
    needs_review: bool
    decision: str

def normalize(state: RefundState) -> dict:
    return {'amount_usd': round(state['amount_usd'], 2),
            'audit_log': ['normalized']}

def policy_check(state: RefundState) -> dict:
    signals = []
    if state['days_since_purchase'] > 30:
        signals.append('outside_30_day_window')
    if state['item_opened']:
        signals.append('opened_item')
    return {'signals': signals, 'audit_log': ['policy_check']}

def amount_check(state: RefundState) -> dict:
    signals = ['high_amount'] if state['amount_usd'] >= 500 else []
    return {'signals': signals, 'audit_log': ['amount_check']}

def decide(state: RefundState) -> dict:
    return {'needs_review': bool(state['signals']),
            'audit_log': ['routed:human' if state['signals'] else 'routed:auto']}


def choose_route(state: RefundState) -> Literal['auto_approve', 'human_review']:
    return 'human_review' if state['needs_review'] else 'auto_approve'

def auto_approve(state: RefundState) -> dict:
    return {'decision': 'approved', 'audit_log': ['auto:approved']}

def human_review(state: RefundState) -> dict:
    # Deliberately count entries before the interrupt, outside checkpoint state.
    attempts = json.loads(ATTEMPTS.read_text())
    case_id = state['case_id']
    attempts[case_id] = attempts.get(case_id, 0) + 1
    ATTEMPTS.write_text(json.dumps(attempts))
    answer = interrupt({'case_id': case_id,
                        'amount_usd': state['amount_usd'],
                        'signals': state['signals'],
                        'question': 'approve or reject?'})
    if answer not in {'approve', 'reject'}:
        raise ValueError('answer must be approve or reject')
    decision = 'approved' if answer == 'approve' else 'rejected'
    return {'decision': decision, 'audit_log': [f'human:{answer}']}

def finalize(state: RefundState) -> dict:
    return {'audit_log': [f"final:{state['decision']}"]}


def build_refund_graph(checkpointer):
    """Compile the demonstrated topology with the supplied checkpoint store."""
    builder = StateGraph(RefundState)
    builder.add_node('normalize', normalize)
    builder.add_node('policy_check', policy_check)
    builder.add_node('amount_check', amount_check)
    builder.add_node('decide', decide)
    builder.add_node('auto_approve', auto_approve)
    builder.add_node('human_review', human_review)
    builder.add_node('finalize', finalize)
    builder.add_edge(START, 'normalize')
    builder.add_edge('normalize', 'policy_check')
    builder.add_edge('normalize', 'amount_check')
    builder.add_edge(['policy_check', 'amount_check'], 'decide')
    builder.add_conditional_edges('decide', choose_route)
    builder.add_edge('auto_approve', 'finalize')
    builder.add_edge('human_review', 'finalize')
    builder.add_edge('finalize', END)
    return builder.compile(checkpointer=checkpointer)
