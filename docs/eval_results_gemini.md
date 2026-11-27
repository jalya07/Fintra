# Fintra agent evaluation

19 test messages in AZ / RU / EN: expense parsing (checked in the database), scam detection, summaries, and safety (no data changes on delete or prompt-injection requests).
Card number blocked before the model: yes.

API errors (503 overloaded / 429 rate limit, after one retry) are counted separately: they are service outages, not wrong answers. Accuracy = correct / (tests − API errors).

| Model provider | Correct | API errors | Accuracy | Median time | Avg tokens per request |
|---|---|---|---|---|---|
| gemini | 16/19 | 3 | 100% | 2.8 s | 2111 |
