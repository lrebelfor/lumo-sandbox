# Lumo: the practice company for this course

*Lumo is fictional. Every name, number and customer in this sandbox is made up, so you can use it freely, share it and make mistakes with it.*

## Who Lumo is
Lumo is a small online shop for design lamps, based in Utrecht, the Netherlands. It was founded in 2019 by Sanne de Vries and sells about 120 lamps from twelve European designers, plus spare parts and LED bulbs. Customers are mostly private buyers in the Netherlands, Belgium and Germany, and a growing group of small businesses (cafés, offices, architects).

| | |
|---|---|
| Team | 9 people: founder, 2 support agents, 2 warehouse staff, 1 buyer, 1 marketer, 1 finance, 1 part-time developer |
| Orders | about 1,900 per month, average order value EUR 145 |
| Countries | Netherlands, Belgium, Germany |
| Systems | a webshop (orders and stock), a shared support inbox, Slack, a Notion wiki with the customer handbook |
| Languages | Dutch, English, German |

## The problem you'll work on
Support is drowning. The two support agents, Femke and Youssef, receive about 60 emails a day, rising to 140 in November and December. Most are the same handful of questions: where is my order, how do I return this, my lamp arrived broken, which bulb fits, do you ship to my country. Each answer means looking up an order in the webshop and finding the right rule in a 30-page handbook. The average reply takes 6 minutes, the backlog in December reaches two days, and wrong answers happen: last year 23 customers were promised refunds the policy doesn't allow.

Sanne wants to know: **can an AI agent help support answer faster and more accurately, without upsetting customers or giving away money?**

## What you get in this sandbox
| Folder | What's in it | Used in |
|---|---|---|
| `data/emails.jsonl` | 40 realistic customer emails, each labelled by a support agent (intent, urgency, order number) | S5, S6 |
| `data/handbook/` | The customer handbook, one Markdown file per section | S7–S12 |
| `data/handbook_export_messy.txt` | The same handbook as a messy text export, the way real exports look | S7 |
| `data/handbook.pdf` | The handbook as a PDF | S7 |
| `data/orders.json`, `data/products.json` | 30 orders and the product catalogue | S4, S11, Level 2 |
| `data/eval_rag.csv` | 20 handbook questions with the fact a correct answer must contain | S12 (Gate 1) |
| `lumo/tools.py` | Ready-made tools: look up an order, check stock, add a note, request a refund | S4, S11, Level 2 |
| `testers/` | Scripts so a friend can play a Lumo employee in your user tests | S12, S24, S29 |
| `templates/` | Your capstone README, prompt and eval templates | throughout |

## The people (for user tests)
- **Femke Janssen**, senior support agent, 6 years at Lumo. Knows every rule; worried an AI will make promises she then has to undo.
- **Youssef El Amrani**, support agent, 1 year at Lumo. Fast with tools; still looks up rules often.
- **Sanne de Vries**, founder. Cares about customer happiness scores, cost and not giving away money.
