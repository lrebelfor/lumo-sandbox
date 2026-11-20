# Lumo sandbox · From Prompt to Production (EvisionC)

A complete practice company for the course **From Prompt to Production**, so you can do every lab, user test and gate without a company or real data of your own.

**Lumo** is a fictional Dutch webshop for design lamps. Its support team is drowning in emails, and your capstone is the AI agent that helps them. Everything here is made up: no real people, no personal data. Read [`data/company.md`](data/company.md) first.

## Start here
1. Click **Use this template → Create a new repository** (top right on GitHub). Call it something like `my-capstone`. That copy is your capstone repo: your notes, prompts, evals and code go there.
2. The course notebooks load this sandbox automatically in Colab. You don't need to download anything.
3. On the **own-case track**? You still use `course_llm.py` from here; put your own documents and data in your copy and point the notebooks at them.

## What's inside
| Path | What | Sessions |
|---|---|---|
| `course_llm.py` | One helper for every model route: Claude, OpenAI, Gemini, open models (OpenRouter, Ollama) | all labs |
| `data/` | Company profile, 40 labelled emails, the handbook (Markdown, messy export, PDF), orders, products, the Gate 1 eval set | S3–S12 |
| `lumo/` | `import lumo` loads the data; `lumo.tools` has ready-made agent tools | S4, S11, Level 2 |
| `testers/` | Scripts for user tests with friends, plus a simulated-user fallback | S12, S24, S29 |
| `templates/` | Capstone README, prompt and eval templates | throughout |

Level 2 and 3 material (pretend Slack, Notion and Gmail, a deploy template) is added before those levels start.

## Choosing a model route (Session 2)
```python
from course_llm import LLM
llm = LLM("claude")      # reference route
llm = LLM("gemini")      # has a free tier, no credit card
llm = LLM("openai")
llm = LLM("openrouter")  # open models, some free; quality and tool use vary
llm = LLM("ollama")      # open models on your own computer (not in Colab)
```
