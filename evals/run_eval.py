
import json
import httpx
from pathlib import Path

API_URL = "http://127.0.0.1:8001/api"
GOLDEN_SET = Path(__file__).parent / "golden_set.json"

REFUSAL_PHRASES = ["cannot answer", "not contain"]


def run_evaluation():
    with open(GOLDEN_SET, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    total = len(dataset)
    answerable_count = sum(item["answerable"] for item in dataset)
    unanswerable_count = total - answerable_count

    successful_requests = 0
    failed_requests = 0
    answerable_tested = 0
    unanswerable_tested = 0
    retrieval_hits = 0
    correct_refusals = 0

    print(f"Starting Evaluation on {total} questions...\n")

    with httpx.Client(timeout=90.0) as client:
        for i, item in enumerate(dataset, start=1):
            question = item["question"]
            is_answerable = item["answerable"]

            try:
                response = client.post(
                    f"{API_URL}/ask",
                    json={"question": question},
                )

                if response.status_code != 200:
                    failed_requests += 1
                    print(f"[{i}] API Error: {response.status_code}")
                    print(f"    Details: {response.text[:300]}")
                    continue

                successful_requests += 1
                result = response.json()

                chunks = result.get("retrieved_chunks", [])
                answer = result.get("answer", "").lower()

                if is_answerable:
                    answerable_tested += 1
                    if chunks:
                        retrieval_hits += 1
                        print(f"[{i}] Retrieved {len(chunks)} chunk(s)")
                    else:
                        print(f"[{i}] No chunks retrieved")
                else:
                    unanswerable_tested += 1
                    if any(phrase in answer for phrase in REFUSAL_PHRASES):
                        correct_refusals += 1
                        print(f"[{i}] Correctly refused")
                    else:
                        print(f"[{i}] Incorrect response to unanswerable question")
                        print(f"    Answer: {answer[:250]}")

            except httpx.RequestError as error:
                failed_requests += 1
                print(f"[{i}] Connection error: {error}")
            except (ValueError, KeyError) as error:
                failed_requests += 1
                print(f"[{i}] Invalid API response: {error}")

    print("\n" + "=" * 45)
    print("             EVALUATION RESULTS")
    print("=" * 45)
    print(f"Total Questions:                  {total}")
    print(f"Successful Requests:              {successful_requests}")
    print(f"Failed Requests:                  {failed_requests}")
    print(f"Answerable Questions:             {answerable_count}")
    print(f"Unanswerable Questions:           {unanswerable_count}")
    print(f"Successfully Tested Answerable:   {answerable_tested}")
    print(f"Successfully Tested Unanswerable: {unanswerable_tested}")

    if answerable_tested:
        print(f"Retrieval Coverage:               {retrieval_hits / answerable_tested:.2%}")
    else:
        print("Retrieval Coverage:               N/A")

    if unanswerable_tested:
        print(f"Refusal Accuracy:                 {correct_refusals / unanswerable_tested:.2%}")
    else:
        print("Refusal Accuracy:                 N/A")

    if total:
        print(f"API Success Rate:                 {successful_requests / total:.2%}")

    print("=" * 45)


if __name__ == "__main__":
    run_evaluation()
