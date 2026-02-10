"""
Langfuse observability configuration for ADK agents.

This module initializes Langfuse instrumentation for automatic tracing of
all Google ADK agent calls, LLM interactions, and tool executions.
"""

import os
from dotenv import load_dotenv
from langfuse import get_client
from openinference.instrumentation.google_adk import GoogleADKInstrumentor

# Load environment variables
load_dotenv()

# Initialize Langfuse client
langfuse = get_client()

# Verify authentication (optional check - may fail on some self-hosted instances)
try:
    if langfuse.auth_check():
        print("✓ Langfuse client authenticated and ready!")
        print(f"  Connected to: {os.getenv('LANGFUSE_BASE_URL')}")
    else:
        print("✗ Langfuse authentication failed. Please check your credentials.")
except Exception as e:
    # Some self-hosted Langfuse instances may have API differences
    # The client will still work for tracing even if auth_check fails
    print(f"⚠ Langfuse auth check encountered an issue (tracing should still work): {type(e).__name__}")
    print(f"  Connected to: {os.getenv('LANGFUSE_BASE_URL')}")

# Instrument Google ADK for automatic tracing
try:
    GoogleADKInstrumentor().instrument()
    print("✓ Google ADK instrumentation enabled")
    print("  All agent calls, LLM interactions, and tools will be traced automatically")
except Exception as e:
    print(f"✗ Google ADK instrumentation error: {e}")

