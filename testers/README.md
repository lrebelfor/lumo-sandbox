# User tests without a company

Three times in the course you put your work in front of real people: **S12** (your RAG assistant), **S24** (your agent with a front end) and **S29** (your deployed agent). On the Lumo track, your testers don't need to know anything about Lumo: give them one of the scripts below and let them play a Lumo employee.

## How to run a test (15 minutes per person)
1. Pick someone: a friend, partner, colleague. They don't need any AI or tech knowledge.
2. Give them **one script** (print it or send it). Let them read it for two minutes.
3. Let them use your assistant for 10 minutes. **Say nothing. Don't explain, don't help.** Every time you want to jump in is a finding.
4. Afterwards, ask only three questions: *What was confusing? Would you trust these answers? What would you use it for?*
5. Write down what they asked, where they got stuck, and what they said.

| Script | Role | Best for |
|---|---|---|
| `tester-1-new-agent.md` | Youssef, a new support agent who doesn't know the rules yet | S12, S24 |
| `tester-2-senior-agent.md` | Femke, a senior agent who knows every rule and distrusts AI | S12, S24, S29 |
| `tester-3-angry-customer.md` | A customer with a late parcel who wants money back | S24, S29 |

## No one available? Simulated users (weaker evidence)
`simulated-user-prompt.md` lets an AI play one of these testers against your assistant. It's useful for finding obvious problems, but it is **not** evidence that real people understand or trust your product. In your brief and gate check, label simulated tests as simulated.
