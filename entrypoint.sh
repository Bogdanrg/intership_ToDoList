#!/bin/sh
echo "Starting"
uvicorn main:app --reload --port "$APP_UVICORN_PORT" --host "$APP_UVICORN_HOST"