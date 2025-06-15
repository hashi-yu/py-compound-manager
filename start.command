#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
pip install -r requirements.txt
echo "Starting web application..."
sleep 2 && open http://127.0.0.1:8081 &
python run.py