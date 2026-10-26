import json
import os

from dotenv import load_dotenv
from langsmith import Client

load_dotenv()

os.environ.setdefault(
    "LANGSMITH_ENDPOINT",
    "https://apac.api.smith.langchain.com",
)

DATASET_NAME = "support-assistant-evaluation-v1"
NEW_QUESTION = "How do I keep my password secure?"


def main():
    client = Client()

    with open("evaluation_examples.json", encoding="utf-8") as file:
        examples = json.load(file)

    item = next(example for example in examples if example["question"] == NEW_QUESTION)

    dataset = client.read_dataset(dataset_name=DATASET_NAME)
    existing_examples = client.list_examples(dataset_id=dataset.id)

    for example in existing_examples:
        if example.inputs.get("question") == NEW_QUESTION:
            print("Example already exists. Nothing was added.")
            return

    client.create_example(
        inputs={"question": item["question"]},
        outputs={"answer": item["expected_answer"]},
        dataset_id=dataset.id,
    )

    print(f"Added example: {NEW_QUESTION}")


if __name__ == "__main__":
    main()
