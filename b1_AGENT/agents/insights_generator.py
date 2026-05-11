from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


def generate_business_insights(summary):

    prompt = f"""
    You are a senior data analyst.

    Analyze these ecommerce metrics
    and generate 3 short business insights.

    Metrics:
    {summary}

    Keep insights concise and business-focused.
    """

    response = llm.invoke(prompt)

    return response.content