# main.py
"""
M&A Due Diligence Automation System
Main entry point for the application.
"""

import os
import sys
import json
import time
from datetime import datetime

# Add modules to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.data_sources import DataSourceManager, resolve_company
from modules.financial_analysis import FinancialAnalyzer
from modules.market_data import MarketDataAnalyzer
from modules.corporate_filings import CorporateFilingsAnalyzer
from modules.legal_analysis import LegalAnalyzer
from modules.patent_analysis import PatentAnalyzer
from modules.news_analysis import NewsAnalyzer
from modules.risk_engine import RiskEngine
from modules.valuation import ValuationAnalyzer
from modules.report_generator import ReportGenerator

class DueDiligenceSystem:
    """Main M&A Due Diligence System orchestrator."""
    
    def __init__(self):
        self.dsm = DataSourceManager()
        self.modules = {
            "financial_analysis": FinancialAnalyzer(),
            "market_data": MarketDataAnalyzer(),
            "corporate_filings": CorporateFilingsAnalyzer(),
            "legal_analysis": LegalAnalyzer(),
            "patent_analysis": PatentAnalyzer(),
            "news_analysis": NewsAnalyzer(),
            "risk_engine": RiskEngine(),
            "valuation": ValuationAnalyzer(),
        }
        self.report_generator = ReportGenerator()
    
    def display_banner(self):
        """Display system banner."""
        print("""
╔══════════════════════════════════════════════════════════════════╗
║           M&A DUE DILIGENCE AUTOMATION SYSTEM                    ║
║                                                                  ║
║  AI-Assisted Intelligence for Indian Listed Companies           ║
║  ─────────────────────────────────────────────────────────────   ║
║  Version: 1.0.0-MVP                                              ║
║  Platform: Android Termux | Python 3                              ║
║  Data Sources: NSE, BSE, Public Records (Free Tier)              ║
╚══════════════════════════════════════════════════════════════════╝
        """)
        print("⚠️  DISCLAIMER: This tool provides analyst assistance only.")
        print("   Not a replacement for legal/financial advisors.\n")
    
    def get_user_input(self):
        """Get company identifier from user."""
        print("─" * 60)
        print("COMPANY IDENTIFICATION")
        print("─" * 60)
        print("Enter one of the following:")
        print("  • NSE Symbol (e.g., INFY, RELIANCE, TCS)")
        print("  • BSE Code (e.g., 500209, 500325)")
        print("  • Company Name (e.g., 'Infosys', 'Reliance Industries')")
        print("  • Type 'list' to see available companies")
        print("  • Type 'quit' to exit")
        print("─" * 60)
        
        while True:
            user_input = input("\n> ").strip().upper()
            
            if user_input == 'QUIT':
                return None
            
            if user_input == 'LIST':
                print("\nAvailable Companies (Sample):")
                print("─" * 40)
                from modules.data_sources import COMPANY_SYMBOLS
                for sym, info in sorted(COMPANY_SYMBOLS.items())[:10]:
                    print(f"  {sym:<12} → {info['name']}")
                print(f"  ... and {len(COMPANY_SYMBOLS) - 10} more")
                continue
            
            company_info = resolve_company(user_input)
            
            if company_info:
                print(f"\n✓ Resolved: {company_info['name']}")
                print(f"  NSE: {company_info['nse']} | BSE: {company_info['bse']}")
                confirm = input("Proceed with analysis? (Y/n): ").strip().lower()
                if confirm != 'n':
                    return company_info
            else:
                print(f"\n✗ Could not resolve '{user_input}'")
                print("  Try using exact NSE symbol or BSE code")
                print("  Example: INFY, RELIANCE, TCS, HDFCBANK")
    
    def run_analysis(self, company_info):
        """Execute full due diligence analysis."""
        print("\n" + "═" * 60)
        print("INITIATING DUE DILIGENCE ANALYSIS")
        print("═" * 60)
        
        results = {}
        start_time = time.time()
        
        # Run all modules
        modules_to_run = [
            ("Financial Analysis", "financial_analysis", lambda m: m.analyze(company_info)),
            ("Market Data", "market_data", lambda m: m.analyze(company_info)),
            ("Corporate Filings", "corporate_filings", lambda m: m.analyze(company_info)),
            ("Legal Analysis", "legal_analysis", lambda m: m.analyze(company_info)),
            ("Patent & IP", "patent_analysis", lambda m: m.analyze(company_info)),
            ("News Intelligence", "news_analysis", lambda m: m.analyze(company_info)),
        ]
        
        for name, key, runner in modules_to_run:
            print(f"\n  ▶ {name}...", end=" ", flush=True)
            try:
                result = runner(self.modules[key])
                results[key] = result
                status = "✓" if not result.get("error") else "⚠"
                print(f"{status}")
                
                if result.get("error"):
                    print(f"    Warning: {result['error']}")
                
                # Rate limiting between modules
                time.sleep(1.5)
                
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                results[key] = self.dsm.create_standard_response(
                    data={}, source=name, confidence=0.0, error=str(e)
                )
        
        # Run risk engine (depends on other modules)
        print(f"\n  ▶ Risk Engine...", end=" ", flush=True)
        try:
            risk_result = self.modules["risk_engine"].analyze(
                results["financial_analysis"],
                results["legal_analysis"],
                results["market_data"],
                results["corporate_filings"],
                results["news_analysis"]
            )
            results["risk_engine"] = risk_result
            print("✓")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results["risk_engine"] = self.dsm.create_standard_response(
                data={}, source="Risk Engine", confidence=0.0, error=str(e)
            )
        
        # Run valuation (depends on financial and market data)
        print(f"  ▶ Valuation Models...", end=" ", flush=True)
        try:
            val_result = self.modules["valuation"].analyze(
                results["financial_analysis"],
                results["market_data"]
            )
            results["valuation"] = val_result
            print("✓")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
            results["valuation"] = self.dsm.create_standard_response(
                data={}, source="Valuation", confidence=0.0, error=str(e)
            )
        
        elapsed = time.time() - start_time
        print(f"\n{'═' * 60}")
        print(f"ANALYSIS COMPLETE in {elapsed:.1f} seconds")
        print(f"{'═' * 60}")
        
        return results
    
    def display_summary(self, results):
        """Display analysis summary in terminal."""
        print("\n" + "─" * 60)
        print("QUICK SUMMARY")
        print("─" * 60)
        
        # Risk overview
        risk_data = results.get("risk_engine", {}).get("data", {})
        overall = risk_data.get("overall_risk", {})
        print(f"\nOverall Risk: {overall.get('level', 'UNKNOWN')} ({overall.get('score', 0):.1f}/100)")
        
        categories = overall.get("category_breakdown", {})
        for cat, info in categories.items():
            print(f"  • {cat.replace('_', ' ').title():15} {info.get('level', 'N/A'):8} ({info.get('score', 0):.1f})")
        
        # Valuation
        val_data = results.get("valuation", {}).get("data", {})
        summary = val_data.get("summary", {})
        if summary.get("dcf_value_per_share"):
            print(f"\nIndicative Valuation: ₹{summary['dcf_value_per_share']:.2f} (DCF)")
        
        # Key red flags count
        red_flags = 0
        fin_data = results.get("financial_analysis", {}).get("data", {})
        red_flags += len([i for i in fin_data.get("ratios", {}).get("insights", []) 
                         if i.get("risk_level") == "HIGH"])
        filings_data = results.get("corporate_filings", {}).get("data", {})
        red_flags += len(filings_data.get("red_flags", []))
        
        if red_flags > 0:
            print(f"\n⚠️  {red_flags} red flag(s) identified - see full report")
        else:
            print(f"\n✓ No critical red flags identified")
    
    def generate_report(self, company_info, results):
        """Generate and save PDF report."""
        print("\n" + "─" * 60)
        print("GENERATING PDF REPORT")
        print("─" * 60)
        
        try:
            filepath = self.report_generator.generate_report(company_info, results)
            print(f"\n✓ Report saved: {filepath}")
            
            # Also save JSON for programmatic access
            json_path = filepath.replace(".pdf", ".json")
            with open(json_path, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"✓ Raw data saved: {json_path}")
            
            return filepath
            
        except Exception as e:
            print(f"\n✗ Report generation failed: {str(e)}")
            # Fallback: save JSON only
            try:
                fallback_path = os.path.join(
                    self.report_generator.output_path,
                    f"{company_info['name'].replace(' ', '_')}_data.json"
                )
                with open(fallback_path, 'w') as f:
                    json.dump(results, f, indent=2, default=str)
                print(f"✓ Data saved (JSON only): {fallback_path}")
                return fallback_path
            except Exception as e2:
                print(f"✗ Fallback save failed: {str(e2)}")
                return None
    
    def run(self):
        """Main application loop."""
        self.display_banner()
        
        while True:
            company_info = self.get_user_input()
            
            if company_info is None:
                print("\nThank you for using M&A Due Diligence System.")
                print("Exiting...\n")
                break
            
            # Run analysis
            results = self.run_analysis(company_info)
            
            # Display summary
            self.display_summary(results)
            
            # Generate report
            report_path = self.generate_report(company_info, results)
            
            print("\n" + "─" * 60)
            next_action = input("Analyze another company? (Y/n): ").strip().lower()
            if next_action == 'n':
                print("\nThank you for using M&A Due Diligence System.")
                print("Exiting...\n")
                break


def main():
    """Entry point."""
    try:
        system = DueDiligenceSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
