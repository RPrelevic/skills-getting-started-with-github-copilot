#!/bin/bash
echo "🧪 Running tests and updating coverage badge..."
python scripts/update_coverage_badge.py
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Badge update completed successfully!"
else
    echo ""
    echo "❌ Badge update failed!"
    exit 1
fi