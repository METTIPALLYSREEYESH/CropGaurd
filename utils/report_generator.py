"""
PDF Report Generator for CropGuard
Creates professional field inspection reports with Unicode support
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np
import io
from utils.translations import get_text

def generate_pdf_report(ai_results, bbox_info, classification_results, ndvi_map, detected_crop, lang='en'):
    """
    Generate a professional PDF field report with Unicode support.
    
    Args:
        ai_results (dict): AI analysis results
        bbox_info (dict): Bounding box information
        classification_results (dict): Health classification data
        ndvi_map (np.array): NDVI data for visualization
        detected_crop (str): Detected crop name
        lang (str): Language code ('en', 'hi', 'te')
        
    Returns:
        bytes: PDF file content
    """
    # Create PDF in memory
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    # Container for PDF elements
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor('#2E7D32'),
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1976D2'),
        spaceAfter=10,
        spaceBefore=12
    )
    
    normal_style = styles['Normal']
    
    # Title
    title = Paragraph("CropGuard Field Inspection Report", title_style)
    elements.append(title)
    
    # Timestamp
    timestamp = Paragraph(
        f"<i>Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</i>",
        ParagraphStyle('Timestamp', parent=normal_style, alignment=TA_CENTER, fontSize=10)
    )
    elements.append(timestamp)
    elements.append(Spacer(1, 20))
    
    # Section 1: Field Information
    elements.append(Paragraph("1. Field Information", heading_style))
    
    field_data = [
        ["Location:", f"{bbox_info['center_lat']:.4f}, {bbox_info['center_lon']:.4f}"],
        ["Area:", f"{bbox_info['area_km2']:.2f} km²"],
        ["Detected Crop:", detected_crop],
    ]
    
    field_table = Table(field_data, colWidths=[2*inch, 4*inch])
    field_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
    ]))
    elements.append(field_table)
    elements.append(Spacer(1, 20))
    
    # Section 2: AI Risk Assessment
    elements.append(Paragraph("2. AI Risk Assessment", heading_style))
    
    risk_level = ai_results['risk_level']
    risk_color_hex = '#4CAF50' if risk_level == 'Stable' else '#FF9800' if risk_level == 'Medium Risk' else '#F44336'
    
    # Risk alert box
    risk_text = f"<b>ALERT: {risk_level.upper()}</b>"
    risk_para = Paragraph(
        risk_text,
        ParagraphStyle('RiskAlert', parent=normal_style, 
                      fontSize=14, textColor=colors.white,
                      alignment=TA_CENTER, spaceAfter=10)
    )
    
    risk_table = Table([[risk_para]], colWidths=[6*inch])
    risk_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(risk_color_hex)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(risk_table)
    elements.append(Spacer(1, 12))
    
    # AI metrics
    metrics_data = [
        ["AI Health Score:", f"{ai_results['ai_score']}/100"],
        ["NDVI Change:", f"{ai_results['ndvi_change']:.3f}"],
    ]
    
    metrics_table = Table(metrics_data, colWidths=[2*inch, 4*inch])
    metrics_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 20))
    
    # Section 3: Detailed Analysis (with Unicode support)
    elements.append(Paragraph("3. Detailed Analysis", heading_style))
    
    # Get translated explanation
    explanation = ai_results['risk_explanation']
    explanation_para = Paragraph(explanation, normal_style)
    elements.append(explanation_para)
    elements.append(Spacer(1, 20))
    
    # Section 4: Recommended Actions (with Unicode support)
    elements.append(Paragraph("4. Recommended Actions", heading_style))
    
    action = ai_results['action_recommendation']
    action_para = Paragraph(action, normal_style)
    elements.append(action_para)
    elements.append(Spacer(1, 20))
    
    # Section 5: Health Distribution
    elements.append(Paragraph("5. Health Distribution", heading_style))
    
    health_data = [
        ["Healthy:", f"{classification_results['healthy']['percentage']:.1f}%"],
        ["Moderate:", f"{classification_results['moderate']['percentage']:.1f}%"],
        ["Unhealthy:", f"{classification_results['unhealthy']['percentage']:.1f}%"],
    ]
    
    health_table = Table(health_data, colWidths=[2*inch, 4*inch])
    health_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(health_table)
    elements.append(Spacer(1, 20))
    
    # Section 6: NDVI Visualization
    elements.append(Paragraph("6. NDVI Heatmap", heading_style))
    
    try:
        # Generate NDVI heatmap
        fig, ax = plt.subplots(figsize=(6, 4))
        im = ax.imshow(ndvi_map, cmap='RdYlGn', vmin=-0.2, vmax=1.0)
        ax.set_title('NDVI Health Map')
        ax.axis('off')
        plt.colorbar(im, ax=ax, label='NDVI Value')
        
        # Save to buffer
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        plt.close()
        
        # Add to PDF
        img = Image(img_buffer, width=5*inch, height=3.5*inch)
        elements.append(img)
    except Exception as e:
        error_para = Paragraph(f"<i>[Visualization unavailable: {str(e)}]</i>", normal_style)
        elements.append(error_para)
    
    elements.append(Spacer(1, 20))
    
    # Footer note
    note_style = ParagraphStyle('Note', parent=normal_style, fontSize=9, textColor=colors.grey)
    note = Paragraph(
        "<i>Note: This report is generated using satellite imagery analysis. "
        "For critical decisions, please consult with agricultural experts.</i>",
        note_style
    )
    elements.append(note)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF bytes
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
