from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


def infer_category(product_name):

    prompt = f"""
    Predict the ecommerce category
    for this product:

    Product: {product_name}

    Return ONLY category name.
    """

    response = llm.invoke(prompt)

    return response.content.strip()