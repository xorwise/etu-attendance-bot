#!/bin/bash

cd /app/app
celery -A worker.celery_app worker -l info
