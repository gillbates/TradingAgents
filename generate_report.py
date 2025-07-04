#!/usr/bin/env python3
"""
TradingAgents PDF Report Generator

This script generates a comprehensive PDF trading report using the TradingAgents framework
with hardcoded API keys and stock symbol for demonstration purposes.
"""

import os
import sys
from datetime import datetime, date
from pathlib import Path
import json

# Set hardcoded API keys (replace with your actual keys)
FINNHUB_API_KEY = "your_finnhub_api_key_here"  # Get free key from https://finnhub.io/
OPENAI_API_KEY = "your_openai_api_key_here"    # Get key from https://platform.openai.com/api-keys

# Validate and set API keys
if FINNHUB_API_KEY == "your_finnhub_api_key_here":
    print("ERROR: Please replace FINNHUB_API_KEY with your actual FinnHub API key!")
    print("Get a free key from: https://finnhub.io/")
    sys.exit(1)

if OPENAI_API_KEY == "your_openai_api_key_here":
    print("ERROR: Please replace OPENAI_API_KEY with your actual OpenAI API key!")
    print("Get a key from: https://platform.openai.com/api-keys")
    sys.exit(1)

os.environ["FINNHUB_API_KEY"] = FINNHUB_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Import TradingAgents after setting environment variables
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

# PDF generation imports
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
except ImportError:
    print("Error: reportlab is required for PDF generation.")
    print("Please install it with: pip install reportlab")
    sys.exit(1)


