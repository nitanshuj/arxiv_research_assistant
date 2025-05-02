import os
from typing import Type, List
from pydantic import BaseModel, Field
from crewai.tools import BaseTool

class TextGenerationInput(BaseModel):
    papers: List[dict] = Field(
        ..., 
        description="List of paper dictionaries containing title, authors, summary, scores and URL"
    )

class TextGenerationTool(BaseTool):
    name: str = "text_generation"   
    description: str = "Generates well-formatted text and markdown documents from research data"
    args_schema: Type[BaseModel] = TextGenerationInput

    def _run(self, papers: List[dict]) -> str:
        # Set up the output paths
        output_dir = "static/reports"
        os.makedirs(output_dir, exist_ok=True)

        txt_path = os.path.join(output_dir, "Report_top_papers_summary.txt")
        md_path = os.path.join(output_dir, "Report_top_papers_summary.md")
        
        # Generate the text file
        try:
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                # Add title with decorative elements
                txt_file.write("=" * 80 + "\n")
                txt_file.write("LATEST AI RESEARCH PAPERS ANALYSIS\n")
                txt_file.write("=" * 80 + "\n\n")
                
                # Process each paper (up to 5)
                for i, paper in enumerate(papers[:5], 1):
                    # Extract paper details with proper error handling
                    title = paper.get('title', 'Untitled')
                    
                    # Handle authors
                    authors = paper.get('authors', ['Unknown'])
                    if isinstance(authors, list):
                        authors_text = ', '.join(str(a) for a in authors if a)
                    else:
                        authors_text = str(authors)
                    
                    # Get other paper info
                    summary = paper.get('summary', 'No summary available.')
                    url = paper.get('url', 'No URL available.')
                    innovation_score = paper.get('innovation_score', 'N/A')
                    impact_score = paper.get('impact_score', 'N/A')
                    key_findings = paper.get('key_findings', 'No key findings available.')
                    
                    # Format paper number and title
                    txt_file.write(f"PAPER #{i}: {title}\n")
                    txt_file.write("-" * 80 + "\n\n")
                    
                    # Add authors
                    txt_file.write(f"AUTHORS:\n{authors_text}\n\n")
                    
                    # Add scores
                    txt_file.write(f"INNOVATION SCORE: {innovation_score}/10\n")
                    txt_file.write(f"IMPACT SCORE: {impact_score}/10\n\n")
                    
                    # Add summary with header
                    txt_file.write("SUMMARY:\n")
                    txt_file.write("-" * 10 + "\n")
                    txt_file.write(f"{summary}\n\n")
                    
                    # Add key findings
                    txt_file.write("KEY FINDINGS:\n")
                    txt_file.write("-" * 13 + "\n")
                    txt_file.write(f"{key_findings}\n\n")
                    
                    # Add URL
                    txt_file.write(f"URL: {url}\n\n")
                    
                    # Add separator between papers
                    txt_file.write("=" * 80 + "\n\n")
            
            # Generate the markdown file
            with open(md_path, 'w', encoding='utf-8') as md_file:
                # Add title and header
                md_file.write("# Latest AI Research Papers Analysis\n\n")
                md_file.write("*An automated analysis of top papers from arXiv*\n\n")
                md_file.write("---\n\n")
                
                # Create table of contents
                md_file.write("## Table of Contents\n\n")
                for i, paper in enumerate(papers[:5], 1):
                    title = paper.get('title', 'Untitled')
                    md_file.write(f"{i}. [{title}](#paper-{i})\n")
                md_file.write("\n---\n\n")
                
                # Process each paper
                for i, paper in enumerate(papers[:5], 1):
                    # Extract paper details
                    title = paper.get('title', 'Untitled')
                    
                    # Handle authors
                    authors = paper.get('authors', ['Unknown'])
                    if isinstance(authors, list):
                        authors_text = ', '.join(str(a) for a in authors if a)
                    else:
                        authors_text = str(authors)
                    
                    # Get other paper info
                    summary = paper.get('summary', 'No summary available.')
                    url = paper.get('url', 'No URL available.')
                    innovation_score = paper.get('innovation_score', 'N/A')
                    impact_score = paper.get('impact_score', 'N/A')
                    key_findings = paper.get('key_findings', 'No key findings available.')
                    
                    # Add paper section with anchor for table of contents
                    md_file.write(f"<a id='paper-{i}'></a>\n")
                    md_file.write(f"## {i}. {title}\n\n")
                    
                    # Add paper metadata
                    md_file.write(f"**Authors:** {authors_text}\n\n")
                    md_file.write(f"**Innovation Score:** {innovation_score}/10  \n")
                    md_file.write(f"**Impact Score:** {impact_score}/10\n\n")
                    
                    # Add summary section
                    md_file.write("### Summary\n\n")
                    md_file.write(f"{summary}\n\n")
                    
                    # Add key findings section
                    md_file.write("### Key Findings\n\n")
                    md_file.write(f"{key_findings}\n\n")
                    
                    # Add URL as a link
                    md_file.write(f"**Read More:** [{url}]({url})\n\n")
                    
                    # Add separator between papers
                    md_file.write("---\n\n")
                
                # Add footer
                md_file.write("*This report was automatically generated by the AI Research Assistant.*\n")
            
            # Return success message
            return f"Documents generated successfully:\n- Text file: {txt_path}\n- Markdown file: {md_path}"
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"Error generating documents: {e}")
            print(f"Error details: {error_details}")
            return f"Failed to generate documents: {str(e)}"