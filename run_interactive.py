"""
Interactive runner for introduction.py examples
Just uncomment the section you want to run
"""

import sys
import os
from typing import Dict, List, Optional
import nest_asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent, ModelRetry, RunContext, Tool
from pydantic_ai.models.openai import OpenAIModel

# Add src directory to path if needed
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from src.utils.markdown import to_markdown

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Initialize the model
model = OpenAIModel("gpt-4o")

def separator():
    """Print a separator for better readability"""
    print("\n" + "="*60 + "\n")

# Uncomment the section you want to run

# ===============================================================
# 1. Simple Agent - Hello World Example
# ===============================================================

def run_simple_agent():
    """Run the simple agent example"""
    print("Running Simple Agent Example...")
    
    agent1 = Agent(
        model=model,
        system_prompt="You are a helpful customer support agent. Be concise and friendly.",
    )

    # Example usage of basic agent
    response = agent1.run_sync("How can I track my order #12345?")
    print("Response data:")
    print(response.data)
    print("\nAll messages:")
    print(response.all_messages())
    print("\nCost:")
    print(response.cost())

    separator()
    
    response2 = agent1.run_sync(
        user_prompt="What was my previous question?",
        message_history=response.new_messages(),
    )
    print("Response to follow-up question:")
    print(response2.data)

# Uncomment to run
# run_simple_agent()

# ===============================================================
# 2. Agent with Structured Response
# ===============================================================

def run_structured_response():
    """Run the structured response example"""
    print("Running Structured Response Example...")
    
    class ResponseModel(BaseModel):
        """Structured response with metadata."""

        response: str
        needs_escalation: bool
        follow_up_required: bool
        sentiment: str = Field(description="Customer sentiment analysis")

    agent2 = Agent(
        model=model,
        result_type=ResponseModel,
        system_prompt=(
            "You are an intelligent customer support agent. "
            "Analyze queries carefully and provide structured responses."
        ),
    )

    response = agent2.run_sync("How can I track my order #12345?")
    print("Structured response:")
    print(response.data.model_dump_json(indent=2))

# Uncomment to run
# run_structured_response()

# ===============================================================
# 3. Agent with Structured Response & Dependencies
# ===============================================================

def run_dependencies_example():
    """Run the dependencies example"""
    print("Running Dependencies Example...")
    
    class ResponseModel(BaseModel):
        """Structured response with metadata."""

        response: str
        needs_escalation: bool
        follow_up_required: bool
        sentiment: str = Field(description="Customer sentiment analysis")

    # Define order schema
    class Order(BaseModel):
        """Structure for order details."""

        order_id: str
        status: str
        items: List[str]

    # Define customer schema
    class CustomerDetails(BaseModel):
        """Structure for incoming customer queries."""

        customer_id: str
        name: str
        email: str
        orders: Optional[List[Order]] = None

    # Agent with structured output and dependencies
    agent5 = Agent(
        model=model,
        result_type=ResponseModel,
        deps_type=CustomerDetails,
        retries=3,
        system_prompt=(
            "You are an intelligent customer support agent. "
            "Analyze queries carefully and provide structured responses. "
            "Always great the customer and provide a helpful response."
        ),
    )

    # Add dynamic system prompt based on dependencies
    @agent5.system_prompt
    async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
        return f"Customer details: {to_markdown(ctx.deps)}"

    customer = CustomerDetails(
        customer_id="1",
        name="John Doe",
        email="john.doe@example.com",
        orders=[
            Order(order_id="12345", status="shipped", items=["Blue Jeans", "T-Shirt"]),
        ],
    )

    response = agent5.run_sync(user_prompt="What did I order?", deps=customer)

    print("All messages:")
    print(response.all_messages())
    
    print("\nStructured response:")
    print(response.data.model_dump_json(indent=2))

    print(
        "\nCustomer Details:\n"
        f"Name: {customer.name}\n"
        f"Email: {customer.email}\n\n"
        "Response Details:\n"
        f"{response.data.response}\n\n"
        "Status:\n"
        f"Follow-up Required: {response.data.follow_up_required}\n"
        f"Needs Escalation: {response.data.needs_escalation}"
    )

# Uncomment to run
# run_dependencies_example()

# ===============================================================
# 4. Agent with Tools
# ===============================================================

def run_tools_example():
    """Run the tools example"""
    print("Running Tools Example...")
    
    class ResponseModel(BaseModel):
        """Structured response with metadata."""

        response: str
        needs_escalation: bool
        follow_up_required: bool
        sentiment: str = Field(description="Customer sentiment analysis")

    # Define order schema
    class Order(BaseModel):
        """Structure for order details."""

        order_id: str
        status: str
        items: List[str]

    # Define customer schema
    class CustomerDetails(BaseModel):
        """Structure for incoming customer queries."""

        customer_id: str
        name: str
        email: str
        orders: Optional[List[Order]] = None

    shipping_info_db: Dict[str, str] = {
        "12345": "Shipped on 2024-12-01",
        "67890": "Out for delivery",
    }

    def get_shipping_info(ctx: RunContext[CustomerDetails]) -> str:
        """Get the customer's shipping information."""
        return shipping_info_db[ctx.deps.orders[0].order_id]

    # Agent with structured output and dependencies
    agent5 = Agent(
        model=model,
        result_type=ResponseModel,
        deps_type=CustomerDetails,
        retries=3,
        system_prompt=(
            "You are an intelligent customer support agent. "
            "Analyze queries carefully and provide structured responses. "
            "Use tools to look up relevant information."
            "Always great the customer and provide a helpful response."
        ),
        tools=[Tool(get_shipping_info, takes_ctx=True)],
    )

    @agent5.system_prompt
    async def add_customer_name(ctx: RunContext[CustomerDetails]) -> str:
        return f"Customer details: {to_markdown(ctx.deps)}"

    customer = CustomerDetails(
        customer_id="1",
        name="John Doe",
        email="john.doe@example.com",
        orders=[
            Order(order_id="12345", status="shipped", items=["Blue Jeans", "T-Shirt"]),
        ],
    )

    response = agent5.run_sync(
        user_prompt="What's the status of my last order?", deps=customer
    )

    print("All messages:")
    print(response.all_messages())
    
    print("\nStructured response:")
    print(response.data.model_dump_json(indent=2))

    print(
        "\nCustomer Details:\n"
        f"Name: {customer.name}\n"
        f"Email: {customer.email}\n\n"
        "Response Details:\n"
        f"{response.data.response}\n\n"
        "Status:\n"
        f"Follow-up Required: {response.data.follow_up_required}\n"
        f"Needs Escalation: {response.data.needs_escalation}"
    )

# Uncomment to run
# run_tools_example()

# ===============================================================
# Run the desired example(s) by uncommenting the calls below
# ===============================================================

# Uncomment the example you want to run
# run_simple_agent()
# run_structured_response()
# run_dependencies_example()
# run_tools_example()

print("To run an example, edit this file and uncomment one of the function calls at the bottom.") 