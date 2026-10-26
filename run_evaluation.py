from langsmith import Client, tracing_context
from langsmith.evaluation import evaluate

from app import answer_question, get_support_category

DATASET_NAME = "support-assistant-evaluation-v1"


def target(inputs: dict) -> dict:
    """Run the support assistant with consistent categorized tracing."""
    question = inputs["question"]
    category = get_support_category(question)

    with tracing_context(
        metadata={"support_category": category},
        tags=[category],
    ):
        return answer_question(question)


def misleading_target(inputs: dict) -> dict:
    """Return a deliberately misleading answer for evaluator testing."""
    return {
        "answer": (
            "Open the login page and select Forgot Password. "
            "Your account will be erased forever."
        )
    }


def exact_match_evaluator(run, example) -> dict:
    """Check whether the answer matches the reference exactly."""
    actual = run.outputs["answer"]
    expected = example.outputs["answer"]

    return {
        "key": "exact_match",
        "score": actual == expected,
    }


def password_reset_criteria_evaluator(run, example) -> dict:
    """Check password-reset instructions only when relevant."""
    question = example.inputs["question"].lower()
    actual = run.outputs["answer"].lower()

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

    reset_related = any(phrase in question for phrase in reset_phrases)

    if not reset_related:
        return {
            "key": "password_reset_criteria",
            "score": None,
            "comment": "Not applicable to this question.",
        }

    required_phrases = [
        "login page",
        "forgot password",
    ]

    misleading_phrases = [
        "permanently delete your account",
        "delete your account",
        "erased forever",
        "permanently lose access to your account",
        "lose access to your account",
    ]

    has_required_phrases = all(phrase in actual for phrase in required_phrases)

    has_misleading_content = any(phrase in actual for phrase in misleading_phrases)

    passed = has_required_phrases and not has_misleading_content

    return {
        "key": "password_reset_criteria",
        "score": passed,
    }


def main():
    client = Client()

    evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[
            exact_match_evaluator,
            password_reset_criteria_evaluator,
        ],
        experiment_prefix="support-assistant-categorized-tracing",
        client=client,
    )

    evaluate(
        misleading_target,
        data=DATASET_NAME,
        evaluators=[
            exact_match_evaluator,
            password_reset_criteria_evaluator,
        ],
        experiment_prefix="support-assistant-misleading-test",
        client=client,
    )

    print("LangSmith evaluation finished.")
    print("Open LangSmith to inspect the experiment and scores.")


if __name__ == "__main__":
    main()
