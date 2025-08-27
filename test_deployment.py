#!/usr/bin/env python3
"""
Test script to verify deployment readiness
"""

import os
import sys

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import crewai
        print("✅ CrewAI import successful")
        
        from langchain_openai import ChatOpenAI  
        print("✅ LangChain OpenAI import successful")
        
        from datetime import datetime
        print("✅ Standard library imports successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_environment():
    """Test environment variable configuration"""
    required_vars = ["AZURE_OPENAI_API_KEY", "AZURE_API_BASE", "AZURE_API_VERSION"]
    
    print("\n📋 Environment Variables Check:")
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if "key" in var.lower():
                print(f"✅ {var}: ***hidden***")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var}: Not set")
            all_good = False
    
    # Optional vars
    optional_vars = ["APP_PASSWORD", "AZURE_MODEL_NAME", "TEMPERATURE"]
    print("\n📋 Optional Environment Variables:")
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            if "password" in var.lower() or "key" in var.lower():
                print(f"✅ {var}: ***hidden***")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"ℹ️  {var}: Not set (using defaults)")
    
    return all_good

def test_files():
    """Test if required files exist"""
    required_files = [
        "brainstorm_crew.py",
        "brainstorm_gui.py", 
        "app.py",
        "requirements.txt",
        ".env.example"
    ]
    
    print("\n📋 Required Files Check:")
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}: Found")
        else:
            print(f"❌ {file}: Missing")
            all_good = False
    
    return all_good

def main():
    print("🧪 Testing Brainstormers Deployment Readiness")
    print("=" * 50)
    
    # Test imports
    imports_ok = test_imports()
    
    # Test environment
    env_ok = test_environment() 
    
    # Test files
    files_ok = test_files()
    
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT READINESS SUMMARY:")
    
    if imports_ok and files_ok:
        if env_ok:
            print("🎉 READY FOR DEPLOYMENT!")
            print("All checks passed. You can deploy this app.")
        else:
            print("⚠️  MISSING ENVIRONMENT VARIABLES")
            print("App structure is good, but you need to set environment variables in your deployment platform.")
        return 0
    else:
        print("❌ NOT READY FOR DEPLOYMENT")
        print("Please fix the issues above before deploying.")
        return 1

if __name__ == "__main__":
    exit(main())