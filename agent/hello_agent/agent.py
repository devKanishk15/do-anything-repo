from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prometheus_agent.prometheus_agent import prometheus_agent
from google.adk.tools.agent_tool import AgentTool
from dotenv import load_dotenv
import os

load_dotenv()

root_agent = Agent(
    model=LiteLlm(
        model="litellm_proxy/google/gemini-2.5-pro"
    ),
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Ask user his name and greet him.',
    tools=[AgentTool(prometheus_agent)]
)

