## Latest Evaluation Results

**Evaluation date:** November 25, 2026

**Dataset:** 25 questions (17 answerable, 8 unanswerable)

### Results

| Metric | Result |
|---|---:|
| Total questions | 25 |
| Successful API requests | 25 |
| Failed API requests | 0 |
| Retrieval coverage | 100% |
| Refusal accuracy | 100% |
| API success rate | 100% |

### Evaluation methodology

- **Retrieval coverage:** Percentage of answerable questions for which the retrieval system returned at least one chunk.
- **Refusal accuracy:** Percentage of unanswerable questions for which the system returned a refusal containing an expected refusal phrase.
- **API success rate:** Percentage of evaluation requests that returned HTTP 200 successfully.

### Limitations

- Retrieval coverage measures chunk availability, not semantic relevance or answer correctness.
- Refusal accuracy uses phrase matching rather than human judgment or an independent LLM evaluator.
- Results represent this 25-question test dataset and should not be interpreted as a guarantee of production performance.
- Relevance-based Hit Rate@k and MRR require labeled relevant documents or chunks and are not reported in this evaluation.

### Conclusion

The system successfully processed all 25 evaluation requests. It retrieved at least one chunk for all 17 answerable questions and correctly refused all 8 unanswerable questions under the current evaluation criteria.