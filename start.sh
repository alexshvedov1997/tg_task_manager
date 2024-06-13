#!/bin/bash
cd /app
python wait_for_postgres.py
alembic upgrade head
python main.py