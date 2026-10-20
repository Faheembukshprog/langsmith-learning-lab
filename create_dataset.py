
import json

from langsmith import Client

DATASET_NAME = "support-assistant-evaluation-v1"


def main():
    client = Client()

    with open("evaluation_examples.json", encoding="utf-8") as file:
        examples = json.load(file)

    if client.has_dataset(dataset_name=DATASET_NAME):
        print(f"Dataset already exists: {DATASET_NAME}")
        print("No examples were uploaded again.")
        return

    dataset = client.create_dataset(
        dataset_name=DATASET_NAME,
        description=(
            "Evaluation examples for the beginner LangSmith "
            "support assistant project."
        ),
    )

    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": {"question": item["question"]},
                "outputs": {"answer": item["expected_answer"]},
            }
            for item in examples
        ],
    )

    print(f"Dataset created: {dataset.name}")
    print(f"Examples uploaded: {len(examples)}")


if __name__ == "__main__":
    main()
