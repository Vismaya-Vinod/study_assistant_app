# core/flashcards.py

from .ai_utils import get_llm_client

def generate_flashcards(content):

    genai, _ = get_llm_client("Gemini")
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    Create 5 high-quality study flashcards from the content below.

    Format strictly like this:

    Q: question here
    A: answer here

    Content:
    {content}
    """

    response = model.generate_content(prompt)

    return response.text