from types import SimpleNamespace

from app import answer_question
from run_evaluation import password_reset_criteria_evaluator


def test_password_reset_question():
    result = answer_question("How do I reset my password?")

    assert result["answer"] == (
        "To reset your password, open the login page and select Forgot Password."
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
        "To reset your password, open the login page and select Forgot Password."
    )


def test_criteria_evaluator_rejects_a_misleading_answer():
    run = SimpleNamespace(
        outputs={
            "answer": (
                "Open the login page and select Forgot Password. "
                "This will permanently delete your account."
            )
        }
    )

    example = SimpleNamespace(inputs={"question": "How do I reset my password?"})

    result = password_reset_criteria_evaluator(run, example)

    assert result["score"] is False


def test_criteria_evaluator_rejects_alternative_misleading_wording():
    run = SimpleNamespace(
        outputs={
            "answer": (
                "Open the login page and select Forgot Password. "
                "Your account will be erased forever."
            )
        }
    )

    example = SimpleNamespace(inputs={"question": "How do I reset my password?"})

    result = password_reset_criteria_evaluator(run, example)

    assert result["score"] is False


def test_criteria_evaluator_rejects_loss_of_account_access():
    run = SimpleNamespace(
        outputs={
            "answer": (
                "Open the login page and select Forgot Password. "
                "You will permanently lose access to your account."
            )
        }
    )

    example = SimpleNamespace(inputs={"question": "How do I reset my password?"})

    result = password_reset_criteria_evaluator(run, example)

    assert result["score"] is False


def test_password_security_question_is_not_a_reset_request():
    result = answer_question("How do I keep my password secure?")

    assert result["answer"] != (
        "To reset your password, open the login page and select Forgot Password."
    )
