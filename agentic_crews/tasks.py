import os

from crewai import Task



def create_research_task(agent):
    return Task(
        description=(
            "Analyze ArXiv papers from {date} using this EXACT two-step process:\n"
            "1. FIRST: Use the fetch_arxiv_papers tool to retrieve papers\n"
            "2. SECOND: After receiving papers, DO NOT USE ANY OTHER TOOLS. Instead, provide your Final Answer with your analysis\n\n"
            "In your Final Answer, you must:\n"
            "- Select and rank the top 5 papers\n"
            "- For each paper: include title, authors list, innovation score (1-10), impact score (1-10), and key findings\n"
            "- Format as a list of paper objects with these fields: title, authors, innovation_score, impact_score, key_findings, summary, url\n\n"
            "IMPORTANT: After fetching papers, DO NOT attempt to use any other tools or actions like 'Manual Analysis' - simply provide your Final Answer"
        ),
        expected_output=(
            "A list of 5 paper objects with these properties:\n"
            "{\n"
            "  'title': 'Paper Title',\n"
            "  'authors': ['Author 1', 'Author 2', ...],\n"
            "  'innovation_score': 8,\n"
            "  'impact_score': 7,\n"
            "  'key_findings': 'Description of key contributions',\n"
            "  'summary': 'Full paper summary in at least60-100 words',\n"
            "  'url': 'Paper URL'\n"
            "}"
        ),
        agent=agent,
        async_execution=False,
        output_file=None,  # Explicitly set to None to avoid file output issues
    )

def create_reporting_task(agent, context_task):
    return Task(
        description=(
            "Create an HTML report from the research findings with:\n"
            "1. Proper HTML5 structure\n"
            "2. Embedded CSS styling\n"
            "3. Clickable paper titles linking to ArXiv\n"
            "4. Responsive design\n"
            "5. Save to './static/reports/research_report.html'"
        ),
        expected_output=(
            "Complete HTML file saved to disk with all research results presented professionally"
        ),
        agent=agent,
        context=[context_task],
        output_file=os.path.join("static", "reports", "research_report.html"),
        human_input=True
    )

# Add this function to the existing tasks.py file

def create_text_file_generation_task(agent, context_task):
    """Creates a task for generating text file reports."""
    return Task(
        description=(
            "Create a professional text file report for the top 5 research papers using:\n"
            "1. Arial font, size 12 for body text\n"
            "2. Size 16 for main headings\n"
            "3. Size 14 for subheadings\n"
            "4. Include paper titles, authors, and summaries\n"
            "5. Add technical innovation and impact scores if available\n"
            "6. Save the file as a .txt file in the './static/results/' directory\n"
            "7. Save as 'Report_top_5_papers_summary.txt' and 'Report_top_5_papers_summary.md' in results folder"
        ),
        expected_output=(
            "A well-formatted text file containing Title, Author, and summaries of top 5 papers"
            "with consistent styling and professional layout"
        ),
        agent=agent,
        context=[context_task],
        output_file="static/results/Report_top_5_papers_summary.txt"    
    )

# def create_pdf_generation_task(agent, context_task):
#     """Creates a task for generating PDF reports."""
#     return Task(
#         description=(
#             "Create a professional PDF report for the top 5 research papers using:\n"
#             "1. Calibri font, size 12 for body text\n"
#             "2. Size 16 for main headings\n"
#             "3. Size 14 for subheadings\n"
#             "4. Include paper titles, authors, and summaries\n"
#             "5. Add technical innovation and impact scores\n"
#             "6. Save the file as a .PDF file in the './static/reports/' directory\n"
#             "7. Save as 'top_5_papers_summary.pdf' in reports folder"
#         ),
#         expected_output=(
#             "A well-formatted PDF file containing Title, Author, and summaries of top 5 papers"
#             "with consistent styling and professional layout"
#         ),
#         agent=agent,
#         context=[context_task],
#         output_file="static/reports/Report_top_5_papers_summary.pdf",
#     )