# Aura Electronics Customer Support Agent

A Python-based customer support agent for Aura Electronics that helps handle customer queries, provide product information, and assist with common support tasks. Built with plain Python, no frameworks required.

## Features

- Answer customer queries about products and services
- Provide troubleshooting guidance
- Track and suggest solutions for common issues
- Maintain a professional and courteous tone in all responses

## Policies & Guidelines

1. **Professional Communication** – Always respond politely and professionally.  
2. **No Sharing Sensitive Data** – Do not disclose customer PII or internal company data.  
3. **Product Accuracy** – Ensure information about products, warranties, and services is correct.  
4. **Escalation** – Escalate unresolved issues to human support staff.  
5. **Work Hours Compliance** – Responses should adhere to company support hours (9am–6pm).  

## Setup

1. Install dependencies:

```bash
pip install -e .
```

2.Run the agent
```bash
export OPENAI_API_KEY="your-api-key"
export MONGO_URL="mongodb://localhost:27017"
docker build -t customer-support-agent .
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY customer-support-agent
```

## Usage

The Aura Electronics Customer Support Agent can be used to:

- **Answer customer queries** about products, services, and warranties.  
- **Provide troubleshooting guidance** for common issues with devices.  
- **Suggest solutions** based on frequently reported problems.  
- **Escalate issues** that require human support intervention.  

**Example queries the agent can handle:**

- "How do I reset my Aura speaker?"  
- "Is the Aura 4K TV covered under warranty?"  
- "My headset is not charging, what should I do?"  
- "Escalate this issue to a human agent"
