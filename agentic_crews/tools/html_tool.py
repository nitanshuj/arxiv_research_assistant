import datetime
import arxiv
from typing import List, Type, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool  # Changed import to use crewai.tools

# First, add a new schema class for the HTML templating tool
class HTMLTemplatingInput(BaseModel):
    papers: List[dict] = Field(
        ...,
        description="List of paper dictionaries containing title, authors, summary, url, and scores"
    )

class HTMLTemplatingTool(BaseTool):
    name: str = "html_templating"
    description: str = "Generates beautiful HTML reports with modern styling"
    args_schema: Type[BaseModel] = HTMLTemplatingInput
    
    def _generate_paper_html(self, paper, index):
        """Generate HTML for a single paper"""
        # Get the full summary without truncation
        full_summary = paper.get('summary', 'No summary available.')
        
        return f"""
            <div class="paper-card">
                <div class="paper-number">{index}</div>
                <h2 class="paper-title">{paper['title']}</h2>
                <div class="paper-meta">
                    <div class="authors">
                        <strong>Authors:</strong><br>
                        {', '.join(paper['authors'])}
                    </div>
                    <div class="scores">
                        <span class="score">Innovation: {paper.get('innovation_score', 'N/A')}/10</span>
                        <span class="score">Impact: {paper.get('impact_score', 'N/A')}/10</span>
                    </div>
                </div>
                <div class="paper-summary">
                    <strong>Full Summary:</strong><br>
                    {full_summary}
                </div>
                <div class="paper-findings">
                    <strong>Key Findings:</strong><br>
                    {paper.get('key_findings', 'N/A')}
                </div>
                <a href="{paper['url']}" class="paper-link" target="_blank">Read on arXiv →</a>
            </div>
        """

    def _run(self, papers: List[dict]) -> str:
        paper_html = ''.join(self._generate_paper_html(paper, i+1) for i, paper in enumerate(papers))
        
        template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Research Papers Analysis</title>
            <style>
                :root {{
                    --primary-color: #2c3e50;
                    --secondary-color: #3498db;
                    --bg-color: #f9fafb;
                    --text-color: #333;
                    --border-color: #e1e4e8;
                }}
                
                * {{
                    box-sizing: border-box;
                    margin: 0;
                    padding: 0;
                }}
                
                body {{
                    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                    line-height: 1.6;
                    color: var(--text-color);
                    background: var(--bg-color);
                }}
                
                .wrapper {{
                    display: flex;
                    justify-content: center;
                    width: 100%;
                    padding: 2rem;
                }}
                
                .container {{
                    width: 100%;
                    max-width: 900px;
                    background: white;
                    border-radius: 12px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    padding: 2rem;
                }}
                
                h1 {{
                    color: var(--primary-color);
                    text-align: center;
                    margin-bottom: 2rem;
                    font-size: 2rem;
                    padding-bottom: 1rem;
                    border-bottom: 2px solid var(--secondary-color);
                }}
                
                .paper-card {{
                    position: relative;
                    background: white;
                    border: 1px solid var(--border-color);
                    border-radius: 8px;
                    padding: 2rem;
                    margin-bottom: 2rem;
                    transition: transform 0.2s, box-shadow 0.2s;
                }}
                
                .paper-card:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
                }}
                
                .paper-number {{
                    position: absolute;
                    top: -12px;
                    left: -12px;
                    width: 32px;
                    height: 32px;
                    background: var(--secondary-color);
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-weight: bold;
                    font-size: 0.9rem;
                }}
                
                .paper-title {{
                    color: var(--primary-color);
                    margin: 0 0 1rem;
                    font-size: 1.4rem;
                    line-height: 1.4;
                }}
                
                .paper-meta {{
                    display: grid;
                    grid-template-columns: 2fr 1fr;
                    gap: 1.5rem;
                    margin: 1rem 0;
                    padding: 1rem;
                    background: var(--bg-color);
                    border-radius: 8px;
                }}
                
                .authors {{
                    font-size: 0.95rem;
                }}
                
                .scores {{
                    display: flex;
                    flex-direction: column;
                    gap: 0.5rem;
                }}
                
                .score {{
                    display: inline-block;
                    padding: 0.4rem 0.8rem;
                    border-radius: 20px;
                    background: white;
                    font-size: 0.9rem;
                    font-weight: 500;
                    color: var(--primary-color);
                    border: 1px solid var(--border-color);
                }}
                
                .paper-summary {{
                    margin: 1rem 0;
                    line-height: 1.8;
                    color: #4a5568;
                    background-color: #f8f9fa;
                    padding: 1rem;
                    border-radius: 8px;
                    border-left: 4px solid var(--secondary-color);
                }}
                
                .paper-findings {{
                    margin: 1rem 0;
                    line-height: 1.8;
                    color: #4a5568;
                }}
                
                .paper-link {{
                    display: inline-flex;
                    align-items: center;
                    color: var(--secondary-color);
                    text-decoration: none;
                    font-weight: 500;
                    margin-top: 1rem;
                    transition: color 0.2s;
                }}
                
                .paper-link:hover {{
                    color: var(--primary-color);
                    text-decoration: underline;
                }}
                
                @media (max-width: 768px) {{
                    .wrapper {{
                        padding: 1rem;
                    }}
                    
                    .container {{
                        padding: 1rem;
                    }}
                    
                    .paper-meta {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .paper-title {{
                        font-size: 1.2rem;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="wrapper">
                <div class="container">
                    <h1>Latest AI Research Papers Analysis</h1>
                    {paper_html}
                </div>
            </div>
        </body>
        </html>
        """
        return template