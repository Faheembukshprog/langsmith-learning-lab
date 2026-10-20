
from app import answer_question


def test_password_reset_question():
    result = answer_question("How do I reset my password?")

    assert result["answer"] == (
        "To reset your password, open the login page "
        "and select Forgot Password."
    )


def test_general_question():
    result = answer_question("Where is my order?")

    assert result["answer"] == (
        "Thank you for contacting support. "
        "Please provide more details about your issue."
    )


def test_empty_question():
    result = answer_question("   ")

    assert result["answer"] == "Please enter a question."


def test_password_reset_is_case_insensitive():
    result = answer_question("PASSWORD RESET")

    assert result["answer"] == (
        "To reset your password, open the login page "
        "and select Forgot Password."
    )
