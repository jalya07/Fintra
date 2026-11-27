#!/usr/bin/env bash
python bot.py &
uvicorn web:app --host 0.0.0.0 --port "${PORT:-8000}" --no-access-log &
wait -n
exit $?