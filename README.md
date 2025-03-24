# Simple Research Agent

## Overview
The **Simple Research Agent** is an AI-powered tool that automates research paper discovery and summarization. It fetches research papers from **arXiv** based on a given topic, extracts key metadata, and generates a structured literature review.

(images/simple-research-agent.png)

## Features
- 📰 **Fetch Research Papers**: Retrieves papers from **arXiv** based on a specified topic.
- 🏷 **Metadata Extraction**: Extracts title, authors, publication date, keywords, and source link.
- ✍ **Summarization**: Generates concise summaries for each paper (max 300 tokens).
- 📄 **Literature Review Generation**: Compiles a structured review, including conclusions and references.
- 📑 **PDF Generation**: Saves the literature review as a PDF.

## Tech Stack
- **Python** (Main Language)
- **Streamlit** (Frontend)
- **FastAPI** (Backend) 
- **Agno** (AI Agent Framework)
- **Together API** (LLM Backend)
- **ArXivTools** (Paper Fetching)
- **dotenv** (Environment Variable Management)

## Installation
1. **Clone the Repository**:
   ```sh
   git clone https://github.com/aminajavaid30/simple-research-agent.git
   cd simple-research-agent
   ```

2. **Set Up a Virtual Environment (Optional but Recommended)**:
   ```sh
   conda create -n agents
   conda activate agents
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file and add your API key:
   ```
   TOGETHER_API_KEY=your_together_api_key_here
   ```

## Usage
### Running the Research Agent
- Navigate to the `backend` folder and start the FastAPI server:  
```sh
cd backend
uvicorn main:app --reload
```

- Navigate to the frontend folder and start the Streamlit application:
```sh
cd frontend
streamlit run app.py
```

- Access the application through the following link.
```sh
http://localhost:8501
```

### Generating a Literature Review
After fetching papers, the agent generates a structured literature review. The output is saved as a **PDF** in the `literature_reviews` folder.

## Project Structure
```
📂 simple-research-agent
├── 📄 README.md            # Project Documentation
├── 📄 requirements.txt     # Dependencies
├── 📝  LICENCE             # Project License
├── 🔐 .env                 # Environment variables
├── 📂 backend              # Backend files
│   ├── main.py             # FastAPI Endpoints
│   ├── research_agent.py   # Agno Agent
│   ├── utils.py            # Utility Functions
│   ├── pdf.py              # PDF Generation Module
├── 📂 frontend             # Frontend files
│   ├── app.py              # Application Entrypoint
└── 📂 literature_reviews   # Generated PDFs
```

## Future Enhancements
- ✅ **Support for Multiple Research Sources** (e.g., Semantic Scholar, IEEE Xplore)
- ✅ **Enhanced Citation Formatting** (BibTeX, APA, MLA)
- ✅ **Database Storage for Research Papers**

## License
This project is open-source and available under the **MIT License**.

## Contributors
- **Amina Javaid** ([@https://github.com/aminajavaid30](https://github.com/aminajavaid30/simple-research-agent))

🚀 Happy Researching!
