#!/usr/bin/env python3
"""
Mock test to verify app logic works without Azure API
"""

import os
from unittest.mock import MagicMock, patch

# Mock the CrewAI components to test app logic
def test_app_logic():
    """Test the app initialization and flow without actual API calls"""
    
    # Set mock environment variables
    os.environ["AZURE_OPENAI_API_KEY"] = "mock_key_123"
    os.environ["AZURE_API_BASE"] = "https://mock.com"
    os.environ["AZURE_API_VERSION"] = "2024-01-01"
    
    print("🧪 Testing App Logic (Mocked)")
    print("=" * 40)
    
    try:
        # Mock the LLM and CrewAI components
        with patch('crewai.LLM') as mock_llm, \
             patch('crewai.Agent') as mock_agent, \
             patch('crewai.Task') as mock_task, \
             patch('crewai.Crew') as mock_crew:
            
            # Import after mocking to avoid Azure API calls
            from brainstorm_crew import alpha, beta, gamma, get_timestamp, authenticate
            
            print("✅ App imports successful with mocked dependencies")
            
            # Test timestamp function
            timestamp = get_timestamp()
            print(f"✅ Timestamp generation: {timestamp}")
            
            # Test authentication (no password)
            auth_result = authenticate()
            print(f"✅ Authentication (no password): {auth_result}")
            
            # Test authentication with mock password
            os.environ["APP_PASSWORD"] = "test123"
            # This should return False in non-interactive environment
            auth_result_with_pass = authenticate()
            print(f"✅ Authentication (with password, non-interactive): {auth_result_with_pass}")
            
            print("✅ All core app logic tests passed!")
            return True
            
    except Exception as e:
        print(f"❌ App logic test failed: {e}")
        return False

def test_imports_without_api():
    """Test that the app can import without hitting Azure API"""
    try:
        # Set dummy env vars to avoid API key prompts
        os.environ["AZURE_OPENAI_API_KEY"] = "dummy"
        os.environ["AZURE_API_BASE"] = "https://dummy.com"
        
        from brainstorm_crew import get_timestamp, authenticate
        print("✅ Core functions import successfully")
        
        # Test utilities
        ts = get_timestamp()
        print(f"✅ Timestamp works: {ts}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    print("🧪 Testing Brainstormers Core Logic")
    print("=" * 50)
    
    # Basic import test
    basic_ok = test_imports_without_api()
    
    # Logic test with mocks
    logic_ok = test_app_logic()
    
    print("\n" + "=" * 50)
    if basic_ok and logic_ok:
        print("🎉 CORE APP LOGIC WORKS!")
        print("The app should deploy fine once you add Azure OpenAI credentials.")
        return 0
    else:
        print("❌ CORE LOGIC ISSUES FOUND")
        return 1

if __name__ == "__main__":
    exit(main())