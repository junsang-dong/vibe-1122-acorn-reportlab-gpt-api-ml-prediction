#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.platypus.flowables import KeepTogether
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_pdf_report(stats_data, analysis_text, charts, output_path):
    """
    ReportLab을 사용하여 PDF 보고서를 생성합니다.
    """
    try:
        # PDF 문서 생성
        doc = SimpleDocTemplate(
            output_path,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=36,
        )
        
        # 스토리 (콘텐츠) 리스트
        story = []
        
        # 스타일 정의
        styles = getSampleStyleSheet()
        
        # 커스텀 스타일 추가
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        heading1_style = ParagraphStyle(
            'CustomHeading1',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2c5aa0'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )
        
        heading2_style = ParagraphStyle(
            'CustomHeading2',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            leading=16,
            alignment=TA_JUSTIFY,
            fontName='Helvetica'
        )
        
        # 제목 페이지
        story.append(Spacer(1, 1.5*inch))
        story.append(Paragraph("Sales Analysis Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        story.append(Paragraph("매출 분석 보고서", title_style))
        story.append(Spacer(1, 0.5*inch))
        
        # 생성 날짜
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        current_date = datetime.now().strftime('%Y년 %m월 %d일')
        story.append(Paragraph(f"Generated on: {current_date}", date_style))
        story.append(PageBreak())
        
        # 주요 통계 요약 테이블
        story.append(Paragraph("Executive Summary", heading1_style))
        story.append(Spacer(1, 0.2*inch))
        
        summary_data = [
            ['Metric', 'Value'],
            ['Total Sales', f"${stats_data.get('total_sales', 0):,.2f}"],
            ['Total Profit', f"${stats_data.get('total_profit', 0):,.2f}"],
            ['Profit Margin', f"{stats_data.get('profit_margin', 0):.2f}%"],
            ['Total Orders', f"{stats_data.get('total_orders', 0):,}"],
            ['Average Sales', f"${stats_data.get('avg_sales', 0):,.2f}"],
            ['Average Profit', f"${stats_data.get('avg_profit', 0):,.2f}"],
        ]
        
        if 'total_quantity' in stats_data:
            summary_data.append(['Total Quantity', f"{stats_data.get('total_quantity', 0):,}"])
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
        
        # 카테고리별 통계 테이블
        if 'category_sales' in stats_data and stats_data['category_sales']:
            story.append(PageBreak())
            story.append(Paragraph("Category Performance", heading1_style))
            story.append(Spacer(1, 0.2*inch))
            
            category_data = [['Category', 'Total Sales', 'Total Profit', 'Orders', 'Avg Sales']]
            for category, data in stats_data['category_sales'].items():
                category_data.append([
                    category,
                    f"${data['total_sales']:,.2f}",
                    f"${data['total_profit']:,.2f}",
                    f"{data['count']:,}",
                    f"${data['avg_sales']:,.2f}"
                ])
            
            category_table = Table(category_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 1*inch, 1.3*inch])
            category_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
            ]))
            
            story.append(category_table)
            story.append(Spacer(1, 0.3*inch))
        
        # 차트 추가
        if charts and len(charts) > 0:
            story.append(PageBreak())
            story.append(Paragraph("Data Visualizations", heading1_style))
            story.append(Spacer(1, 0.2*inch))
            
            for i, chart_path in enumerate(charts):
                if os.path.exists(chart_path):
                    try:
                        # 차트 제목 추출
                        chart_name = os.path.basename(chart_path).replace('.png', '').replace('_', ' ').title()
                        story.append(Paragraph(chart_name, heading2_style))
                        story.append(Spacer(1, 0.1*inch))
                        
                        # 이미지 추가 (크기 조정)
                        img = Image(chart_path, width=5.5*inch, height=3.3*inch)
                        story.append(img)
                        story.append(Spacer(1, 0.3*inch))
                        
                        # 페이지당 2개 차트
                        if (i + 1) % 2 == 0 and i < len(charts) - 1:
                            story.append(PageBreak())
                    except Exception as e:
                        print(f"Error adding chart {chart_path}: {str(e)}", file=sys.stderr)
        
        # GPT 분석 결과 추가
        if analysis_text:
            story.append(PageBreak())
            story.append(Paragraph("AI-Generated Analysis & Strategy", heading1_style))
            story.append(Spacer(1, 0.2*inch))
            
            # 분석 텍스트를 문단으로 나누기
            paragraphs = analysis_text.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    # 마크다운 헤딩 처리
                    if para.strip().startswith('##'):
                        heading_text = para.strip().replace('##', '').strip()
                        story.append(Paragraph(heading_text, heading2_style))
                    elif para.strip().startswith('#'):
                        heading_text = para.strip().replace('#', '').strip()
                        story.append(Paragraph(heading_text, heading1_style))
                    else:
                        # 줄바꿈을 <br/>로 변환
                        para_text = para.replace('\n', '<br/>')
                        # 불릿 포인트 처리
                        if para_text.strip().startswith('-'):
                            para_text = para_text.replace('- ', '• ')
                        story.append(Paragraph(para_text, body_style))
                    story.append(Spacer(1, 0.15*inch))
        
        # 푸터 정보
        story.append(PageBreak())
        footer_style = ParagraphStyle(
            'FooterStyle',
            parent=styles['Normal'],
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph("Report generated by Sales Report Generator", footer_style))
        story.append(Paragraph("Powered by Python, Pandas, Matplotlib, and GPT API", footer_style))
        
        # PDF 빌드
        doc.build(story)
        
        return {
            'success': True,
            'output_path': output_path
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


if __name__ == '__main__':
    if len(sys.argv) < 5:
        print(json.dumps({
            'error': '필수 인자가 부족합니다. (stats_json, analysis_text, charts_json, output_path)'
        }, ensure_ascii=False))
        sys.exit(1)
    
    stats_json = sys.argv[1]
    analysis_text = sys.argv[2]
    charts_json = sys.argv[3]
    output_path = sys.argv[4]
    
    stats_data = json.loads(stats_json)
    charts = json.loads(charts_json)
    
    result = create_pdf_report(stats_data, analysis_text, charts, output_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))

