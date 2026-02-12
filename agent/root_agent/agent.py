from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .prometheus_agent.prometheus_agent import prometheus_agent
from .loki_agent.loki_agent import loki_agent
from google.adk.tools.agent_tool import AgentTool
from dotenv import load_dotenv
import os

# Initialize Langfuse observability
from . import langfuse_config

load_dotenv()

root_agent = Agent(
    model=LiteLlm(
        model="litellm_proxy/google/gemini-2.5-pro"
    ),
    name='root_agent',
    description='Intelligent monitoring and observability assistant that analyzes user queries and delegates to specialized agents for metrics (Prometheus) and logs (Loki).',
    instruction='''You are a monitoring and observability coordinator. Your role is to understand user queries and delegate them to the appropriate specialized agent:

- **For metrics, performance data, or monitoring queries**: Use the Prometheus Agent
  Examples: CPU usage, memory consumption, network metrics, application performance, resource utilization
  
- **For logs, errors, or debugging queries**: Use the Loki Agent  
  Examples: error messages, application logs, authentication failures, stack traces, log patterns

**Your responsibilities:**
1. Analyze the user's question to determine if it's about metrics or logs
2. Delegate to the appropriate agent (Prometheus or Loki)
3. Return clear, actionable responses based on the agent's findings
4. If the query involves both metrics and logs, coordinate with both agents

**Important:** Do NOT ask user the details which you already have. Focus only on answering their monitoring and observability questions using the available tools.''',
    tools=[AgentTool(prometheus_agent), AgentTool(loki_agent)]
)

