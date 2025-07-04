#!/usr/bin/env python3
"""
Test script to verify TradingAgents setup and dependencies.

This script checks if all required dependencies are installed and API keys are configured.
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")
    
    required_packages = [
        ("reportlab", "reportlab.lib.pagesizes"),
        ("langchain_openai", "langchain_openai"),
        ("langgraph", "langgraph.prebuilt"),
        ("pandas", "pandas"),
        ("yfinance", "yfinance"),
        ("requests", "requests"),
    ]
    
    missing_packages = []
    
    for package_name, import_path in required_packages:
        try:
            __import__(import_path)
            print(f"✓ {package_name}")
        except ImportError:
            print(f"✗ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    print("✓ All required packages are installed!")
    return True

def test_tradingagents_import():
    """Test if TradingAgents can be imported."""
    print("\nTesting TradingAgents import...")
    
    try:
        from tradingagents.graph.trading_graph import TradingAgentsGraph
        from tradingagents.default_config import DEFAULT_CONFIG
        print("✓ TradingAgents framework imported successfully!")
        return True
    except ImportError as e:
        print(f"✗ Failed to import TradingAgents: {e}")
        print("Make sure you're in the TradingAgents directory and have installed dependencies.")
        return False

def test_api_keys():
    """Test if API keys are configured."""
    print("\nTesting API key configuration...")
    
    finnhub_key = os.getenv("FINNHUB_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not finnhub_key or finnhub_key == "your_finnhub_api_key_here":
        print("✗ FINNHUB_API_KEY not configured")
        print("  Set with: export FINNHUB_API_KEY=your_actual_key")
        print("  Or edit the API key in generate_report.py")
        return False
    else:
        print("✓ FINNHUB_API_KEY configured")
    
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("✗ OPENAI_API_KEY not configured")
        print("  Set with: export OPENAI_API_KEY=your_actual_key")
        print("  Or edit the API key in generate_report.py")
        return False
    else:
        print("✓ OPENAI_API_KEY configured")
    
    return True

def test_api_connectivity():
    """Test basic API connectivity."""
    print("\nTesting API connectivity...")
    
    # Test FinnHub API
    try:
        import requests
        finnhub_key = os.getenv("FINNHUB_API_KEY")
        if finnhub_key and finnhub_key != "your_finnhub_api_key_here":
            response = requests.get(
                f"https://finnhub.io/api/v1/quote?symbol=AAPL&token={finnhub_key}",
                timeout=10
            )
            if response.status_code == 200:
                print("✓ FinnHub API connection successful")
            else:
                print(f"✗ FinnHub API error: {response.status_code}")
                return False
        else:
            print("⚠ Skipping FinnHub test - API key not configured")
    except Exception as e:
        print(f"✗ FinnHub API test failed: {e}")
        return False
    
    # Test OpenAI API
    try:
        from langchain_openai import ChatOpenAI
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key and openai_key != "your_openai_api_key_here":
            llm = ChatOpenAI(model="gpt-4o-mini", max_tokens=10)
            response = llm.invoke("Hello")
            print("✓ OpenAI API connection successful")
        else:
            print("⚠ Skipping OpenAI test - API key not configured")
    except Exception as e:
        print(f"✗ OpenAI API test failed: {e}")
        return False
    
    return True

def test_pdf_generation():
    """Test PDF generation capability."""
    print("\nTesting PDF generation...")
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        
        # Create a simple test PDF
        test_filename = "test_report.pdf"
        doc = SimpleDocTemplate(test_filename, pagesize=letter)
        styles = getSampleStyleSheet()
        
        story = [
            Paragraph("Test PDF Generation", styles['Title']),
            Paragraph("This is a test to verify PDF generation works.", styles['Normal'])
        ]
        
        doc.build(story)
        
        # Check if file was created
        if os.path.exists(test_filename):
            print("✓ PDF generation test successful")
            os.remove(test_filename)  # Clean up
            return True
        else:
            print("✗ PDF file was not created")
            return False
            
    except Exception as e:
        print(f"✗ PDF generation test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("TradingAgents Setup Test")
    print("=" * 50)
    
    tests = [
        ("Package Imports", test_imports),
        ("TradingAgents Import", test_tradingagents_import),
        ("API Keys", test_api_keys),
        ("API Connectivity", test_api_connectivity),
        ("PDF Generation", test_pdf_generation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("✓ All tests passed! You're ready to generate reports.")
        print("\nNext steps:")
        print("1. Edit API keys in generate_report.py or example_usage.py")
        print("2. Run: python generate_report.py")
        print("   or: python example_usage.py")
    else:
        print("✗ Some tests failed. Please fix the issues above before proceeding.")
        print("\nCommon solutions:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Configure API keys in generate_report.py")
        print("- Check internet connectivity")
        sys.exit(1)

if __name__ == "__main__":
    main()
