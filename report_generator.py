# modules/report_generator.py
"""
M&A Due Diligence - Report Generator Module
Generates professional PDF reports using ReportLab.
"""

import os
import json
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.textlabels import Label

class ReportGenerator:
    """Generates professional M&A due diligence reports."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.output_path = "/sdcard/M&A_Reports/"
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist."""
        try:
            os.makedirs(self.output_path, exist_ok=True)
        except:
            # Fallback for non-Android environments
            self.output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "storage", "reports")
            os.makedirs(self.output_path, exist_ok=True)
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            fontSize=24,
            leading=30,
            alignment=TA_CENTER,
            spaceAfter=30,
            textColor=colors.HexColor('#1a365d'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading1',
            fontSize=16,
            leading=20,
            alignment=TA_LEFT,
            spaceAfter=12,
            spaceBefore=12,
            textColor=colors.HexColor('#2c5282'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            fontSize=13,
            leading=16,
            alignment=TA_LEFT,
            spaceAfter=10,
            spaceBefore=10,
            textColor=colors.HexColor('#2b6cb0'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            fontSize=10,
            leading=14,
            alignment=TA_JUSTIFY,
            spaceAfter=8,
            fontName='Helvetica'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskHigh',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#c53030'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskMedium',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#dd6b20'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='RiskLow',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#38a169'),
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            fontSize=9,
            leading=12,
            alignment=TA_JUSTIFY,
            textColor=colors.HexColor('#718096'),
            fontName='Helvetica-Oblique'
        ))
    
    def _create_header_footer(self, canvas, doc):
        """Add header and footer to each page."""
        canvas.saveState()
        
        # Header line
        canvas.setStrokeColor(colors.HexColor('#2c5282'))
        canvas.setLineWidth(2)
        canvas.line(50, A4[1] - 40, A4[0] - 50, A4[1] - 40)
        
        # Footer line
        canvas.line(50, 50, A4[0] - 50, 50)
        
        # Page number
        canvas.setFont('Helvetica', 9)
        canvas.setFillColor(colors.HexColor('#718096'))
        canvas.drawRightString(A4[0] - 50, 35, f"Page {doc.page}")
        
        # Confidential notice
        canvas.drawString(50, 35, "CONFIDENTIAL - DRAFT DUE DILIGENCE REPORT")
        
        canvas.restoreState()
    
    def _create_risk_badge(self, level):
        """Create colored risk badge."""
        color_map = {
            "HIGH": colors.HexColor('#fed7d7'),
            "MEDIUM": colors.HexColor('#feebc8'),
            "LOW": colors.HexColor('#c6f6d5')
        }
        text_color = {
            "HIGH": colors.HexColor('#c53030'),
            "MEDIUM": colors.HexColor('#dd6b20'),
            "LOW": colors.HexColor('#38a169')
        }
        return color_map.get(level, colors.gray), text_color.get(level, colors.black)
    
    def generate_report(self, company_info, analysis_results, output_filename=None):
        """Generate complete PDF report."""
        company_name = company_info.get("name", "Unknown Company")
        
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{company_name.replace(' ', '_')}_{timestamp}_Report.pdf"
        
        filepath = os.path.join(self.output_path, output_filename)
        
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=70,
            bottomMargin=60
        )
        
        story = []
        
        # Build all sections
        story.extend(self._create_cover_page(company_info, analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_executive_summary(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_company_overview(company_info, analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_financial_analysis(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_ratio_dashboard(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_corporate_actions(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_legal_risk(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_ip_analysis(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_news_sentiment(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_red_flags(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_valuation(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_final_risk_rating(analysis_results))
        story.append(PageBreak())
        
        story.extend(self._create_source_appendix(analysis_results))
        
        # Build PDF
        doc.build(story, onFirstPage=self._create_header_footer, 
                 onLaterPages=self._create_header_footer)
        
        return filepath
    
    def _create_cover_page(self, company_info, analysis_results):
        """Create cover page."""
        elements = []
        
        # Title block
        elements.append(Spacer(1, 2*inch))
        elements.append(Paragraph("M&A DUE DILIGENCE", self.styles['CustomTitle']))
        elements.append(Paragraph("INTELLIGENCE REPORT", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Company name
        company_name = company_info.get("name", "")
        elements.append(Paragraph(f"<b>{company_name}</b>", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Identifiers
        nse = company_info.get("nse", "N/A")
        bse = company_info.get("bse", "N/A")
        elements.append(Paragraph(f"NSE: {nse} | BSE: {bse}", self.styles['CustomHeading2']))
        elements.append(Spacer(1, 0.5*inch))
        
        # Report metadata
        elements.append(Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y')}", 
                                 self.styles['CustomBody']))
        elements.append(Paragraph("Classification: CONFIDENTIAL", self.styles['CustomBody']))
        elements.append(Spacer(1, 1*inch))
        
        # Disclaimer box
        disclaimer_data = [[Paragraph(
            "<b>IMPORTANT DISCLAIMER:</b> This report is generated by an AI-assisted "
            "analyst tool for informational purposes only. It does not constitute "
            "investment advice, legal opinion, or a recommendation to buy, sell, or "
            "hold any security. All valuations are indicative and based on publicly "
            "available information. Consult qualified financial and legal advisors "
            "before making any investment decisions.",
            self.styles['Disclaimer']
        )]]
        
        disclaimer_table = Table(disclaimer_data, colWidths=[6*inch])
        disclaimer_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffaf0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#dd6b20')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        elements.append(disclaimer_table)
        
        return elements
    
    def _create_executive_summary(self, analysis_results):
        """Create executive summary section."""
        elements = []
        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        risk_data = analysis_results.get("risk_engine", {}).get("data", {}).get("overall_risk", {})
        overall_score = risk_data.get("score", 0)
        overall_level = risk_data.get("level", "UNKNOWN")
        
        # Risk summary box
        bg_color, text_color = self._create_risk_badge(overall_level)
        
        summary_data = [
            [Paragraph("<b>Overall Risk Rating</b>", self.styles['CustomHeading2']), 
             Paragraph(f"<b>{overall_level}</b>", ParagraphStyle(
                 name='RiskBig', fontSize=20, textColor=text_color, fontName='Helvetica-Bold'
             ))],
            [Paragraph("Risk Score", self.styles['CustomBody']), 
             Paragraph(f"{overall_score}/100", self.styles['CustomBody'])],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), bg_color),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Key findings
        elements.append(Paragraph("KEY FINDINGS", self.styles['CustomHeading2']))
        
        findings = []
        
        # Financial insights
        fin_data = analysis_results.get("financial_analysis", {}).get("data", {})
        ratios = fin_data.get("ratios", {})
        insights = ratios.get("insights", [])
        for insight in insights[:3]:
            risk_style = f"Risk{insight.get('risk_level', 'Low')}"
            findings.append([
                Paragraph("FINANCIAL", self.styles['CustomBody']),
                Paragraph(insight.get("finding", ""), self.styles['CustomBody']),
                Paragraph(insight.get("risk_level", "LOW"), self.styles.get(risk_style, self.styles['CustomBody']))
            ])
        
        # Legal risks
        legal_data = analysis_results.get("legal_analysis", {}).get("data", {})
        risk_assessment = legal_data.get("risk_assessment", {})
        if risk_assessment.get("score", 0) > 0:
            findings.append([
                Paragraph("LEGAL", self.styles['CustomBody']),
                Paragraph(risk_assessment.get("reason", ""), self.styles['CustomBody']),
                Paragraph(risk_assessment.get("level", "LOW"), self.styles['RiskHigh' if risk_assessment.get('level') == 'HIGH' else 'CustomBody'])
            ])
        
        # News sentiment
        news_data = analysis_results.get("news_analysis", {}).get("data", {})
        sentiment = news_data.get("sentiment", {})
        findings.append([
            Paragraph("SENTIMENT", self.styles['CustomBody']),
            Paragraph(f"News sentiment: {sentiment.get('overall_sentiment', 'NEUTRAL')} "
                     f"({sentiment.get('positive_pct', 0):.0f}% positive)", 
                     self.styles['CustomBody']),
            Paragraph("INFO", self.styles['CustomBody'])
        ])
        
        if findings:
            findings_table = Table(findings, colWidths=[1.2*inch, 3.8*inch, 1*inch])
            findings_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#edf2f7')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            elements.append(findings_table)
        
        return elements
    
    def _create_company_overview(self, company_info, analysis_results):
        """Create company overview section."""
        elements = []
        elements.append(Paragraph("COMPANY OVERVIEW", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Basic info table
        market_data = analysis_results.get("market_data", {}).get("data", {}).get("market_data", {})
        
        overview_data = [
            ["Company Name", company_info.get("name", "N/A")],
            ["NSE Symbol", company_info.get("nse", "N/A")],
            ["BSE Code", company_info.get("bse", "N/A")],
            ["Current Price", f"₹{market_data.get('current_price', 'N/A')}"],
            ["Market Cap", f"₹{market_data.get('market_cap_cr', 'N/A'):,.0f} Cr" if market_data.get('market_cap_cr') else "N/A"],
            ["P/E Ratio", f"{market_data.get('pe_ratio', 'N/A')}x"],
            ["Dividend Yield", f"{market_data.get('dividend_yield', 'N/A')}%"],
            ["52-Week Range", f"₹{market_data.get('52_week_low', 'N/A')} - ₹{market_data.get('52_week_high', 'N/A')}"],
        ]
        
        overview_table = Table(overview_data, colWidths=[2*inch, 4*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ]))
        elements.append(overview_table)
        
        return elements
    
    def _create_financial_analysis(self, analysis_results):
        """Create financial analysis section."""
        elements = []
        elements.append(Paragraph("FINANCIAL ANALYSIS", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        fin_data = analysis_results.get("financial_analysis", {}).get("data", {})
        financials = fin_data.get("financial_statements", {})
        
        # P&L Table
        elements.append(Paragraph("Profit & Loss Statement (Last 5 Years)", self.styles['CustomHeading2']))
        
        pl_data = [["Year", "Revenue (Cr)", "EBITDA (Cr)", "Net Profit (Cr)", "Source"]]
        for item in financials.get("profit_loss", []):
            pl_data.append([
                item.get("year", ""),
                f"₹{item.get('revenue', 0):,.2f}",
                f"₹{item.get('ebitda', 0):,.2f}",
                f"₹{item.get('net_profit', 0):,.2f}",
                item.get("source", "")
            ])
        
        pl_table = Table(pl_data, colWidths=[1*inch, 1.3*inch, 1.3*inch, 1.3*inch, 1.1*inch])
        pl_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (3, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(pl_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Balance Sheet
        elements.append(Paragraph("Balance Sheet Summary", self.styles['CustomHeading2']))
        
        bs_data = [["Year", "Total Assets (Cr)", "Equity (Cr)", "Debt (Cr)", "Source"]]
        for item in financials.get("balance_sheet", []):
            bs_data.append([
                item.get("year", ""),
                f"₹{item.get('total_assets', 0):,.2f}",
                f"₹{item.get('equity', 0):,.2f}",
                f"₹{item.get('debt', 0):,.2f}",
                item.get("source", "")
            ])
        
        bs_table = Table(bs_data, colWidths=[1*inch, 1.5*inch, 1.2*inch, 1.2*inch, 1.1*inch])
        bs_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (3, -1), 'RIGHT'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(bs_table)
        
        return elements
    
    def _create_ratio_dashboard(self, analysis_results):
        """Create financial ratio dashboard."""
        elements = []
        elements.append(Paragraph("RATIO DASHBOARD", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        fin_data = analysis_results.get("financial_analysis", {}).get("data", {})
        ratios = fin_data.get("ratios", {})
        
        # Key ratios table
        ratio_categories = [
            ("Revenue Growth %", "revenue_growth"),
            ("EBITDA Margin %", "ebitda_margin"),
            ("Net Profit Margin %", "net_profit_margin"),
            ("ROCE %", "roce"),
            ("Debt/Equity", "debt_equity_ratio"),
            ("Current Ratio", "current_ratio"),
            ("Interest Coverage (x)", "interest_coverage_ratio"),
        ]
        
        ratio_data = [["Metric", "Latest", "Trend", "Assessment"]]
        
        for label, key in ratio_categories:
            values = ratios.get(key, [])
            if values:
                latest = values[-1].get("value", 0)
                trend = "↗" if len(values) > 1 and values[-1]["value"] > values[-2]["value"] else "↘" if len(values) > 1 else "→"
                
                # Simple assessment
                if key == "debt_equity_ratio" and latest > 1:
                    assessment = "HIGH RISK"
                elif key == "interest_coverage_ratio" and latest < 3:
                    assessment = "WATCH"
                elif key == "revenue_growth" and latest < 5:
                    assessment = "SLOW"
                else:
                    assessment = "NORMAL"
                
                ratio_data.append([label, f"{latest:.2f}", trend, assessment])
            else:
                ratio_data.append([label, "N/A", "-", "NO DATA"])
        
        ratio_table = Table(ratio_data, colWidths=[2.2*inch, 1.3*inch, 0.8*inch, 1.7*inch])
        ratio_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(ratio_table)
        
        # Financial insights
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Automated Insights", self.styles['CustomHeading2']))
        
        insights = ratios.get("insights", [])
        for insight in insights:
            risk_style = f"Risk{insight.get('risk_level', 'Low')}"
            elements.append(Paragraph(
                f"• <b>[{insight.get('risk_level', 'INFO')}]</b> {insight.get('finding', '')} "
                f"<i>({insight.get('reason', '')})</i>",
                self.styles.get(risk_style, self.styles['CustomBody'])
            ))
        
        return elements
    
    def _create_corporate_actions(self, analysis_results):
        """Create corporate actions section."""
        elements = []
        elements.append(Paragraph("CORPORATE ACTIONS & FILINGS", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        filings_data = analysis_results.get("corporate_filings", {}).get("data", {})
        filings = filings_data.get("filings", {})
        filings_list = filings.get("filings", [])
        
        if filings_list:
            cf_data = [["Date", "Type", "Title", "Source"]]
            for filing in filings_list[:10]:  # Limit to 10 recent
                cf_data.append([
                    filing.get("date", ""),
                    filing.get("type", ""),
                    Paragraph(filing.get("title", ""), ParagraphStyle(name='Small', fontSize=8)),
                    filing.get("source", "")
                ])
            
            cf_table = Table(cf_data, colWidths=[1*inch, 1.2*inch, 3*inch, 0.8*inch])
            cf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            elements.append(cf_table)
        else:
            elements.append(Paragraph("No recent corporate filings found.", self.styles['CustomBody']))
        
        return elements
    
    def _create_legal_risk(self, analysis_results):
        """Create legal risk analysis section."""
        elements = []
        elements.append(Paragraph("LEGAL RISK ANALYSIS", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        legal_data = analysis_results.get("legal_analysis", {}).get("data", {})
        legal_info = legal_data.get("legal_data", {})
        risk = legal_data.get("risk_assessment", {})
        
        # Risk summary
        score = risk.get("score", 0)
        level = risk.get("level", "LOW")
        bg_color, text_color = self._create_risk_badge(level)
        
        risk_summary = [[
            Paragraph(f"<b>Legal Risk Score: {score}/100</b>", self.styles['CustomHeading2']),
            Paragraph(f"<b>{level}</b>", ParagraphStyle(name='LegalRisk', fontSize=16, textColor=text_color, fontName='Helvetica-Bold'))
        ]]
        
        risk_table = Table(risk_summary, colWidths=[4*inch, 2*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e0')),
        ]))
        elements.append(risk_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Cases table
        cases = legal_info.get("cases", [])
        if cases:
            case_data = [["Case Type", "Court", "Status", "Amount (Cr)", "Risk"]]
            for case in cases:
                case_data.append([
                    case.get("case_type", "").replace("_", " ").title(),
                    Paragraph(case.get("court", ""), ParagraphStyle(name='Small', fontSize=8)),
                    case.get("status", ""),
                    f"₹{case.get('amount_involved_cr', 0):,.2f}",
                    case.get("risk_level", "LOW")
                ])
            
            case_table = Table(case_data, colWidths=[1.3*inch, 2.2*inch, 1*inch, 1*inch, 0.5*inch])
            case_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            elements.append(case_table)
        else:
            elements.append(Paragraph("No legal cases found in public records.", self.styles['CustomBody']))
        
        return elements
    
    def _create_ip_analysis(self, analysis_results):
        """Create IP analysis section."""
        elements = []
        elements.append(Paragraph("INTELLECTUAL PROPERTY ANALYSIS", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        ip_data = analysis_results.get("patent_analysis", {}).get("data", {})
        ip_info = ip_data.get("ip_data", {})
        strength = ip_data.get("strength_score", {})
        
        # IP Strength Score
        score = strength.get("score", 0)
        strength_level = strength.get("strength", "WEAK")
        
        elements.append(Paragraph(f"<b>IP Strength Score: {score}/100 ({strength_level})</b>", 
                                 self.styles['CustomHeading2']))
        elements.append(Spacer(1, 0.1*inch))
        
        # Breakdown
        breakdown = strength.get("breakdown", {})
        for key, value in breakdown.items():
            elements.append(Paragraph(f"• {key.replace('_', ' ').title()}: {value} points", 
                                     self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Patent summary
        patents = ip_info.get("patents", {})
        elements.append(Paragraph(f"<b>Patents:</b> {patents.get('total_count', 0)} total "
                               f"({patents.get('granted', 0)} granted, {patents.get('pending', 0)} pending)",
                               self.styles['CustomBody']))
        
        trademarks = ip_info.get("trademarks", {})
        elements.append(Paragraph(f"<b>Trademarks:</b> {trademarks.get('total_count', 0)} total "
                               f"({trademarks.get('registered', 0)} registered)",
                               self.styles['CustomBody']))
        
        return elements
    
    def _create_news_sentiment(self, analysis_results):
        """Create news sentiment section."""
        elements = []
        elements.append(Paragraph("NEWS SENTIMENT ANALYSIS", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        news_data = analysis_results.get("news_analysis", {}).get("data", {})
        sentiment = news_data.get("sentiment", {})
        
        # Sentiment breakdown
        pos = sentiment.get("positive_pct", 0)
        neg = sentiment.get("negative_pct", 0)
        neu = sentiment.get("neutral_pct", 0)
        
        sentiment_data = [
            ["Sentiment", "Percentage", "Count"],
            ["Positive", f"{pos:.1f}%", str(sentiment.get("positive_count", 0))],
            ["Negative", f"{neg:.1f}%", str(sentiment.get("negative_count", 0))],
            ["Neutral", f"{neu:.1f}%", str(sentiment.get("neutral_count", 0))],
        ]
        
        sent_table = Table(sentiment_data, colWidths=[2*inch, 2*inch, 2*inch])
        sent_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(sent_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Overall sentiment
        overall = sentiment.get("overall_sentiment", "NEUTRAL")
        color = colors.HexColor('#38a169') if overall == "POSITIVE" else colors.HexColor('#c53030') if overall == "NEGATIVE" else colors.HexColor('#718096')
        elements.append(Paragraph(f"<b>Overall Sentiment: {overall}</b>", 
                                 ParagraphStyle(name='Sentiment', fontSize=14, textColor=color, fontName='Helvetica-Bold')))
        
        return elements
    
    def _create_red_flags(self, analysis_results):
        """Create red flag checklist section."""
        elements = []
        elements.append(Paragraph("RED FLAG CHECKLIST", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Collect all red flags
        all_flags = []
        
        # From financial insights
        fin_data = analysis_results.get("financial_analysis", {}).get("data", {})
        for insight in fin_data.get("ratios", {}).get("insights", []):
            if insight.get("risk_level") in ["HIGH", "MEDIUM"]:
                all_flags.append({
                    "category": "FINANCIAL",
                    "description": insight.get("finding", ""),
                    "risk": insight.get("risk_level", "MEDIUM"),
                    "source": insight.get("source", "")
                })
        
        # From corporate filings
        filings_data = analysis_results.get("corporate_filings", {}).get("data", {})
        for flag in filings_data.get("red_flags", []):
            all_flags.append({
                "category": "CORPORATE",
                "description": flag.get("filing_title", ""),
                "risk": flag.get("risk_level", "MEDIUM"),
                "source": flag.get("source", "")
            })
        
        # From legal
        legal_data = analysis_results.get("legal_analysis", {}).get("data", {})
        for case in legal_data.get("legal_data", {}).get("cases", []):
            if case.get("risk_level") == "HIGH":
                all_flags.append({
                    "category": "LEGAL",
                    "description": case.get("title", ""),
                    "risk": case.get("risk_level", "HIGH"),
                    "source": case.get("source", "")
                })
        
        if all_flags:
            flag_data = [["Category", "Description", "Risk", "Source"]]
            for flag in all_flags:
                flag_data.append([
                    flag["category"],
                    Paragraph(flag["description"], ParagraphStyle(name='Small', fontSize=8)),
                    flag["risk"],
                    flag["source"]
                ])
            
            flag_table = Table(flag_data, colWidths=[1*inch, 3.5*inch, 0.7*inch, 0.8*inch])
            flag_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c53030')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            elements.append(flag_table)
        else:
            elements.append(Paragraph("No significant red flags identified.", self.styles['CustomBody']))
        
        return elements
    
    def _create_valuation(self, analysis_results):
        """Create valuation section."""
        elements = []
        elements.append(Paragraph("VALUATION OVERVIEW", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Disclaimer
        disc_box = [[Paragraph(
            "<b>IMPORTANT:</b> Indicative valuation only. Not investment advice. "
            "These estimates are based on simplified models and publicly available information. "
            "Actual valuation requires comprehensive due diligence by qualified professionals.",
            self.styles['Disclaimer']
        )]]
        disc_table = Table(disc_box, colWidths=[6*inch])
        disc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffaf0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#dd6b20')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(disc_table)
        elements.append(Spacer(1, 0.2*inch))
        
        val_data = analysis_results.get("valuation", {}).get("data", {})
        
        # DCF Valuation
        dcf = val_data.get("dcf_valuation", {})
        elements.append(Paragraph("Discounted Cash Flow (DCF) Estimate", self.styles['CustomHeading2']))
        
        if dcf.get("value_per_share"):
            dcf_data = [
                ["Enterprise Value", f"₹{dcf.get('enterprise_value_cr', 0):,.2f} Cr"],
                ["Equity Value", f"₹{dcf.get('equity_value_cr', 0):,.2f} Cr"],
                ["Value per Share", f"₹{dcf.get('value_per_share', 0):,.2f}"],
            ]
            
            assumptions = dcf.get("assumptions", {})
            dcf_data.append(["Growth Rate (5Y)", f"{assumptions.get('growth_rate_5yr', 0)*100:.1f}%"])
            dcf_data.append(["Terminal Growth", f"{assumptions.get('terminal_growth', 0)*100:.1f}%"])
            dcf_data.append(["Discount Rate", f"{assumptions.get('discount_rate', 0)*100:.1f}%"])
            
            dcf_table = Table(dcf_data, colWidths=[2.5*inch, 3.5*inch])
            dcf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ]))
            elements.append(dcf_table)
        else:
            elements.append(Paragraph("DCF valuation could not be calculated due to insufficient data.", 
                                     self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2*inch))
        
        # Comparable Valuation
        comp = val_data.get("comparable_valuation", {})
        elements.append(Paragraph("Comparable Company Analysis", self.styles['CustomHeading2']))
        
        if comp.get("average_value"):
            comp_data = [
                ["P/E Based Value", f"₹{comp.get('pe_based_value', 0):,.2f}"],
                ["P/B Based Value", f"₹{comp.get('pb_based_value', 0):,.2f}"],
                ["Revenue Multiple Value", f"₹{comp.get('revenue_multiple_value', 0):,.2f}"],
                ["Average Value", f"₹{comp.get('average_value', 0):,.2f}"],
            ]
            
            comp_table = Table(comp_data, colWidths=[2.5*inch, 3.5*inch])
            comp_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#edf2f7')),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#c6f6d5')),
            ]))
            elements.append(comp_table)
        
        return elements
    
    def _create_final_risk_rating(self, analysis_results):
        """Create final risk rating section."""
        elements = []
        elements.append(Paragraph("FINAL RISK RATING", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        risk_data = analysis_results.get("risk_engine", {}).get("data", {})
        overall = risk_data.get("overall_risk", {})
        categories = risk_data.get("category_scores", {})
        
        # Overall score big display
        score = overall.get("score", 0)
        level = overall.get("level", "UNKNOWN")
        bg_color, text_color = self._create_risk_badge(level)
        
        # Risk meter
        risk_display = [[
            Paragraph("<b>OVERALL RISK SCORE</b>", self.styles['CustomHeading2']),
            Paragraph(f"<b>{score}</b>", ParagraphStyle(name='BigScore', fontSize=36, textColor=text_color, fontName='Helvetica-Bold'))
        ], [
            Paragraph("Risk Level", self.styles['CustomBody']),
            Paragraph(f"<b>{level}</b>", ParagraphStyle(name='RiskLevel', fontSize=18, textColor=text_color, fontName='Helvetica-Bold'))
        ]]
        
        risk_table = Table(risk_display, colWidths=[4*inch, 2*inch])
        risk_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_color),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor('#cbd5e0')),
        ]))
        elements.append(risk_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Category breakdown
        elements.append(Paragraph("Risk Breakdown by Category", self.styles['CustomHeading2']))
        
        cat_data = [["Category", "Score", "Level", "Key Concerns"]]
        for cat_name, cat_info in categories.items():
            concerns = "; ".join(cat_info.get("reasons", [])[:2])
            cat_data.append([
                cat_name.replace("_", " ").title(),
                str(cat_info.get("score", 0)),
                cat_info.get("level", "LOW"),
                Paragraph(concerns, ParagraphStyle(name='Small', fontSize=8))
            ])
        
        cat_table = Table(cat_data, colWidths=[1.3*inch, 0.8*inch, 0.8*inch, 2.8*inch])
        cat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        elements.append(cat_table)
        
        return elements
    
    def _create_source_appendix(self, analysis_results):
        """Create source appendix section."""
        elements = []
        elements.append(Paragraph("COMPLETE SOURCE APPENDIX", self.styles['CustomHeading1']))
        elements.append(Spacer(1, 0.2*inch))
        
        sources = []
        
        # Collect all sources with confidence scores
        for module_name, module_data in analysis_results.items():
            data = module_data.get("data", {})
            source = module_data.get("source", "Unknown")
            confidence = module_data.get("confidence", 0)
            date = module_data.get("retrieval_date", "Unknown")
            
            sources.append([
                module_name.replace("_", " ").title(),
                source,
                f"{confidence*100:.0f}%",
                date[:10] if date != "Unknown" else "N/A"
            ])
        
        if sources:
            source_data = [["Module", "Data Source", "Confidence", "Retrieval Date"]]
            source_data.extend(sources)
            
            source_table = Table(source_data, colWidths=[1.8*inch, 2.5*inch, 1*inch, 1.2*inch])
            source_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5282')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
            ]))
            elements.append(source_table)
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Final disclaimer
        elements.append(Paragraph(
            "<b>DATA QUALITY NOTICE:</b> This report uses simulated data for demonstration purposes. "
            "In production, all data is sourced from official NSE/BSE filings, public court records, "
            "IP registries, and verified news sources. Confidence scores indicate data reliability based "
            "on source authority and verification level.",
            self.styles['Disclaimer']
        ))
        
        return elements
