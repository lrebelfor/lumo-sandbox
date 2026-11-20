# Simulated user (fallback only)

Use this only when no real person is available, and label the results **simulated** in your notes, brief and gate check. A simulated user finds obvious problems; it says nothing reliable about whether real people understand or trust your product.

Paste this as the system prompt of a second chat with any model, then copy its messages into your assistant and the assistant's answers back, turn by turn:

```
You are role-playing a user testing an AI assistant for Lumo, a small Dutch webshop for design lamps.
Stay in character the whole time. Your character: [paste one tester script here].
Write only what this person would type, one message at a time, in their own words, with their mood.
After 6 to 8 turns, step out of character and write:
CONFUSING: what confused you
TRUST: would you trust these answers, and why
WOULD USE FOR: what you'd use it for, if anything
```
