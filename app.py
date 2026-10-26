import os

from dotenv import load_dotenv
from langsmith import traceable, tracing_context

load_dotenv()

os.environ.setdefault("LANGSMITH_TRACING", "true")
os.environ.setdefault(
    "LANGSMITH_PROJECT",
    "langsmith-learning-support",
)
os.environ.setdefault(
    "LANGSMITH_ENDPOINT",
    "https://apac.api.smith.langchain.com",
)


def get_support_category(question: str) -> str:
    """Classify a support question using simple rules."""
    question_lower = question.lower()

    reset_phrases = [
        "password reset",
        "reset my password",
        "reset password",
        "forgot my password",
        "forgot password",
        "change my password",
        "change password",
        "cannot log in",
        "can't log in",
        "cannot login",
        "can't login",
        "cannot sign in",
        "can't sign in",
        "unable to log in",
        "unable to login",
        "unable to sign in",
    ]

    if any(phrase in question_lower for phrase in reset_phrases):
        return "password_support"

    return "general_support"


@traceable(name="support_assistant")
def answer_question(question: str) -> dict:
    """Answer a support question using simple rules."""
    question = question.strip()

    if not question:
        return {"answer": "Please enter a question."}

    category = get_support_category(question)

    if category == "password_support":
        answer = (
            "To reset your password, open the login page and select Forgot Password."
        )
    else:
        answer = (
            "Thank you for contacting support. "
            "Please provide more details about your issue."
        )

    return {"answer": answer}


if __name__ == "__main__":
    question = input("Ask support: ").strip()
    category = get_support_category(question)

    with tracing_context(
        metadata={"support_category": category},
        tags=[category],
    ):
        result = answer_question(question)

    print("Assistant:", result["answer"])
