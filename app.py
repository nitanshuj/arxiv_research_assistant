import datetime
import os
import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import streamlit.components.v1 as components

from dotenv import load_dotenv
load_dotenv()

from agentic_crews.arxiv_crew import assemble_crew
from agentic_crews.utils import save_feedback

def initialize_session_state():
    """Initialize session state variables"""
    if 'research_done' not in st.session_state:
        st.session_state.research_done = False
    if 'report_path' not in st.session_state:
        st.session_state.report_path = None
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None
    if 'agent_status' not in st.session_state:
        st.session_state.agent_status = ""
    if 'feedback_submitted' not in st.session_state:
        st.session_state.feedback_submitted = False

def update_agent_status(agent_name, status):
    """Update agent status in the UI"""
    st.session_state.current_agent = agent_name
    st.session_state.agent_status = status
    status_placeholder.markdown(f"""
    <div class="status-card">
        <div class="agent-name">{agent_name}</div>
        <div class="agent-status">{status}</div>
    </div>
    """, unsafe_allow_html=True)

def agent_callback(agent_name, status):
    """Callback function for agents to update their status"""
    update_agent_status(agent_name, status)

def handle_feedback(feedback_text, task_type):
    """Handle user feedback and trigger rework if needed"""
    save_feedback(feedback_text)
    st.session_state.feedback_submitted = True
    
    if task_type == "research":
        # Reassemble crew and rerun research task
        crew = assemble_crew()
        result = crew.kickoff(
            inputs={
                "date": st.session_state.target_date,
                "feedback": feedback_text,
                "rework_task": "research"
            }
        )
    elif task_type == "report":
        # Reassemble crew and rerun reporting task
        crew = assemble_crew()
        result = crew.kickoff(
            inputs={
                "date": st.session_state.target_date,
                "feedback": feedback_text,
                "rework_task": "report"
            }
        )
    
    return result

def main():
    st.set_page_config(page_title="arXiv Research Assistant", layout="wide")
    initialize_session_state()
    
    # Custom CSS for better styling
    st.markdown("""
        <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
            background-color: #f8f9fa;
        }
        .app-header {
            padding: 2rem 1rem;
            background: linear-gradient(135deg, #3a8dde 0%, #2c3e50 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
        }
        .app-title {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        .app-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .input-section {
            background-color: white;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .paper-container {
            padding: 0;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .download-section {
            display: flex;
            justify-content: center;
            gap: 1rem;
            padding: 1.5rem;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }
        .download-card {
            background-color: #f1f3f5;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            transition: transform 0.2s, box-shadow 0.2s;
            width: 200px;
        }
        .download-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .download-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: #3a8dde;
        }
        .download-title {
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        .download-desc {
            font-size: 0.85rem;
            color: #6c757d;
            margin-bottom: 1rem;
        }
        .status-card {
            background-color: white;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        .agent-name {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
        }
        .agent-status {
            color: #6c757d;
        }
        .feedback-section {
            background-color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-top: 1.5rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 20px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .download-buttons {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-top: 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # App Header
    st.markdown("""
        <div class="app-header">
            <div class="app-title">📄 arXiv Research Assistant</div>
            <div class="app-subtitle">Discover and analyze the latest AI research papers</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Create a placeholder for agent status
    global status_placeholder
    status_placeholder = st.empty()
    
    # Input Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    
    with st.form("research_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            target_date = st.date_input(
                "Select research date",
                datetime.date.today()
            )
        
        with col2:
            st.markdown("### Options")
            generate_outputs = st.checkbox("Generate Report Files", value=True)
        
        if st.form_submit_button("🔍 Start Research", use_container_width=True):
            st.session_state.target_date = target_date.strftime("%Y-%m-%d")
            st.session_state.research_done = False
            st.session_state.feedback_submitted = False
            
            try:
                with st.spinner("🔍 Analyzing research papers..."):
                    crew = assemble_crew()
                    result = crew.kickoff(
                        inputs={
                            "date": st.session_state.target_date,
                            "generate_outputs": generate_outputs
                        }
                    )
                    
                    # Update report path
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    report_filename = f"research_report_{timestamp}.html"
                    st.session_state.report_path = os.path.join("static", "reports", report_filename)
                    
                    # Rename the generated file
                    temp_path = os.path.join("static", "reports", "research_report.html")
                    if os.path.exists(temp_path):
                        os.rename(temp_path, st.session_state.report_path)
                        st.session_state.research_done = True
                        st.success("✅ Research completed successfully!")
                    else:
                        st.error("❌ Report generation failed - no output file found")
                        
            except Exception as e:
                st.error(f"❌ Research failed: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # Display results and collect feedback
    if st.session_state.research_done and st.session_state.report_path:
        # Display the report in the main area
        with open(st.session_state.report_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Create a centered download section
        st.markdown("""
        <div style="text-align:center; margin-bottom:20px">
            <h3>Download Reports</h3>
        </div>
        """, unsafe_allow_html=True)

        download_col = st.container()
        with download_col:
            # Create a 3-button row
            btn1, btn2, btn3 = st.columns(3)
            
            # HTML Download
            with btn1:
                st.download_button(
                    label="⬇️ Download HTML Report",
                    data=html_content,
                    file_name=os.path.basename(st.session_state.report_path),
                    mime="text/html",
                    use_container_width=True
                )
            
            # Markdown Download
            with btn2:
                md_path = os.path.join("static", "reports", "Report_top_papers_summary.md")
                if os.path.exists(md_path):
                    with open(md_path, "r", encoding="utf-8") as md_file:
                        st.download_button(
                            label="⬇️ Download Markdown",
                            data=md_file.read(),
                            file_name="Report_top_papers_summary.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                else:
                    st.button("⬇️ Download Markdown (N/A)", disabled=True, use_container_width=True)
            
            # Text file Download
            with btn3:
                txt_path = os.path.join("static", "reports", "Report_top_papers_summary.txt")
                if os.path.exists(txt_path):
                    with open(txt_path, "r", encoding="utf-8") as txt_file:
                        st.download_button(
                            label="⬇️ Download Text",
                            data=txt_file.read(),
                            file_name="Report_top_papers_summary.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                else:
                    st.button("⬇️ Download Text (N/A)", disabled=True, use_container_width=True)
        
        # Show the HTML report
        st.markdown('<div class="paper-container">', unsafe_allow_html=True)
        components.html(html_content, height=800, scrolling=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Feedback section
        if not st.session_state.feedback_submitted:
            st.markdown('<div class="feedback-section">', unsafe_allow_html=True)
            st.markdown("### Provide Feedback")
            feedback_text = st.text_area("Your feedback:", height=120)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📝 Research Feedback", use_container_width=True):
                    if feedback_text:
                        result = handle_feedback(feedback_text, "research")
                        st.success("Research updated based on feedback!")
            
            with col2:
                if st.button("🎨 Report Feedback", use_container_width=True):
                    if feedback_text:
                        result = handle_feedback(feedback_text, "report")
                        st.success("Report updated based on feedback!")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()