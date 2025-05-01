from crewai import Crew
from .agents import create_researcher, create_frontend_engineer
from .tasks import create_research_task, create_reporting_task
from crewai import LLM
import os

def configure_llm():
    return LLM(
        model="openai/gemma-3-4b-it-Q4_K_M",
        api_base="http://localhost:1234/v1",
        temperature=0.1,
        max_tokens=4096,
        provider="openai",
        api_key=os.getenv("LM_STUDIO_KEY", "lm-studio"),
        top_p=0.9,
        frequency_penalty=0.1
    )

def assemble_crew():
    llm = configure_llm()
    
    researcher = create_researcher(llm)
    frontend_engineer = create_frontend_engineer(llm)
    
    research_task = create_research_task(researcher)
    reporting_task = create_reporting_task(frontend_engineer, research_task)
    
    return Crew(
        agents=[researcher, frontend_engineer],
        tasks=[research_task, reporting_task],
        verbose=True,
        memory=True,
        process="sequential"
    )