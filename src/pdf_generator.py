"""
PDF Report Generator Module
Generates professional PDF reports for trading advisor analysis
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import io
from typing import Dict, Any, Optional


class PDFReportGenerator:
    """Generate PDF reports for trading advisor analysis"""
    
    def __init__(self):
        """Initialize PDF generator"""
        self.buffer = io.BytesIO()
        self.styles = getSampleStyleSheet()
        self._setup_styles()
    
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
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            fontName='Helvetica'
        ))
        
        # Footer style
        self.styles.add(ParagraphStyle(
            name='Footer',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        ))
    
    def _add_header(self, elements):
        """Add report header"""
        # Title
        title = Paragraph("BÁO CÁO TƯ VẤN GIAO DỊCH", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # Date
        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        date_para = Paragraph(f"Ngày tạo: {date_str}", self.styles['CustomBody'])
        elements.append(date_para)
        elements.append(Spacer(1, 1*cm))
    
    def _add_profile_section(self, elements, profile_data: Dict[str, Any]):
        """Add user profile section"""
        # Section header
        header = Paragraph("1. THÔNG TIN HỒ SƠ NGƯỜI DÙNG", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Profile data table
        profile_table_data = [
            ['Tên:', str(profile_data.get('name', 'N/A'))],
            ['Tuổi:', str(profile_data.get('age', 'N/A'))],
            ['Giới tính:', str(profile_data.get('gender', 'N/A'))],
            ['Học vấn:', str(profile_data.get('education', 'N/A'))],
            ['Thu nhập:', str(profile_data.get('income', 'N/A'))],
            ['Vốn giao dịch:', f"${profile_data.get('capital', 0):,.2f}"],
            ['Kinh nghiệm:', str(profile_data.get('experience', 'N/A'))],
            ['Khả năng chấp nhận rủi ro:', f"{profile_data.get('risk_tolerance', 'N/A')}/10"],
            ['Thời gian giao dịch:', str(profile_data.get('available_time', 'N/A'))],
            ['Mục tiêu:', str(profile_data.get('goals', 'N/A'))]
        ]
        
        profile_table = Table(profile_table_data, colWidths=[5*cm, 11*cm])
        profile_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
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
        header = Paragraph("2. PHÂN LOẠI TRADER", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Classification data
        trader_type = classification.get('trader_type', 'N/A')
        confidence = classification.get('confidence_score', 0) * 100
        trading_style = classification.get('trading_style', 'N/A')
        risk_level = classification.get('risk_level', 'N/A')
        
        classification_table_data = [
            ['Loại Trader:', trader_type],
            ['Độ tin cậy:', f"{confidence:.1f}%"],
            ['Phong cách giao dịch:', trading_style],
            ['Mức độ rủi ro:', risk_level]
        ]
        
        classification_table = Table(classification_table_data, colWidths=[5*cm, 11*cm])
        classification_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f4f8')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
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
        header = Paragraph("3. CHỈ SỐ HIỆU SUẤT", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Metrics data
        metrics_table_data = [
            ['Tổng PnL:', f"${metrics.get('total_pnl', 0):,.2f}"],
            ['Tỷ lệ thắng:', f"{metrics.get('win_rate', 0):.2f}%"],
            ['Tổng giao dịch:', str(metrics.get('total_trades', 0))],
            ['Giao dịch thắng:', str(metrics.get('winning_trades', 0))],
            ['Giao dịch thua:', str(metrics.get('losing_trades', 0))],
            ['Lợi nhuận trung bình:', f"${metrics.get('avg_profit', 0):,.2f}"],
            ['Lỗ trung bình:', f"${metrics.get('avg_loss', 0):,.2f}"],
            ['Max Drawdown:', f"${metrics.get('max_drawdown', 0):,.2f}"],
            ['Risk/Reward Ratio:', f"{metrics.get('risk_reward_ratio', 0):.2f}"],
            ['Profit Factor:', f"{metrics.get('profit_factor', 0):.2f}"]
        ]
        
        metrics_table = Table(metrics_table_data, colWidths=[5*cm, 11*cm])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f8f5')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        
        elements.append(metrics_table)
        elements.append(Spacer(1, 1*cm))
    
    def _add_advisory_section(self, elements, advisory: Dict[str, Any]):
        """Add advisory section"""
        # Section header
        header = Paragraph("4. BÁO CÁO TƯ VẤN", self.styles['CustomHeading'])
        elements.append(header)
        elements.append(Spacer(1, 0.3*cm))
        
        # Trader type
        trader_type = advisory.get('trader_type', 'N/A')
        type_para = Paragraph(f"<b>Loại Trader:</b> {trader_type}", self.styles['CustomBody'])
        elements.append(type_para)
        elements.append(Spacer(1, 0.5*cm))
        
        # Strengths
        strengths_header = Paragraph("4.1. ĐIỂM MẠNH", self.styles['CustomSubHeading'])
        elements.append(strengths_header)
        
        for i, strength in enumerate(advisory.get('strengths', []), 1):
            strength_para = Paragraph(f"• {strength}", self.styles['CustomBody'])
            elements.append(strength_para)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Weaknesses
        weaknesses_header = Paragraph("4.2. ĐIỂM YẾU", self.styles['CustomSubHeading'])
        elements.append(weaknesses_header)
        
        for i, weakness in enumerate(advisory.get('weaknesses', []), 1):
            weakness_para = Paragraph(f"• {weakness}", self.styles['CustomBody'])
            elements.append(weakness_para)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Recommendations
        recommendations_header = Paragraph("4.3. KHUYẾN NGHỊ", self.styles['CustomSubHeading'])
        elements.append(recommendations_header)
        
        for i, rec in enumerate(advisory.get('recommendations', []), 1):
            rec_para = Paragraph(f"{i}. {rec}", self.styles['CustomBody'])
            elements.append(rec_para)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Risk warnings
        warnings_header = Paragraph("4.4. CẢNH BÁO RỦI RO", self.styles['CustomSubHeading'])
        elements.append(warnings_header)
        
        for i, warning in enumerate(advisory.get('risk_warnings', []), 1):
            warning_para = Paragraph(f"⚠ {warning}", self.styles['CustomBody'])
            elements.append(warning_para)
        
        elements.append(Spacer(1, 0.5*cm))
        
        # Summary
        if 'summary' in advisory and advisory['summary']:
            summary_header = Paragraph("4.5. TÓM TẮT", self.styles['CustomSubHeading'])
            elements.append(summary_header)
            summary_para = Paragraph(advisory['summary'], self.styles['CustomBody'])
            elements.append(summary_para)
    
    def _add_footer(self, elements):
        """Add report footer"""
        elements.append(Spacer(1, 2*cm))
        footer_text = (
            "Báo cáo này được tạo tự động bởi Trading Advisor AI.<br/>"
            "Thông tin chỉ mang tính chất tham khảo, không phải lời khuyên đầu tư.<br/>"
            "© 2025 SharkMe AI. All rights reserved."
        )
        footer = Paragraph(footer_text, self.styles['Footer'])
        elements.append(footer)
    
    def generate_report(
        self,
        profile_data: Dict[str, Any],
        classification: Dict[str, Any],
        metrics: Dict[str, Any],
        advisory: Dict[str, Any]
    ) -> bytes:
        """
        Generate complete PDF report
        
        Args:
            profile_data: User profile information
            classification: Trader classification results
            metrics: Performance metrics
            advisory: Advisory report data
        
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
        self._add_advisory_section(elements, advisory)
        self._add_footer(elements)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF data
        pdf_data = self.buffer.getvalue()
        self.buffer.close()
        
        return pdf_data
    
    def generate_filename(self, profile_data: Dict[str, Any]) -> str:
        """
        Generate filename for the PDF report
        
        Args:
            profile_data: User profile data
        
        Returns:
            str: Filename for the PDF
        """
        name = profile_data.get('name', 'trader').replace(' ', '_')
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"Trading_Report_{name}_{date_str}.pdf"
