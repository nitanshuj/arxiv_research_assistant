# ----------------
# This is working
# ----------------

import os
from typing import Type, List
from pydantic import BaseModel, Field 
import arxiv
import datetime
from crewai import Agent, Task, Crew, LLM
from crewai.tools import BaseTool

# Configure LM Studio LLM with explicit provider
lm_studio_llm = LLM(
    model="openai/gemma-3-4b-it-Q4_K_M",  # Modified model name format
    api_base="http://localhost:1234/v1",
    temperature=0.3,
    max_tokens=4096,
    provider="openai",  # Explicit provider specification
    api_key="lm-studio"  # Dummy key required by LiteLLM
)

# ArXiv Custom Tool
class FetchArxivPapersInput(BaseModel):
    target_date: datetime.date = Field(..., description="Target date to fetch papers for.")

class FetchArxivPapersTool(BaseTool):
    name: str = "fetch_arxiv_papers"
    description: str = "Fetches all ArXiv papers from selected categories submitted on the target date."
    args_schema: Type[BaseModel] = FetchArxivPapersInput

    def _run(self, target_date: datetime.date) -> List[dict]:
        AI_CATEGORIES = ["cs.CL"]
        client = arxiv.Client(page_size=100, delay_seconds=3)
        
        start_date = target_date.strftime('%Y%m%d%H%M')
        end_date = (target_date + datetime.timedelta(days=1)).strftime('%Y%m%d%H%M')
        
        papers = []
        for category in AI_CATEGORIES:
            search = arxiv.Search(
                query=f"cat:{category} AND submittedDate:[{start_date} TO {end_date}]",
                sort_by=arxiv.SortCriterion.SubmittedDate
            )
            
            for result in client.results(search):
                papers.append({
                    'title': result.title,
                    'authors': [author.name for author in result.authors],
                    'summary': result.summary,
                    'url': result.entry_id
                })
        
        return papers

# Initialize tool
arxiv_tool = FetchArxivPapersTool()

# Research Agent Configuration
researcher = Agent(
    role="Senior AI Researcher",
    goal="Find and rank top AI research papers from ArXiv",
    backstory=(
        "Expert researcher with decades of experience in evaluating "
        "scientific papers and identifying impactful work."
    ),
    tools=[arxiv_tool],
    llm=lm_studio_llm,  # Using LM Studio LLM here
    verbose=True,
    max_iterations=3
)

# Research Task
research_task = Task(
    description=(
        "Analyze all ArXiv papers from {date} and select "
        "the 10 most significant AI research papers. "
        "Rank them by potential impact."
    ),
    expected_output=(
        "Ranked list of top 10 papers with:\n"
        "- Title\n- Authors\n- Key findings\n- Paper URL"
    ),
    agent=researcher,
    human_input=True
)

# Create and run crew
crew = Crew(
    agents=[researcher],
    tasks=[research_task],
    verbose=True
)

if __name__ == "__main__":
    # Make sure LM Studio server is running first!
    result = crew.kickoff(inputs={"date": "2025-04-25"})
    print("\n\n=== FINAL RESULT ===")
    # print(result)