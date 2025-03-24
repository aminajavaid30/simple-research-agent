from agno.agent import Agent, RunResponse
from agno.models.together import Together
from agno.tools.arxiv import ArxivTools
from agno.utils.pprint import pprint_run_response
from dotenv import load_dotenv
import os

load_dotenv()

# Define the research agent
research_agent = Agent(
    name="research-agent",
    model=Together(
        id="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", 
        api_key=os.getenv("TOGETHER_API_KEY")),
    tools=[ArxivTools()],
    description=
    '''
        You are a research agent that will fetch papers from arXiv based on a given topic and maximum number of papers.
        You will generate a comprehensive literature review of these papers.
    ''',
    instructions=[
        "Search for research papers on the given topic from arXiv.",
        "If the number of papers is not specified, fetch 5 by default.",
        "Process papers one at a time to reduce token usage.",
        "For each paper, extract the following metadata: title, abstract, authors, publication date, keywords, and source link.",
        "Limit extracted text to at most 2000 tokens per paper.",
        "Generate a concise summary (max 300 tokens) for each paper.",
        "After all papers are processed, generate a literature review using only stored summaries.",
        "The final response should include the literature review of each research paper in a separate paragraph."
        "Each paper review should start with the number and title of the paper as a subheading."
        "The metadata of each paper should be displayed after the title.",
        "Follow the following format for the metadata of each paper in normal text displaying each metadata item on a new line:",
            "**Authors**: [Authors of the Paper]",
            "**Publication Date**: [Date of Publication]",
            "**Keywords**: [Keywords of the Paper]",
        "Follow the following format for the review of each paper in italic text:",
            "**Review**: *[Literature review of the Paper]*",
        "Do not include a Literature Review heading in the response.",
        "Include a conclusion section providing a combined summary of all papers.",
        "Include a references section with citations and source links at the end of the literature review.",
        "Include numbers for each paper in front of their titles.",
        "Generate the literature review by processing the summaries of the papers in smaller chunks instead of one long response."
    ],
    markdown=True,
    show_tool_calls=True,
    debug_mode=True
)

# research_agent.print_response("Search for 5 most relevant papers on Deep Learning and generate a literature review.", stream=True)

# Run agent and return the response as a variable
# response: RunResponse = research_agent.run("Search for 5 most relevant papers on Deep Learning and generate a literature review.")
# # Print the response in markdown format
# pprint_run_response(response, markdown=True)