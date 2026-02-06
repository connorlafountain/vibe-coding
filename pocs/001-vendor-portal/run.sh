#!/bin/bash
# Quick start script for POC

echo "🚀 Starting Vendor Portal POC..."
echo ""

# Activate venv
source ../../venv/bin/activate

# Check if database exists
if [ ! -f "vendor_portal.db" ]; then
    echo "📊 Database not found. Creating and seeding..."
    python database.py
    echo ""
fi

# Start server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
