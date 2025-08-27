#!/usr/bin/env python3
"""
Web-compatible version of Brainstormers for deployment
Now uses Flask web interface instead of terminal
"""

import os

# Run the web interface for deployments
if __name__ == "__main__":
    from web_app import app
    
    print("🌐 Starting Brainstormers Web Interface...")
    port = int(os.getenv('PORT', 8080))
    print(f"✅ Server running on port {port}")
    
    # Note: Don't use debug=True in production
    app.run(host='0.0.0.0', port=port, debug=False)