# modules/valuation.py
"""
M&A Due Diligence - Valuation Module
Provides indicative valuation estimates.
"""

import json
import numpy as np
from datetime import datetime
from modules.data_sources import DataSourceManager

class ValuationAnalyzer:
    """Calculates indicative valuation metrics."""
    
    def __init__(self):
        self.dsm = DataSourceManager()
    
    def dcf_valuation(self, financial_data, assumptions=None):
        """Calculate DCF-based valuation."""
        if assumptions is None:
            assumptions = {
                "growth_rate_5yr": 0.12,
                "terminal_growth": 0.03,
                "discount_rate": 0.12,
                "tax_rate": 0.25
            }
        
        # Get latest financials
        pl = financial_data.get("profit_loss", [])
        cf = financial_data.get("cash_flow", [])
        
        if not pl or not cf:
            return {
                "value_per_share": None,
                "enterprise_value_cr": None,
                "method": "DCF",
                "error": "Insufficient financial data"
            }
        
        latest_pl = pl[-1]
        latest_cf = cf[-1]
        
        # Project FCF for 5 years
        fcf = latest_cf.get("operating_cash_flow", 0) * 0.7  # Approximate FCF
        growth = assumptions["growth_rate_5yr"]
        terminal_g = assumptions["terminal_growth"]
        discount = assumptions["discount_rate"]
        
        projected_fcfs = []
        pv_fcfs = []
        
        for year in range(1, 6):
            fcf_proj = fcf * ((1 + growth) ** year)
            pv = fcf_proj / ((1 + discount) ** year)
            projected_fcfs.append(round(fcf_proj, 2))
            pv_fcfs.append(round(pv, 2))
        
        # Terminal value
        terminal_value = (projected_fcfs[-1] * (1 + terminal_g)) / (discount - terminal_g)
        pv_terminal = terminal_value / ((1 + discount) ** 5)
        
        enterprise_value = sum(pv_fcfs) + pv_terminal
        
        # Equity value (simplified)
        equity_value = enterprise_value - latest_pl.get("revenue", 0) * 0.15  # Approximate debt
        
        return {
            "method": "Discounted Cash Flow (DCF)",
            "enterprise_value_cr": round(enterprise_value, 2),
            "equity_value_cr": round(max(equity_value, 0), 2),
            "value_per_share": round(equity_value / 100, 2),  # Assuming 100cr shares
            "projected_fcfs": projected_fcfs,
            "pv_fcfs": pv_fcfs,
            "terminal_value": round(terminal_value, 2),
            "pv_terminal": round(pv_terminal, 2),
            "assumptions": assumptions,
            "disclaimer": "Indicative valuation only. Not investment advice.",
            "confidence": 0.50
        }
    
    def comparable_valuation(self, market_data, financial_data):
        """Calculate comparable company valuation."""
        mdata = market_data.get("market_data", {})
        
        pe = mdata.get("pe_ratio", 25)
        pb = mdata.get("pb_ratio", 4)
        
        # Get latest EPS and Book Value
        pl = financial_data.get("profit_loss", [])
        bs = financial_data.get("balance_sheet", [])
        
        if not pl or not bs:
            return {
                "error": "Insufficient data for comparable valuation"
            }
        
        latest_pl = pl[-1]
        latest_bs = bs[-1]
        
        # Calculate implied values
        net_profit = latest_pl.get("net_profit", 0)
        equity = latest_bs.get("equity", 0)
        
        # Shares outstanding (estimated)
        shares_cr = 100  # Simplified assumption
        
        eps = net_profit / shares_cr
        bvps = equity / shares_cr
        
        pe_value = eps * pe
        pb_value = bvps * pb
        
        # Revenue multiple
        revenue = latest_pl.get("revenue", 0)
        revenue_multiple = 3.5  # Industry average
        rev_value = (revenue / shares_cr) * revenue_multiple
        
        return {
            "method": "Comparable Company Analysis",
            "pe_based_value": round(pe_value, 2),
            "pb_based_value": round(pb_value, 2),
            "revenue_multiple_value": round(rev_value, 2),
            "average_value": round((pe_value + pb_value + rev_value) / 3, 2),
            "multiples_used": {
                "pe_ratio": pe,
                "pb_ratio": pb,
                "revenue_multiple": revenue_multiple
            },
            "disclaimer": "Indicative valuation only. Not investment advice.",
            "confidence": 0.55
        }
    
    def analyze(self, financial_data, market_data, custom_assumptions=None):
        """Main valuation method."""
        try:
            fin_data = financial_data.get("data", {}).get("financial_statements", {})
            mkt_data = market_data.get("data", {})
            
            dcf = self.dcf_valuation(fin_data, custom_assumptions)
            comparable = self.comparable_valuation(mkt_data, fin_data)
            
            return self.dsm.create_standard_response(
                data={
                    "dcf_valuation": dcf,
                    "comparable_valuation": comparable,
                    "summary": {
                        "dcf_value_per_share": dcf.get("value_per_share"),
                        "comparable_avg_value": comparable.get("average_value"),
                        "valuation_range": {
                            "low": min(dcf.get("value_per_share", 0), comparable.get("average_value", 0)),
                            "high": max(dcf.get("value_per_share", 0), comparable.get("average_value", 0))
                        }
                    }
                },
                source="Valuation Models",
                confidence=0.50
            )
        except Exception as e:
            return self.dsm.create_standard_response(
                data={},
                source="Valuation",
                confidence=0.0,
                error=str(e)
            )
