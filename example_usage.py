#!/usr/bin/env python3
"""
Example usage of the TradingAgents PDF Report Generator

This script demonstrates how to use the generate_report.py script with proper API key configuration.
"""

import os
import sys
from datetime import date

from generate_report import TradingReportGenerator


def setup_api_keys():
    """
    Setup API keys for TradingAgents.
    
    IMPORTANT: Replace these with your actual API keys before running!
    """
    
    # FinnHub API Key (get free key from https://finnhub.io/)
    FINNHUB_API_KEY = "your_actual_finnhub_api_key_here"
    
    # OpenAI API Key (get from https://platform.openai.com/api-keys)
    OPENAI_API_KEY = "your_actual_openai_api_key_here"
    
    # Validate API keys
    if FINNHUB_API_KEY == "your_actual_finnhub_api_key_here":
        print("ERROR: Please replace FINNHUB_API_KEY with your actual FinnHub API key!")
        print("Get a free key from: https://finnhub.io/")
        return False
    
    if OPENAI_API_KEY == "your_actual_openai_api_key_here":
        print("ERROR: Please replace OPENAI_API_KEY with your actual OpenAI API key!")
        print("Get a key from: https://platform.openai.com/api-keys")
        return False
    
    # Set environment variables
    os.environ["FINNHUB_API_KEY"] = FINNHUB_API_KEY
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
    print("✓ API keys configured successfully!")
    return True

def main():
    """Main function to demonstrate report generation."""
    
    print("TradingAgents PDF Report Generator - Example Usage")
    print("=" * 60)
    
    # Setup API keys
    if not setup_api_keys():
        sys.exit(1)
    
    # Import the report generator after setting up API keys
    try:
        from generate_report import TradingReportGenerator
    except ImportError as e:
        print(f"Error importing generate_report: {e}")
        print("Make sure generate_report.py is in the same directory.")
        sys.exit(1)
    
    # Configuration options
    stock_symbols = ["AAPL", "NVDA", "TSLA", "MSFT", "GOOGL"]
    selected_stock = "NVDA"  # Change this to analyze different stocks
    analysis_date = "2025-07-05"  # Change this to analyze different dates
    
    print(f"Selected Stock: {selected_stock}")
    print(f"Analysis Date: {analysis_date}")
    print(f"Available stocks: {', '.join(stock_symbols)}")
    print("=" * 60)
    
    try:
        # Create report generator
        print("Initializing TradingAgents...")
        generator = TradingReportGenerator(
            stock_symbol=selected_stock,
            analysis_date=analysis_date
        )
        
        # Run analysis
        print("Running comprehensive market analysis...")
        print("This may take several minutes as the agents analyze market data...")
        final_state, decision = generator.run_analysis()
        
        # Generate PDF report
        print("Generating PDF report...")
        output_file = generator.generate_pdf_report(final_state, decision)
        
        print("\n" + "=" * 60)
        print("REPORT GENERATION COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print(f"📊 Stock Analyzed: {selected_stock}")
        print(f"📅 Analysis Date: {analysis_date}")
        print(f"🎯 Final Decision: {decision}")
        print(f"📄 PDF Report: {output_file}")
        print("=" * 60)
        
        # Display summary of what was analyzed
        print("\nReport Contents:")
        print("• Executive Summary with key metrics")
        print("• Market Analysis (technical indicators, price trends)")
        print("• Sentiment Analysis (social media, market sentiment)")
        print("• News Analysis (recent news impact)")
        print("• Fundamentals Analysis (financial metrics)")
        print("• Investment Debate Summary")
        print("• Risk Assessment")
        print("• Final Trading Decision with detailed reasoning")
        
    except Exception as e:
        print(f"\nError generating report: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Ensure your API keys are valid and have sufficient credits")
        print("2. Check your internet connection")
        print("3. Verify the stock symbol is valid")
        print("4. Make sure the analysis date is not too far in the future")
        sys.exit(1)

def generate_multiple_reports():
    """
    Example function to generate reports for multiple stocks.
    Uncomment and modify as needed.
    """
    stocks = ["AAPL", "NVDA", "TSLA"]
    analysis_date = date.today().strftime("%Y-%m-%d")
    
    for stock in stocks:
        print(f"\nGenerating report for {stock}...")
        try:
            generator = TradingReportGenerator(
                stock_symbol=stock,
                analysis_date=analysis_date
            )
            final_state, decision = generator.run_analysis()
            output_file = generator.generate_pdf_report(final_state, decision)
            print(f"✓ Report generated for {stock}: {output_file}")
        except Exception as e:
            print(f"✗ Failed to generate report for {stock}: {e}")

if __name__ == "__main__":
    main()
    
    # Uncomment the line below to generate reports for multiple stocks
    # generate_multiple_reports()
