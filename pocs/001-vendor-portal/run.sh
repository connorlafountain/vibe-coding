#!/bin/bash
# Quick start script for POC

echo "🚀 Starting Vendor Portal POC..."
echo ""

# Activate venv
source ../../venv/bin/activate

# Always start with fresh database (better for testing POC)
if [ -f "vendor_portal.db" ]; then
    echo "🗑️  Removing old database..."
    rm vendor_portal.db
fi

echo "📊 Creating fresh database with seed data..."
python database.py
echo ""

# Start server
echo "✅ Starting FastAPI server on http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
