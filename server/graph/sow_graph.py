from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

from agents.drafting_agent import DraftingAgent
from agents.compliance_agent import ComplianceAgent
from agents.validation_agent import ValidationAgent
from agents.formatting_agent import FormattingAgent

# Define our state
class State(TypedDict, total=False):
    flow: str
    previous_sow: str
    query_map: dict
    user_query: str
    additional_context: str
    sow: str            # SOW as a JSON string (or raw text) produced by the drafting agent.
    validated_sow: dict # Parsed and validated SOW data.
    formatted_sow: str  # Filename of the generated DOCX.
    compliance_results: dict  # Results from compliance analysis.
    feedback: str
    error: str
    retryCount: int
    doc_file_path: str

# Initialize agents
drafting_agent = DraftingAgent()
compliance_agent = ComplianceAgent()
validation_agent = ValidationAgent()
formatting_agent = FormattingAgent()

# Agent processing functions
def get_relevant_context(state: State):
    """Get relevant context for the query"""
    context = drafting_agent.get_relevant_context(state['user_query'])
    return {'additional_context': context, 'retryCount': 0}

def process_drafting(state: State):
    """Process drafting stage"""
    return drafting_agent.process_sow(state)

def process_compliance(state: State):
    """Process compliance checking"""
    return compliance_agent.process_sow(state)

def process_validation(state: State):
    """Process validation stage"""
    return validation_agent.process_sow(state)

def process_formatting(state: State):
    """Process formatting stage"""
    return formatting_agent.process_sow(state)

def agent_router(state: State):
    """Route based on feedback and error state"""
    if state['retryCount'] > 10:
        return 'SUCCESS'
    # If any error exists (from compliance or validation), loop back to drafting.
    if state.get('error'):
        print(f"error: {state.get('error')}")
        return 'REJECTED'
    if state.get('feedback') == 'ACCEPTED':
        return 'SUCCESS'
    print(f"error: {state.get('error')}")
    return 'REJECTED'

def create_graph():
    """Create the workflow graph"""
    # Initialize graph builder
    graph_builder = StateGraph(State)
    
    # Add nodes
    graph_builder.add_node('get_relevant_context', get_relevant_context)
    graph_builder.add_node('drafting_agent', process_drafting)
    graph_builder.add_node('compliance_agent', process_compliance)
    graph_builder.add_node('validation_agent', process_validation)
    graph_builder.add_node('formatting_agent', process_formatting)
    
    # Add edges
    graph_builder.add_edge(START, 'get_relevant_context')
    graph_builder.add_edge('get_relevant_context', 'drafting_agent')
    graph_builder.add_edge('drafting_agent', 'compliance_agent')
    graph_builder.add_edge('compliance_agent', 'validation_agent')
    
    # Add conditional edges
    graph_builder.add_conditional_edges(
        "validation_agent",
        agent_router,
        {
            'SUCCESS': 'formatting_agent',
            'REJECTED': 'drafting_agent'
        }
    )
    
    graph_builder.add_edge('formatting_agent', END)
    
    # Compile and return graph
    return graph_builder.compile()

# Create the graph singleton
graph = create_graph()