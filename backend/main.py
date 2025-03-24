from fastapi import FastAPI
from pydantic import BaseModel
from agno.agent import RunResponse
from research_agent import research_agent
from utils import extract_metadata, save_paper_metadata, generate_pdf
import os

# Initialize FastAPI app
app = FastAPI()

# Define request model for research paper fetching
class ResearchRequest(BaseModel):
    topic: str  # Research topic provided by the user
    max_papers: int = 5  # Default number of papers to fetch

# Define API endpoint to fetch research papers
@app.post("/fetch_papers/")
async def fetch_papers(request: ResearchRequest):
    # Call the research agent to search for relevant papers and generate a literature review
    response: RunResponse = research_agent.run(
        f"Search for {request.max_papers} most relevant papers on {request.topic} and generate a literature review."
    )
    
    if response:
        # Extract metadata from the response (e.g., title, authors, publication year, etc.)
        metadata = extract_metadata(response.content)
        
        # Save extracted metadata to a file for future reference
        metadata_file = save_paper_metadata(request.topic, metadata)
        
        # Generate a PDF containing the literature review
        generate_pdf(request.topic, response.content)
        
        # Define the PDF file path based on the topic name
        pdf_path = os.path.join("../literature_reviews", f"{request.topic.replace(' ', '_')}_literature_review.pdf")
        
        # Return the generated literature review details
        return {
            "message": "Literature review generated!", 
            "pdf_path": pdf_path, 
            "response": response.content
        }
    else:
        # Return an error message if no papers were found
        return {"error": "No papers found"}
