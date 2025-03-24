import streamlit as st
import requests
import json

# Set Streamlit page configuration
st.set_page_config(page_title="AI Research Agent", layout="wide")

# Initialize session state variables
if "result_json" not in st.session_state:
    st.session_state.result_json = None  # Stores fetched research paper results

if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""  # Stores user-entered research topic

if "max_papers" not in st.session_state:
    st.session_state.max_papers = 5  # Stores user-defined number of papers to fetch

# Sidebar UI elements
with st.sidebar:
    st.image("../images/research_logo.png", width=150)  # Display research agent logo
    st.subheader("Search and Generate Literature Reviews")
    st.header("🔍 Search Papers")
    
    # User input fields for topic and number of papers
    topic = st.text_input("Enter Research Topic:", key="topic_input", value=st.session_state.research_topic)
    max_papers = st.number_input("Number of Papers to Fetch:", min_value=1, max_value=10, 
                                 value=st.session_state.max_papers, key="papers_input")
    
    # Button columns for fetching papers and refreshing
    col_fetch, col_refresh = st.columns([2, 1])

    with col_fetch:
        if st.button("Fetch Papers & Generate Review"):
            if topic:
                st.session_state.research_topic = topic  # Save topic in session state
                try:
                    with st.spinner("Fetching papers..."):
                        API_URL = "http://127.0.0.1:8000/fetch_papers/"  # Backend API endpoint
                        response = requests.post(API_URL, json={"topic": topic, "max_papers": max_papers})

                    if response.status_code != 200:
                        st.error("Error: Invalid response from server.")
                        st.stop()

                    result_decoded = response.content.decode("utf-8")
                    st.session_state.result_json = json.loads(result_decoded)  # Store API response in session state

                except json.JSONDecodeError:
                    st.error("Error: Received an unreadable response from the server.")
                    st.stop()
                except requests.exceptions.RequestException:
                    st.error("Error: Could not connect to the server.")
                    st.stop()

    with col_refresh:
        if st.button("🔄 Refresh"):
            st.session_state.result_json = None  # Clear previous results
            st.session_state.research_topic = ""  # Reset topic field
            st.session_state.max_papers = 5  # Reset number of papers
            st.rerun()  # Force a page refresh

# Main content layout
col1, col2 = st.columns([1, 11])

# Page title
st.title("AI Research Agent")

# Initial message when no results are available
if st.session_state.result_json is None:
    st.info("Enter a research topic and click 'Fetch Papers & Generate Review' to get started.")

# Display results if available
if st.session_state.result_json:
    research_topic = st.session_state.research_topic
    research_topic = ' '.join(word.capitalize() for word in research_topic.split())  # Capitalize topic words
    
    st.header(f"📖 Literature Review: {research_topic}")

    # If a PDF path is provided in the response, display download option
    if "pdf_path" in st.session_state.result_json:
        pdf_path = st.session_state.result_json["pdf_path"]
        filename = f"{topic.replace(' ', '_')}_literature_review.pdf"

        # Create a row layout for success message + download button
        col_success, col_download = st.columns([7, 1])

        with col_success:
            st.success("Literature Review Generated!")

        with col_download:
            st.download_button(label="📥 Download", 
                               data=open(pdf_path, "rb"), 
                               file_name=filename, 
                               mime="application/pdf")
        
        # Display the generated literature review text
        st.write(st.session_state.result_json.get("response", "No review available."))  
    else:
        st.error("No papers found!")
