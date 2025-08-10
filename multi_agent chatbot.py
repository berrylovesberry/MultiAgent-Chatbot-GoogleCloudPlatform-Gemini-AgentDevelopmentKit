from google.adk.agents import Agent

from vertexai.preview.language_models import TextGenerationModel
from vertexai.preview.generative_models import GenerativeModel, Part
from google.cloud import aiplatform
import exa_py
import os

PROJECT_ID = "your_PROJECT_ID"
LOCATION = "your_LOCATION"  
aiplatform.init(project="PROJECT_ID", location="your_LOCATION")

# --- LLM setup ---
# Option 1: Gemini (multimodal, recommended)
model = GenerativeModel("gemini-2.0-flash") 
# Initialize the Exa client
#exa = exa_py.Exa(os.environ.get("EXA_API_KEY"))
exa = exa_py.Exa('e1b6c48f-4af1-4b17-aa69-513c8d79e08a')

def tax_helper(user_query: str)-> str:
    """
    Retrieve the most relevant content from a specific website based on a user query.

    Args:
        user_query (str): The user's question or query
        website_domain (str): The domain to search within (e.g., "example.com")
        max_results (int): Maximum number of results to return

    Returns:
        List of results with relevant content
    """
    # Search the specific domain with content retrieval in one call
    response = exa.search_and_contents(
        query=user_query,
        include_domains=["irs.gov"],
        num_results=5,
        #text=True,  # Get the full text content
        #text={"max_characters": 2000, "include_html_tags": False}, #control the returned content length
        summary={"query": "Provide a summary of the content of this IRS webpage. If the query asks about detailed information, such as tax rate and calculation formula, make sure to include the corresponding detailed information, links and numbers"},#summary option with query
        type="auto"  # Let Exa choose the best search method
    )

    summary = response.results
    answer = model.generate_content(f"answer user's question {user_query} in a clear and informative way based on the following sources: {summary} and cite links where helpful.")
    #to do: pirnt() try if answer used.
    return answer.text.strip()

def social_security_helper(user_query:str)-> str:
    """
    Retrieve the most relevant content from a specific website based on a user query.

    Args:
        user_query (str): The user's question or query
        website_domain (str): The domain to search within (e.g., "example.com")
        max_results (int): Maximum number of results to return

    Returns:
        List of results with relevant content
    """
    # Search the specific domain with content retrieval in one call
    response = exa.search_and_contents(
        query=user_query,
        include_domains=["ssa.gov"],
        num_results=5,
        #text=True,  # Get the full text content
        #text={"max_characters": 2000, "include_html_tags": False}, #control the returned content length
        summary={"query": "Provide a summary of the content of this SSA, the United States Social Security Administration webpage. If the query asks about detailed information, make sure to include the corresponding detailed informatio, links and numbers"},#summary option with query
        type="auto"  # Let Exa choose the best search method
    )
    summary = response.results
    answer = model.generate_content(f"answer user's question {user_query} in a clear and informative way based on the following sources: {summary} and cite links where helpful.")
    return answer.text.strip()

root_agent = Agent(
    name="FinEd_agent",
    model="gemini-2.0-flash",
    description="Agent to answer user's questions about tax and social security in a clear and informative way cite links where helpful",
    instruction="I can answer your questions about tax and social security in a clear and informative way cite links where helpful.",
    tools=[tax_helper, social_security_helper]
)
"""
1. for questions related to both tools, check if the final returned contend arre from both tools. 
returen summary for each tools without llm, if necessary, check summary's data structure, extract it's str content. can also remove the return type(str) if not needed
#to do: pirnt() try if answer used.
2. try ways to make the answer more informative, such as adding more details, links, numbers, etc.
3, try https://cloud.google.com/dialogflow/cx/docs
"""