class TradingReportGenerator:
    """Generates comprehensive PDF trading reports using TradingAgents framework."""
    
    def __init__(self, stock_symbol="AAPL", analysis_date=None):
        """
        Initialize the report generator.
        
        Args:
            stock_symbol: Stock ticker symbol to analyze (default: AAPL)
            analysis_date: Date for analysis (default: today)
        """
        self.stock_symbol = stock_symbol.upper()
        self.analysis_date = analysis_date or date.today().strftime("%Y-%m-%d")
        
        # Configure TradingAgents
        self.config = DEFAULT_CONFIG.copy()
        self.config["llm_provider"] = "openai"
        self.config["deep_think_llm"] = "gpt-4o-mini"  # Use cost-effective model
        self.config["quick_think_llm"] = "gpt-4o-mini"
        self.config["max_debate_rounds"] = 1
        self.config["online_tools"] = True
        
        # Initialize TradingAgents
        self.trading_agents = TradingAgentsGraph(debug=True, config=self.config)
        
        # PDF styling
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom styles for the PDF report."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
            borderWidth=1,
            borderColor=colors.darkblue,
            borderPadding=5
        ))
        
        # Subsection header style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=12,
            textColor=colors.darkgreen
        ))
        
        # Decision style (for final trading decision)
        self.styles.add(ParagraphStyle(
            name='Decision',
            parent=self.styles['Normal'],
            fontSize=14,
            spaceAfter=12,
            alignment=TA_CENTER,
            textColor=colors.red,
            fontName='Helvetica-Bold'
        ))
    
    def run_analysis(self):
        """Run the TradingAgents analysis and return the results."""
        print(f"Running TradingAgents analysis for {self.stock_symbol} on {self.analysis_date}...")
        
        try:
            # Run the analysis
            final_state, decision = self.trading_agents.propagate(
                self.stock_symbol, 
                self.analysis_date
            )
            
            print(f"Analysis completed. Final decision: {decision}")
            return final_state, decision
            
        except Exception as e:
            print(f"Error during analysis: {str(e)}")
            raise
    
    def _clean_text_for_pdf(self, text):
        """Clean and format text for PDF generation."""
        if not text:
            return "No data available."
        
        # Remove excessive whitespace and normalize
        text = ' '.join(text.split())
        
        # Escape special characters for reportlab
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        
        return text
    
    def _create_summary_table(self, final_state, decision):
        """Create a summary table with key information."""
        data = [
            ['Stock Symbol', self.stock_symbol],
            ['Analysis Date', self.analysis_date],
            ['Final Decision', decision],
            ['Generated On', datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        table = Table(data, colWidths=[2*inch, 3*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        return table
    
    def generate_pdf_report(self, final_state, decision, output_filename=None):
        """Generate a comprehensive PDF report from the analysis results."""
        
        if output_filename is None:
            output_filename = f"trading_report_{self.stock_symbol}_{self.analysis_date}.pdf"
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build the story (content)
        story = []
        
        # Title
        title = f"TradingAgents Analysis Report: {self.stock_symbol}"
        story.append(Paragraph(title, self.styles['CustomTitle']))
        story.append(Spacer(1, 20))
        
        # Summary table
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        story.append(self._create_summary_table(final_state, decision))
        story.append(Spacer(1, 20))
        
        # Final Trading Decision (highlighted)
        story.append(Paragraph("FINAL TRADING DECISION", self.styles['SectionHeader']))
        decision_text = f"<b>{decision}</b>"
        story.append(Paragraph(decision_text, self.styles['Decision']))
        story.append(Spacer(1, 20))
        
        # Market Analysis Report
        if final_state.get("market_report"):
            story.append(Paragraph("Market Analysis Report", self.styles['SectionHeader']))
            market_text = self._clean_text_for_pdf(final_state["market_report"])
            story.append(Paragraph(market_text, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Sentiment Analysis Report
        if final_state.get("sentiment_report"):
            story.append(Paragraph("Sentiment Analysis Report", self.styles['SectionHeader']))
            sentiment_text = self._clean_text_for_pdf(final_state["sentiment_report"])
            story.append(Paragraph(sentiment_text, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # News Analysis Report
        if final_state.get("news_report"):
            story.append(Paragraph("News Analysis Report", self.styles['SectionHeader']))
            news_text = self._clean_text_for_pdf(final_state["news_report"])
            story.append(Paragraph(news_text, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Fundamentals Analysis Report
        if final_state.get("fundamentals_report"):
            story.append(Paragraph("Fundamentals Analysis Report", self.styles['SectionHeader']))
            fundamentals_text = self._clean_text_for_pdf(final_state["fundamentals_report"])
            story.append(Paragraph(fundamentals_text, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Page break before detailed analysis
        story.append(PageBreak())
        
        # Investment Debate Summary
        if final_state.get("investment_debate_state"):
            story.append(Paragraph("Investment Debate Summary", self.styles['SectionHeader']))
            
            debate_state = final_state["investment_debate_state"]
            if hasattr(debate_state, 'get'):
                judge_decision = debate_state.get("judge_decision", "")
                if judge_decision:
                    story.append(Paragraph("Judge Decision:", self.styles['SubsectionHeader']))
                    judge_text = self._clean_text_for_pdf(judge_decision)
                    story.append(Paragraph(judge_text, self.styles['Normal']))
                    story.append(Spacer(1, 10))
        
        # Trader Investment Plan
        if final_state.get("trader_investment_plan"):
            story.append(Paragraph("Trader Investment Plan", self.styles['SectionHeader']))
            trader_text = self._clean_text_for_pdf(final_state["trader_investment_plan"])
            story.append(Paragraph(trader_text, self.styles['Normal']))
            story.append(Spacer(1, 15))
        
        # Risk Assessment
        if final_state.get("risk_debate_state"):
            story.append(Paragraph("Risk Assessment", self.styles['SectionHeader']))
            
            risk_state = final_state["risk_debate_state"]
            if hasattr(risk_state, 'get'):
                risk_judge_decision = risk_state.get("judge_decision", "")
                if risk_judge_decision:
                    story.append(Paragraph("Risk Management Decision:", self.styles['SubsectionHeader']))
                    risk_text = self._clean_text_for_pdf(risk_judge_decision)
                    story.append(Paragraph(risk_text, self.styles['Normal']))
                    story.append(Spacer(1, 10))
        
        # Final Trade Decision Details
        if final_state.get("final_trade_decision"):
            story.append(Paragraph("Detailed Final Trade Decision", self.styles['SectionHeader']))
            final_decision_text = self._clean_text_for_pdf(final_state["final_trade_decision"])
            story.append(Paragraph(final_decision_text, self.styles['Normal']))
        
        # Build the PDF
        doc.build(story)
        print(f"PDF report generated: {output_filename}")
        return output_filename


def main():
    """Main function to run the report generation."""
    
    # Configuration
    STOCK_SYMBOL = "AAPL"  # Hardcoded stock symbol
    ANALYSIS_DATE = "2024-12-01"  # Hardcoded analysis date
    
    print("TradingAgents PDF Report Generator")
    print("=" * 50)
    print(f"Stock Symbol: {STOCK_SYMBOL}")
    print(f"Analysis Date: {ANALYSIS_DATE}")
    print("=" * 50)
    
    try:
        # Create report generator
        generator = TradingReportGenerator(
            stock_symbol=STOCK_SYMBOL,
            analysis_date=ANALYSIS_DATE
        )
        
        # Run analysis
        final_state, decision = generator.run_analysis()
        
        # Generate PDF report
        output_file = generator.generate_pdf_report(final_state, decision)
        
        print(f"\nReport generation completed successfully!")
        print(f"Output file: {output_file}")
        print(f"Final trading decision: {decision}")
        
    except Exception as e:
        print(f"Error generating report: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
