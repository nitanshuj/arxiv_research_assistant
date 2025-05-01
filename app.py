import streamlit as st
from agentic_crews.arxiv_crew import assemble_crew
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="arXiv Research Assistant", layout="wide")

def main():
    st.title("📄 arXiv Research Assistant")
    
    # Initialize session state
    if 'research_done' not in st.session_state:
        st.session_state.research_done = False
    if 'report_path' not in st.session_state:
        st.session_state.report_path = None

    with st.form("research_form"):
        target_date = st.date_input("Select research date", datetime.date.today())
        
        if st.form_submit_button("Start Research"):
            with st.spinner("🔍 Analyzing research papers..."):
                try:
                    # Clear previous results
                    st.session_state.research_done = False
                    
                    crew = assemble_crew()
                    result = crew.kickoff(inputs={"date": target_date.strftime("%Y-%m-%d")})
                    
                    # Set report path with timestamp
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

    if st.session_state.research_done and st.session_state.report_path:
        st.divider()
        
        # Display report
        with open(st.session_state.report_path, "r", encoding="utf-8") as f:
            html_content = f.read()
            
            col1, col2 = st.columns([1, 3])
            with col1:
                st.download_button(
                    label="⬇️ Download Report",
                    data=html_content,
                    file_name=os.path.basename(st.session_state.report_path),
                    mime="text/html"
                )
            
            with col2:
                st.components.v1.html(html_content, height=800, scrolling=True)

if __name__ == "__main__":
    main()