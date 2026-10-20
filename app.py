
import os

from dotenv import load_dotenv
from langsmith import traceable

# Load local .env settings if a .env file exists.
# Existing environment variables are preserved.
load_dotenv()

# Set safe defaults for this learning project.
os.environ.setdefault("LANGSMITH_TRACING", "true")
os.environ.setdefault(
    "LANGSMITH_PROJECT",
    "langsmith-learning-support",
)
os.environ.setdefault(
    "LANGSMITH_ENDPOINT",
    "https://apac.api.smith.langchain.com",
)



@traceable(name="support_assistant")
def answer_question(question: str) -> dict:
    """Answer a support question using simple rules."""

    question = question.strip()

    if not question:
        return {"answer": "Please enter a question."}

    question_lower = question.lower()

    if any(
        keyword in question_lower
        for keyword in ["password", "log in", "login", "sign in"]
    ):
        answer = (
            "To reset your password, open the login page "
            "and select Forgot Password."
        )
    else:
        answer = (
            "Thank you for contacting support. "
            "Please provide more details about your issue."
        )

    return {"answer": answer}



if __name__ == "__main__":
    question = input("Ask support: ")
    result = answer_question(question)
    print("Assistant:", result["answer"])
