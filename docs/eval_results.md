# Fintra agent evaluation

19 test messages in AZ / RU / EN: expense parsing (checked in the database), scam detection, summaries, and safety (no data changes on delete or prompt-injection requests).
Card number blocked before the model: no.

| Model provider | Correct | Median time | Avg tokens per request |
|---|---|---|---|
| openrouter | 7/19 | 2.8 s | — |
| ollama | 10/19 | 2.0 s | — |
