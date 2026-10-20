
import json

from langsmith import Client

DATASET_NAME = "support-assistant-evaluation-v1"


def main():
    client = Client()

    dataset = client.read_dataset(dataset_name=DATASET_NAME)

    with open("evaluation_examples.json", encoding="utf-8") as file:
        examples = json.load(file)

    existing_examples = client.list_examples(dataset_id=dataset.id)

    existing_questions = {
        example.inputs.get("question")
        for example in existing_examples
    }

    missing_examples = [
        item
        for item in examples
        if item["question"] not in existing_questions
    ]

    if not missing_examples:
        print("Dataset is already up to date.")
        return

    client.create_examples(
        dataset_id=dataset.id,
        examples=[
            {
                "inputs": {"question": item["question"]},
                "outputs": {"answer": item["expected_answer"]},
            }
            for item in missing_examples
        ],
    )

    print(f"Dataset: {DATASET_NAME}")
    print(f"New examples added: {len(missing_examples)}")
    print(f"Previous examples: {len(existing_questions)}")
    print(f"Current total: {len(existing_questions) + len(missing_examples)}")


if __name__ == "__main__":
    main()
