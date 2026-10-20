
from langsmith import Client
from langsmith.evaluation import evaluate

from app import answer_question

DATASET_NAME = "support-assistant-evaluation-v1"


def target(inputs: dict) -> dict:
    """Run the support assistant on one dataset example."""
    return answer_question(inputs["question"])


def exact_match_evaluator(run, example) -> dict:
    """Score whether the generated answer exactly matches the reference."""
    actual = run.outputs["answer"]
    expected = example.outputs["answer"]

    return {
        "key": "exact_match",
        "score": actual == expected,
    }


def main():
    client = Client()

    results = evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[exact_match_evaluator],
        experiment_prefix="support-assistant-baseline",
        client=client,
    )

    print("LangSmith evaluation finished.")
    print("Open LangSmith to inspect the experiment and scores.")


if __name__ == "__main__":
    main()
