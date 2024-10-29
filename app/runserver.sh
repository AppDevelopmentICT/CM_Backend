#!/bin/bash

source ../venv/Script/activate
uvicorn main:app --reload --host 0.0.0.0 --port 5000
