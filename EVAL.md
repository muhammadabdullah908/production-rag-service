@'
# RAG System Evaluation

**Evaluation date:** November 25, 2026

## Dataset
The golden dataset contains 25 questions:
- Answerable: 18
- Unanswerable: 7

## Results

| Metric | Result |
|---|---:|
| Total questions | 25 |
| Successful API requests | 25 |
| Failed API requests | 0 |
| Answerable questions with retrieved chunks | 18/18 |
| Correctly refused unanswerable questions | 7/7 |
| Retrieval coverage | 100% |
| Refusal accuracy | 100% |
| API success rate | 100% |

## Methodology
- Retrieval coverage measures the percentage of answerable questions that returned at least one chunk.
- Refusal accuracy measures the percentage of unanswerable questions that matched the expected refusal criteria.
- API success rate measures requests completed with HTTP 200.

## Limitations
- Retrieved chunks are not necessarily semantically relevant.
- Refusal evaluation uses automated phrase matching, not human judgment.
- The dataset contains only 25 questions.
- Hit Rate@k and MRR are not reported because labeled relevant chunks are unavailable.
- These results do not guarantee production performance.

## Conclusion
All 25 evaluation requests completed successfully. All 18 answerable questions returned chunks, and all 7 unanswerable questions were refused according to the evaluation criteria.
'@ | Set-Content -Encoding utf8 .\EVAL.md