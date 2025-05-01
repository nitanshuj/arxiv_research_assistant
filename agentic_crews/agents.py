from crewai import Agent
from .tools import FetchArxivPapersTool

def create_researcher(llm):
    return Agent(
        role="Senior AI Research Analyst",
        goal="Analyze and rank AI research papers from ArXiv based on impact potential",
        backstory=(
            "Expert researcher with decades of experience in evaluating scientific papers. "
            "Specializes in identifying groundbreaking work through comprehensive analysis of "
            "methodological rigor, innovation level, and potential real-world impact."
        ),
        tools=[FetchArxivPapersTool()],
        llm=llm,
        verbose=True,
        max_iterations=5,
        memory=True,
        allow_delegation=False
    )

def create_frontend_engineer(llm):
    return Agent(
        role="Senior Frontend Engineer",
        goal="Generate professional HTML reports from research data",
        backstory=(
            "Expert web developer specializing in creating beautiful, "
            "interactive research reports with perfect formatting and "
            "responsive design."
        ),
        llm=llm,
        verbose=True,
        memory=True,
        allow_delegation=False
        
    )