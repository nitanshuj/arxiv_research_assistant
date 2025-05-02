import os
from crewai import Crew, LLM
from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Replace with your key

# from .agents import create_pdf_generator
# from .tasks import create_pdf_generation_task
# from .tools.pdfgen_tool import PDFGenerationTool
# from .tools.docx_tool import DocxGenerationTool

from .agents import create_researcher
from .agents import create_frontend_engineer
from .agents import create_text_file_generator

from .tasks import create_research_task
from .tasks import create_reporting_task
from .tasks import create_text_file_generation_task

from .tools.arxiv_tool import FetchArxivPapersTool
from .tools.html_tool import HTMLTemplatingTool
from .tools.text_tool import TextGenerationTool

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

def configure_gemini_llm(model_version="gemini-1.5-flash"):
    return LLM(
        model='gemini/'+model_version,
        provider="google",
        api_key=os.getenv("GOOGLE_API_KEY")
    )



def assemble_crew():
    
    # Initialize LLM
    # ------------------------
    # Initialize local LLM - Google's Gemma3: 4b - using LM Studio
    llm_1_local = configure_llm()    
    # Initialize Gemini LLM
    llm_2_gemini = configure_gemini_llm()

    # Create tools
    # ------------------------
    # pdf_tool = PDFGenerationTool()
    arxiv_tool = FetchArxivPapersTool()
    html_tool = HTMLTemplatingTool()
    text_tool = TextGenerationTool()

    
    # Create agents with tools
    # ------------------------
    
    # pdf_generator = create_pdf_generator(llm=llm_2_gemini, tools=[pdf_tool])
    researcher = create_researcher(llm=llm_1_local, tools=[arxiv_tool]) # Swtich to "llm_1_local" later
    frontend_engineer = create_frontend_engineer(llm=llm_2_gemini, tools=[html_tool])
    text_generator = create_text_file_generator(llm=llm_2_gemini, tools=[text_tool])
    
    # Create tasks
    # ------------------------
   #  pdf_task = create_pdf_generation_task(pdf_generator, research_task)
    research_task = create_research_task(researcher)
    reporting_task = create_reporting_task(frontend_engineer, research_task)
    text_task = create_text_file_generation_task(text_generator, research_task)

    
    return Crew(
        agents=[researcher, frontend_engineer, text_generator],
        tasks=[research_task, reporting_task, text_task],
        verbose=True,
        process="sequential"
    )

    # return Crew(
    #     agents=[researcher, docx_generator],
    #     tasks=[research_task, docx_task],
    #     verbose=True,
    #     process="sequential"
    # )
