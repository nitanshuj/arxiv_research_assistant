import os
from typing import Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import io
import textwrap
import PyPDF2
# PDF Generation Libraries
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class PDFGenerationInput(BaseModel):
    papers: List[dict] = Field(
        ..., 
        description="List of paper dictionaries containing title, authors, summary, scores and URL"
    )

class PDFGenerationTool(BaseTool):
    name: str = "pdf_generation"
    description: str = "Generates professional PDF reports from research data"
    args_schema: Type[BaseModel] = PDFGenerationInput

    def _run(self, papers: List[dict]) -> str:
        # Set up the output path
        output_dir = "static/reports"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "Report_top_5_papers_summary.pdf")
        
        try:
            # Register Calibri font (ensure the .ttf file is available)
            try:
                pdfmetrics.registerFont(TTFont('Calibri', 'Calibri.ttf'))
                font_name = 'Calibri'
            except:
                print("Calibri font not found. Falling back to Helvetica.")
                font_name = 'Helvetica'

            # Safely sanitize text to avoid encoding/HTML issues
            def sanitize(text):
                if not isinstance(text, str):
                    text = str(text)
                # Replace problematic Unicode characters
                replacements = {
                    '\u2013': '-',    # en dash
                    '\u2014': '--',   # em dash
                    '\u2018': "'",    # left single quote
                    '\u2019': "'",    # right single quote
                    '\u201c': '"',    # left double quote
                    '\u201d': '"',    # right double quote
                    '\u2022': '*',    # bullet
                    '\u2026': '...',  # ellipsis
                }
                for char, replacement in replacements.items():
                    text = text.replace(char, replacement)
                # Escape HTML-sensitive characters
                text = text.replace('&', '&amp;')
                text = text.replace('<', '&lt;')
                text = text.replace('>', '&gt;')
                return text
            
            # Create a PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Define styles (using Calibri or fallback font)
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'Title',
                parent=styles['Heading1'],
                fontName=font_name,
                fontSize=16,
                alignment=1,  # Center
                spaceAfter=24
            )
            
            heading_style = ParagraphStyle(
                'Heading',
                parent=styles['Heading2'],
                fontName=font_name,
                fontSize=14,
                spaceAfter=12
            )
            
            subtitle_style = ParagraphStyle(
                'Subtitle',
                parent=styles['Heading3'],
                fontName=font_name,
                fontSize=12,
                spaceAfter=6
            )
            
            normal_style = ParagraphStyle(
                'Normal',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=10,
                spaceAfter=10
            )
            
            # Build the PDF content
            story = []
            story.append(Paragraph(sanitize("Top AI Research Papers Analysis"), title_style))
            story.append(Spacer(1, 12))
            
            # Add each paper
            for i, paper in enumerate(papers[:5], 1):
                title = sanitize(paper.get('title', 'Untitled'))
                authors = paper.get('authors', ['Unknown'])
                authors_text = sanitize(', '.join(authors) if isinstance(authors, list) else sanitize(authors))
                summary = sanitize(paper.get('summary', 'No summary available.'))
                url = sanitize(paper.get('url', 'No URL available.'))
                
                # Add paper content
                story.append(Paragraph(f"{i}. {title}", heading_style))
                story.append(Paragraph(f"<b>Authors:</b> {authors_text}", normal_style))
                story.append(Paragraph("<b>Summary:</b>", subtitle_style))
                
                # Split summary into paragraphs
                for paragraph in summary.split('\n'):
                    if paragraph.strip():
                        story.append(Paragraph(paragraph, normal_style))
                
                story.append(Paragraph(f"<b>URL:</b> {url}", normal_style))
                story.append(Spacer(1, 20))
                
                # Page break (except for last paper)
                if i < min(len(papers), 5):
                    story.append(PageBreak())
            
            # Generate PDF
            doc.build(story)
            
            # Verify the PDF
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                return f"PDF generated successfully at: {output_path}"
            else:
                raise Exception("PDF was created but is empty/corrupted.")
            
        except Exception as e:
            # Fallback: Create a minimal error PDF
            try:
                from reportlab.pdfgen import canvas
                c = canvas.Canvas(output_path, pagesize=letter)
                c.setFont("Helvetica", 12)
                c.drawString(72, 72, "Error generating full PDF report.")
                c.drawString(72, 56, f"Reason: {str(e)}")
                c.save()
                return f"Fallback PDF created at {output_path} due to error: {str(e)}"
            except:
                return f"Failed to generate any PDF. Original error: {str(e)}"