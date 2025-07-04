# TradingAgents PDF Report Generator

This document explains how to use the PDF report generation functionality for the TradingAgents framework.

## Overview

The `generate_report.py` script creates comprehensive PDF trading reports using the TradingAgents multi-agent framework. It analyzes a stock using specialized AI agents and generates a professional PDF report with all findings and recommendations.

## Features

- **Comprehensive Analysis**: Utilizes all TradingAgents specialists (market, sentiment, news, fundamentals analysts)
- **Professional PDF Output**: Generates well-formatted PDF reports with proper styling
- **Hardcoded Configuration**: Easy to use with predefined settings for demonstration
- **Detailed Reporting**: Includes executive summary, detailed analysis, and final trading decisions

## Prerequisites

### 1. Install Dependencies

Make sure you have installed all required dependencies:

```bash
pip install -r requirements.txt
```

The report generator specifically requires:
- `reportlab` for PDF generation
- All TradingAgents dependencies (langchain, openai, finnhub, etc.)

### 2. API Keys Required

You need two API keys:

#### FinnHub API Key (Free)
1. Go to [https://finnhub.io/](https://finnhub.io/)
2. Sign up for a free account
3. Get your API key from the dashboard

#### OpenAI API Key (Paid)
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create an account and add billing information
3. Generate an API key

**Note**: The script uses `gpt-4o-mini` model to minimize costs, but you'll still need OpenAI credits.

## Usage

### Method 1: Direct Script Usage

1. **Edit API Keys**: Open `generate_report.py` and replace the placeholder API keys:

```python
os.environ["FINNHUB_API_KEY"] = "your_actual_finnhub_api_key_here"
os.environ["OPENAI_API_KEY"] = "your_actual_openai_api_key_here"
```

2. **Run the Script**:

```bash
python generate_report.py
```

### Method 2: Using Example Script (Recommended)

1. **Edit API Keys**: Open `example_usage.py` and replace the placeholder API keys in the `setup_api_keys()` function:

```python
FINNHUB_API_KEY = "your_actual_finnhub_api_key_here"
OPENAI_API_KEY = "your_actual_openai_api_key_here"
```

2. **Customize Settings** (optional):

```python
selected_stock = "AAPL"  # Change to any valid stock symbol
analysis_date = "2024-12-01"  # Change to desired analysis date
```

3. **Run the Example**:

```bash
python example_usage.py
```

### Method 3: Programmatic Usage

```python
from generate_report import TradingReportGenerator
import os

# Set API keys
os.environ["FINNHUB_API_KEY"] = "your_key_here"
os.environ["OPENAI_API_KEY"] = "your_key_here"

# Create generator
generator = TradingReportGenerator(
    stock_symbol="AAPL",
    analysis_date="2024-12-01"
)

# Run analysis and generate report
final_state, decision = generator.run_analysis()
output_file = generator.generate_pdf_report(final_state, decision)

print(f"Report generated: {output_file}")
print(f"Trading decision: {decision}")
```

## Configuration Options

### Stock Symbols
You can analyze any valid stock symbol:
- `AAPL` (Apple)
- `NVDA` (NVIDIA)
- `TSLA` (Tesla)
- `MSFT` (Microsoft)
- `GOOGL` (Google)
- Any other valid ticker symbol

### Analysis Date
- Use format: `YYYY-MM-DD`
- Can be historical dates or recent dates
- Avoid dates too far in the future

### LLM Configuration
The script uses cost-effective models by default:
- `deep_think_llm`: `gpt-4o-mini`
- `quick_think_llm`: `gpt-4o-mini`

You can modify these in the `TradingReportGenerator.__init__()` method.

## Output

### PDF Report Structure

The generated PDF report includes:

1. **Executive Summary**
   - Stock symbol and analysis date
   - Final trading decision (BUY/SELL/HOLD)
   - Generation timestamp

2. **Market Analysis Report**
   - Technical indicators analysis
   - Price trend analysis
   - Market conditions assessment

3. **Sentiment Analysis Report**
   - Social media sentiment
   - Market sentiment indicators
   - Public opinion analysis

4. **News Analysis Report**
   - Recent news impact
   - Macroeconomic factors
   - Industry-specific news

5. **Fundamentals Analysis Report**
   - Financial metrics
   - Company performance
   - Insider sentiment and transactions

6. **Investment Debate Summary**
   - Bull vs bear arguments
   - Judge decision rationale

7. **Risk Assessment**
   - Risk management evaluation
   - Portfolio impact analysis

8. **Detailed Final Trade Decision**
   - Complete reasoning
   - Supporting evidence
   - Risk considerations

### File Naming
Reports are saved as: `trading_report_{SYMBOL}_{DATE}.pdf`

Example: `trading_report_AAPL_2024-12-01.pdf`

## Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify your API keys are correct
   - Check that you have sufficient credits/quota
   - Ensure keys are properly set in environment variables

2. **Import Errors**
   - Run `pip install -r requirements.txt`
   - Make sure you're in the correct virtual environment

3. **PDF Generation Errors**
   - Install reportlab: `pip install reportlab`
   - Check file permissions in the output directory

4. **Analysis Timeout**
   - The analysis can take 5-10 minutes
   - Ensure stable internet connection
   - Try with a different stock symbol or date

### Performance Tips

1. **Cost Optimization**
   - The script uses `gpt-4o-mini` to minimize costs
   - Each report typically costs $0.10-$0.50 in API calls

2. **Speed Optimization**
   - Set `max_debate_rounds = 1` for faster analysis
   - Use `online_tools = True` for real-time data

## Example Output

When successful, you'll see output like:

```
TradingAgents PDF Report Generator
==================================================
Stock Symbol: AAPL
Analysis Date: 2024-12-01
==================================================
Running TradingAgents analysis for AAPL on 2024-12-01...
Analysis completed. Final decision: BUY
PDF report generated: trading_report_AAPL_2024-12-01.pdf

Report generation completed successfully!
Output file: trading_report_AAPL_2024-12-01.pdf
Final trading decision: BUY
```

## Support

For issues related to:
- **TradingAgents Framework**: Check the main README.md
- **API Keys**: Visit FinnHub.io or OpenAI documentation
- **PDF Generation**: Check reportlab documentation
- **Report Generator**: Review this document or examine the code comments

## Disclaimer

This tool is for research and educational purposes only. The generated reports should not be considered as financial advice. Always consult with qualified financial advisors before making investment decisions.
