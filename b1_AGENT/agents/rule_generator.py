from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.1-8b-instant"
)

def generate_rules(profile):

    prompt = f"""
    You are a professional Data Quality Engineer.

    Analyze this dataset profile:

    {profile}

    Generate data quality validation rules.

    Include:
    - null checks
    - uniqueness rules
    - datatype validation
    - business rules
    - consistency checks

    Give concise bullet points.
    """

    response = llm.invoke(prompt)

    return response.content