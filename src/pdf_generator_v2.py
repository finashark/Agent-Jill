"""
PDF Report Generator Module V2
Enhanced with Vietnamese font support and chart embedding
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
import os
from typing import Dict, Any, Optional, List
import plotly.graph_objects as go


class PDFReportGeneratorV2:
    """Generate PDF reports with Vietnamese support and charts"""
    
    def __init__(self):
        """Initialize PDF generator"""
        self.buffer = io.BytesIO()
        self.styles = getSampleStyleSheet()
        self._register_fonts()
        self._setup_styles()
    
    def _register_fonts(self):
        """Register fonts that support Vietnamese"""
        try:
            # Try to use DejaVu fonts (best Unicode support)
            from reportlab.pdfbase.ttfonts import TTFont
            from reportlab.pdfbase import pdfmetrics
            import reportlab
            
            # Get reportlab fonts directory
            rl_dir = os.path.dirname(reportlab.__file__)
            fonts_dir = os.path.join(rl_dir, 'fonts')
            
            # Register DejaVu fonts if available
            dejavu_regular = os.path.join(fonts_dir, 'DejaVuSans.ttf')
            dejavu_bold = os.path.join(fonts_dir, 'DejaVuSans-Bold.ttf')
            dejavu_italic = os.path.join(fonts_dir, 'DejaVuSans-Oblique.ttf')
            
            if os.path.exists(dejavu_regular):
                pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_regular))
                self.font_regular = 'DejaVuSans'
            else:
                self.font_regular = 'Helvetica'
                
            if os.path.exists(dejavu_bold):
                pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', dejavu_bold))
                self.font_bold = 'DejaVuSans-Bold'
            else:
                self.font_bold = 'Helvetica-Bold'
                
            if os.path.exists(dejavu_italic):
                pdfmetrics.registerFont(TTFont('DejaVuSans-Oblique', dejavu_italic))
                self.font_italic = 'DejaVuSans-Oblique'
            else:
                self.font_italic = 'Helvetica-Oblique'
                
        except Exception as e:
            print(f"Font registration warning: {e}")
            # Fallback to Helvetica
            self.font_regular = 'Helvetica'
            self.font_bold = 'Helvetica-Bold'
            self.font_italic = 'Helvetica-Oblique'
    
    def _setup_styles(self):
        """Setup custom styles for the PDF"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName=self.font_bold
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName=self.font_bold
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=8,
            fontName=self.font_bold
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName=self.font_regular
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER,
            fontName=self.font_italic
        ))
    
    def _plotly_to_image(self, fig: go.Figure, width=600, height=400) -> Optional[Image]:
        """Convert plotly figure to reportlab Image"""
        try:
            # Export plotly figure to PNG bytes
            img_bytes = fig.to_image(format="png", width=width, height=height, scale=2)
            
            # Create Image object from bytes
            img_buffer = io.BytesIO(img_bytes)
            img = Image(img_buffer, width=14*cm, height=9*cm)
            return img
        except Exception as e:
            print(f"Chart conversion error: {e}")
            return None
    
    def _add_header(self, elements):
        """Add report header"""
        # Title
        title = Paragraph("TRADING ADVISOR REPORT", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # Date
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        date_para = Paragraph(f"Generated: {date_str}", self.styles['CustomBody'])
        elements.append(date_para)
        elements.append(Spacer(1, 1*cm))
    
    def _add_profile_section(self, elements, profile_data: Dict[str, Any]):
        """Add user profile section"""
        # Section header
        header = Paragraph("1. USER PROFILE", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Profile data table
        profile_table_data = [
            ['Name:', str(profile_data.get('name', 'N/A'))],
            ['Age:', str(profile_data.get('age', 'N/A'))],
            ['Gender:', str(profile_data.get('gender', 'N/A'))],
            ['Education:', str(profile_data.get('education', 'N/A'))],
            ['Income:', str(profile_data.get('income', 'N/A'))],
            ['Trading Capital:', f"${profile_data.get('capital', 0):,.2f}"],
            ['Experience:', str(profile_data.get('experience', 'N/A'))],
            ['Risk Tolerance:', f"{profile_data.get('risk_tolerance', 'N/A')}/10"],
            ['Trading Time:', str(profile_data.get('available_time', 'N/A'))],
        ]
        
        # Add goals if available
        goals = profile_data.get('goals', [])
        if isinstance(goals, list):
            goals_str = ', '.join(goals)
        else:
            goals_str = str(goals)
        profile_table_data.append(['Goals:', goals_str])
        
        profile_table = Table(profile_table_data, colWidths=[5*cm, 11*cm])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), self.font_bold),
            ('FONTNAME', (1, 0), (1, -1), self.font_regular),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(profile_table)
        elements.append(Spacer(1, 1*cm))
    
    def _add_classification_section(self, elements, classification: Dict[str, Any]):
        """Add trader classification section"""
        # Section header
        header = Paragraph("2. TRADER CLASSIFICATION", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Classification data
        trader_type = classification.get('trader_type', 'N/A')
        confidence = classification.get('confidence_score', 0) * 100
        trading_style = classification.get('trading_style', 'N/A')
        risk_level = classification.get('risk_level', 'N/A')
        
        classification_table_data = [
            ['Trader Type:', trader_type],
            ['Confidence Score:', f"{confidence:.1f}%"],
            ['Trading Style:', trading_style],
            ['Risk Level:', risk_level]
        ]
        
        classification_table = Table(classification_table_data, colWidths=[5*cm, 11*cm])
        classification_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), self.font_bold),
            ('FONTNAME', (1, 0), (1, -1), self.font_regular),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(classification_table)
        elements.append(Spacer(1, 1*cm))
    
    def _add_metrics_section(self, elements, metrics: Dict[str, Any]):
        """Add performance metrics section"""
        # Section header
        header = Paragraph("3. PERFORMANCE METRICS", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Metrics data
        metrics_table_data = [
            ['Total PnL:', f"${metrics.get('total_pnl', 0):,.2f}"],
            ['Win Rate:', f"{metrics.get('win_rate', 0):.2f}%"],
            ['Total Trades:', str(metrics.get('total_trades', 0))],
            ['Winning Trades:', str(metrics.get('winning_trades', 0))],
            ['Losing Trades:', str(metrics.get('losing_trades', 0))],
            ['Avg Win:', f"${metrics.get('avg_win', 0):,.2f}"],
            ['Avg Loss:', f"${metrics.get('avg_loss', 0):,.2f}"],
            ['Max Drawdown:', f"{metrics.get('max_drawdown', 0):.2f}%"],
            ['Risk/Reward Ratio:', f"{metrics.get('risk_reward_ratio', 0):.2f}"],
            ['Profit Factor:', f"{metrics.get('profit_factor', 0):.2f}"]
        ]
        
        metrics_table = Table(metrics_table_data, colWidths=[5*cm, 11*cm])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f8f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), self.font_bold),
            ('FONTNAME', (1, 0), (1, -1), self.font_regular),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 1*cm))
    
    def _add_charts_section(self, elements, charts: Optional[List[go.Figure]] = None):
        """Add charts section"""
        if not charts:
            return
        
        # Section header
        header = Paragraph("4. ANALYSIS CHARTS", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Add each chart
        for i, fig in enumerate(charts, 1):
            if fig is None:
                continue
                
            chart_img = self._plotly_to_image(fig)
            if chart_img:
                elements.append(chart_img)
                elements.append(Spacer(1, 0.5*cm))
                
                # Add page break after every 2 charts
                if i % 2 == 0 and i < len(charts):
                    elements.append(PageBreak())
    
    def _add_advisory_section(self, elements, advisory: Dict[str, Any]):
        """Add advisory section"""
        # Section header
        header = Paragraph("5. ADVISORY REPORT", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Strengths
        strengths_header = Paragraph("5.1. STRENGTHS", self.styles['CustomSubHeading'])
        elements.append(strengths_header)
        
        for strength in advisory.get('strengths', []):
            # Remove emoji and use bullet points
            strength_clean = strength.replace('✅', '').strip()
            strength_para = Paragraph(f"• {strength_clean}", self.styles['CustomBody'])
            elements.append(strength_para)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Weaknesses
        weaknesses_header = Paragraph("5.2. WEAKNESSES", self.styles['CustomSubHeading'])
        elements.append(weaknesses_header)
        
        for weakness in advisory.get('weaknesses', []):
            weakness_clean = weakness.replace('⚠️', '').strip()
            weakness_para = Paragraph(f"• {weakness_clean}", self.styles['CustomBody'])
            elements.append(weakness_para)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Recommendations
        recommendations_header = Paragraph("5.3. RECOMMENDATIONS", self.styles['CustomSubHeading'])
        elements.append(recommendations_header)
        
        for i, rec in enumerate(advisory.get('recommendations', []), 1):
            rec_clean = rec.replace('💡', '').replace('📌', '').strip()
            rec_para = Paragraph(f"{i}. {rec_clean}", self.styles['CustomBody'])
            elements.append(rec_para)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Risk warnings
        warnings_header = Paragraph("5.4. RISK WARNINGS", self.styles['CustomSubHeading'])
        elements.append(warnings_header)
        
        for warning in advisory.get('risk_warnings', []):
            warning_clean = warning.replace('🚨', '').replace('⚠️', '').strip()
            warning_para = Paragraph(f"! {warning_clean}", self.styles['CustomBody'])
            elements.append(warning_para)
    
    def _add_footer(self, elements):
        """Add report footer"""
        elements.append(Spacer(1, 2*cm))
        footer_text = (
            "This report is automatically generated by Trading Advisor AI.<br/>"
            "Information is for reference only, not investment advice.<br/>"
            "&copy; 2025 SharkMe AI. All rights reserved."
        )
        footer = Paragraph(footer_text, self.styles['Footer'])
        elements.append(footer)
    
    def generate_report(
        self,
        profile_data: Dict[str, Any],
        classification: Dict[str, Any],
        metrics: Dict[str, Any],
        advisory: Dict[str, Any],
        charts: Optional[List[go.Figure]] = None
    ) -> bytes:
        """
        Generate complete PDF report with charts
        
        Args:
            profile_data: User profile information
            classification: Trader classification results
            metrics: Performance metrics
            advisory: Advisory report data
            charts: List of plotly figures to include (optional)
        
        Returns:
            bytes: PDF file content
        """
        # Create document
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        # Build document elements
        elements = []
        
        # Add sections
        self._add_header(elements)
        self._add_profile_section(elements, profile_data)
        self._add_classification_section(elements, classification)
        self._add_metrics_section(elements, metrics)
        
        # Add charts if provided
        if charts:
            elements.append(PageBreak())
            self._add_charts_section(elements, charts)
        
        # Add advisory section
        elements.append(PageBreak())
        self._add_advisory_section(elements, advisory)
        self._add_footer(elements)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF data
        pdf_data = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf_data
    
    def generate_filename(self, profile_data: Dict[str, Any]) -> str:
        """Generate filename for the PDF report"""
        name = profile_data.get('name', 'trader').replace(' ', '_')
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"Trading_Report_{name}_{date_str}.pdf"
