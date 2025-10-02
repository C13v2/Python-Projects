# Telegram AI Assistant with Smart Google Search

This project is a **Telegram bot** built in Python that serves as an AI assistant. It integrates **OpenAI GPT** for intelligent responses and **SerpAPI (Google Search API)** for real-time searches when required. The bot also maintains a **conversation history** for each user, allowing context-aware replies.

---

## Features

- Responds to any question using **GPT-4o-mini**.
- Automatically decides when to perform a **Google search** for updated information.
- Summarizes search results and provides **links to sources**.
- Stores conversation history per user in a **JSON file**.
- Handles long messages (>4000 characters) for Telegram.
- Provides `/start` and `/storico` commands for interaction and history review.
- Includes **logging** for debug and monitoring.

---

## Requirements

- Python 3.10+
- Libraries:
  ```bash
  
---  
Accounts / API keys:
Telegram Bot Token
OpenAI API Key
SerpAPI API Key

---

How it Works
1. User Interaction
User sends a message in Telegram.
Bot reads the message and retrieves the user's conversation history.

2. Decision: Google Search or Not

The bot asks GPT: "Does this question require an up-to-date Google search? Answer YES or NO."
YES → the bot searches Google using SerpAPI.
NO → GPT answers directly using memory of past conversations.

3. Google Search (if needed)

Top 5 search results are retrieved (title + link).
Fallback is applied: if a result has no title or link, it defaults to "No title" or "No link".
GPT summarizes the search results and provides a concise response, appended with the links.

4. Direct GPT Response

If no search is needed, GPT answers directly.
The bot includes the last 10 messages from conversation history to maintain context.

5. Conversation Memory

Both the user message and GPT's response are saved in chat_history.json.
This allows context-aware responses for future interactions.

6. Sending Responses

Messages longer than Telegram’s 4096-character limit are automatically split into chunks.
This ensures that even long GPT responses are delivered correctly.

7. Logging

User inputs, GPT decisions (YES/NO), and any errors are logged.
Only the first 100 characters of GPT responses are logged to avoid oversized log files.

Commands
/start – Initializes interaction with the bot.
/storico – Displays the last 20 messages in your chat history.

---
