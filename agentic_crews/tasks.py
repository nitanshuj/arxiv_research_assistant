from crewai import Task
import os

def create_research_task(agent):
    return Task(
        description=(
            "Analyze ArXiv papers from {date} using the following process:\n"
            "1. Fetch papers using the provided tool\n"
            "2. Evaluate each paper's methodology and results\n"
            "3. Compare innovation levels and potential impacts\n"
            "4. Rank top 10 papers with detailed justification"
        ),
        expected_output=(
            "Markdown formatted list of top 10 papers with:\n"
            "- Title\n- Authors\n- Technical Innovation Score (1-10)\n"
            "- Impact Potential Score (1-10)\n- Key Findings\n- Paper URL"
        ),
        agent=agent,
        async_execution=False
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