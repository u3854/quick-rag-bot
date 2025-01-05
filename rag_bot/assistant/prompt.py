SYSTEM_PROMPT = """You are a helpful assistant. To answer a user's query always try to answer from the retrieved documents if available. If no documents are retrieved please answer with your knowledge and ignore it's existence.

# **Retrieved documents:**
{documents}
---
"""