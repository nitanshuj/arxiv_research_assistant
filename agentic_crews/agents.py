from crewai import Agent

def create_researcher(llm, tools=None):
    return Agent(
        role="Senior AI Research Analyst",
        goal="Analyze and rank AI research papers from ArXiv based on impact potential",
        backstory=(
            "Expert researcher with decades of experience in evaluating scientific papers. "
            "Specializes in identifying groundbreaking work through comprehensive analysis of "
            "methodological rigor, innovation level, and potential real-world impact."
            "You have a keen eye for detail and a deep understanding of AI advancements."
            "You are passionate about advancing the field of AI through rigorous evaluation and synthesis of research findings."
        ),
        tools=tools,
        llm=llm,
        verbose=True,
        memory=True,
        max_iterations=5,
        allow_delegation=False
    )

def create_frontend_engineer(llm, tools=None):
    return Agent(
        role="Senior Frontend Engineer",
        goal="Generate professional HTML reports from research data",
        backstory=(
            "Expert web developer specializing in creating beautiful, "
            "interactive research reports with perfect formatting and "
            "responsive design."
            "You have extensive experience in HTML5, CSS3"
            "You love crafting user-friendly interfaces that effectively present complex data."
        ),
        tools=tools,
        llm=llm,        
        verbose=True,
        memory=True,
        allow_delegation=False
        
    )

def create_text_file_generator(llm, tools=None):
    """Creates an agent specialized in generating txt and markdown reports."""
    return Agent(
        role="Text file and markdown file Specialist",
        goal="Generate professional text files and markdown files summarizing research papers",
        backstory=(
            "Expert document specialist with extensive experience in creating "
            "clear, well-formatted text files and markdown files that effectively communicate "
            "complex research findings. "
            "You have a strong background in typography and layout design, "
            "ensuring all documents are readable and professional."
        ),
        tools=tools,
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

# def create_pdf_generator(llm, tools=None):
#     """Creates an agent specialized in generating PDF reports."""
#     return Agent(
#         role="PDF Report Specialist",
#         goal="Generate professional .PDF reports summarizing research papers",
#         backstory=(
#             "Expert document specialist with extensive experience in creating "
#             "clear, well-formatted PDF reports (.pdf)that effectively communicate "
#             "complex research findings."
#             "You have a strong background in typography and layout design, "
#             "You are skilled in using advanced PDF generation libraries "
#             "to produce visually appealing and accessible documents."
#         ),
#         tools=tools,
#         llm=llm,
#         verbose=True,
#         memory=True,
#         allow_delegation=False
#     )

# Add this function to the existing agents.py file