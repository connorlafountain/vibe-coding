#!/bin/bash

echo "🚀 Starting Advisory Services Portal POC..."
echo ""

# Initialize database and seed data
echo "📋 Initializing database and seeding mock data..."
python database.py
echo ""

# Start FastAPI server
echo "🌐 Starting web server on http://localhost:8000"
echo ""
python app.py
