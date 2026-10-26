import json

from app import answer_question


def main():
    with open("evaluation_examples.json", encoding="utf-8") as file:
        examples = json.load(file)

    passed = 0

    for example in examples:
        question = example["question"]
        expected = example["expected_answer"]
        result = answer_question(question)
        actual = result["answer"]

        correct = actual == expected

        if correct:
            passed += 1

        print(f"Question: {question}")
        print(f"Expected: {expected}")
        print(f"Actual:   {actual}")
        print(f"Result:   {'PASS' if correct else 'FAIL'}")
        print("-" * 50)

    accuracy = passed / len(examples) * 100 if examples else 0

    print(f"Evaluation: {passed}/{len(examples)} passed")
    print(f"Accuracy: {accuracy:.1f}%")


if __name__ == "__main__":
    main()
