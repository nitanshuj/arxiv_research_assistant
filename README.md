# ArXiv Research Assistant

## Overview
The **ArXiv Research Assistant** is a multi-agent system designed to automate the process of discovering, analyzing, and ranking AI research papers from ArXiv. It leverages advanced AI tools and models to provide a ranked list of the most impactful research papers, along with an interactive HTML report for easy exploration.

## Features
- **Automated Paper Retrieval**: Fetches AI research papers from ArXiv for a specified date.
- **Ranking and Analysis**: Analyzes and ranks the top 10 papers based on technical innovation and impact potential.
- **Interactive Reports**: Generates a clean, responsive HTML report with clickable links to the papers.
- **Feedback Integration**: Collects user feedback to improve the system's performance and outputs.
- **Local LLM Hosting**: Local secure hosting of LLM (Gemma3:4b) using `LM Studio`.

## How It Works
1. **Paper Retrieval**: The system uses the `FetchArxivPapersTool` to fetch papers from ArXiv based on the selected date and categories.
2. **Analysis and Ranking**: A `Senior AI Researcher` agent evaluates the papers using a custom LLM (Language Model) and ranks them based on their significance.
3. **Report Generation**: A `Frontend Engineer` agent compiles the results into an interactive HTML report.
4. **Feedback Collection**: Users can provide feedback on the results, which is saved for future improvements.

## Project Structure
```
arxiv_research_assistant/
├── agentic_crews/
│   ├── __init__.py
│   ├── agents.py          # Defines the agents (e.g., researcher, frontend engineer)
│   ├── arxiv_crew.py      # Assembles the multi-agent system (crew)
│   ├── tasks.py           # Defines tasks for the agents
│   ├── tools.py           # Custom tools for fetching ArXiv papers
│   ├── utils.py           # Utility functions (e.g., environment loading, feedback saving)
│   ├── working_code.py    # Fully functional code for reference
├── static/
│   ├── feedback/          # Stores user feedback
│   ├── results/           # Stores research results and reports
├── .env                   # Environment variables (API keys, etc.)
├── .gitignore             # Git ignore file
├── app.py                 # Streamlit application for user interaction
├── requirements.txt       # Python dependencies
├── Readme.md              # Project documentation
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/arxiv-research-assistant.git
   cd arxiv-research-assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install LM Studio:
   - Download and install LM Studio from the [official website](https://lmstudio.ai/).
   - After installation, download the required model (e.g., `gemma3:4b`) within LM Studio.

4. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your API keys (e.g., OpenAI, Serper, LM Studio) as shown in the example `.env` file:
     ```
     OPENAI_API="your-openai-api-key"
     SERPER_API_KEY="your-serper-api-key"
     LM_STUDIO_KEY="your-lm-studio-key"
     ```

5. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the Streamlit app in your browser.
2. Select a target date for research.
3. Click "Start Research" to begin the process.
4. View the ranked list of papers and the interactive HTML report.
5. Provide feedback to improve the system.

## Key Components
### Agents
- **Researcher**: Analyzes and ranks papers using the `FetchArxivPapersTool` and a custom LLM.
- **Frontend Engineer**: Generates an interactive HTML report from the research findings.

### Tools
- **FetchArxivPapersTool**: Fetches papers from ArXiv based on the selected date and categories.

### Tasks
- **Research Task**: Analyzes and ranks papers.
- **Reporting Task**: Generates an HTML report.

## Dependencies
- Python 3.8+
- Libraries: `numpy`, `pandas`, `crewai`, `arxiv`, `streamlit`, `pydantic`, `transformers`, etc. (see `requirements.txt` for the full list).

## Feedback
User feedback is stored in the `static/feedback/` directory and can be used to refine the system's performance.

## Future Enhancements
- Add support for more AI categories.
- Improve the ranking algorithm with additional metrics.
- Enable real-time updates for ArXiv submissions.

## License
This project is licensed under the MIT License.

## Acknowledgments
This mini-project is inspired by the article: [Building Your First AI Agent](https://levelup.gitconnected.com/building-your-first-ai-agent-that-will-actually-improve-you-as-an-ai-engineer-4cb99e590d30).