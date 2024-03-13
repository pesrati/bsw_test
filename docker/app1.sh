#!/bin/bash

alembic upgrade head

gunicorn app.line_provider.router:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000