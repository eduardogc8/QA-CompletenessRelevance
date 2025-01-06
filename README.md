
# QA-CompletenessRelevance

This repository provides the dataset and associated resources described in the paper:

> **Beyond Accuracy: Completeness and Relevance Metrics for Evaluating the Quality of Long Answers**  
> *[Citation details will be made available soon. This article is currently under submission.]*

---

## Overview

**QA-CompletenessRelevance** is a resource for evaluating the **completeness** and **relevance** of long-form answers in question answering systems, particularly within instruction question (e.g., "How to..."). 

Our goal is to offer:

- A **benchmark dataset** comprising pairs of questions and answers, each annotated by expert judges with scores for completeness and relevance.
- **Reference answers** for select questions, created by domain experts (Computer Science).

### Key Features

1. **Instruction-Focused**: The dataset targets instruction-type questions in Computer Science, ensuring a controlled environment for evaluation of answer quality.
2. **Human Annotations**: Each answer is assigned a numerical score (0-100) for both completeness and relevance by at least four annotators with Computer Science backgrounds.
3. **Expert-Curated References**: Includes carefully selected or developed reference answers for benchmarking.
4. **Compatibility with Traditional Metrics**: Can be used to contrast new evaluation models against BLEU, ROUGE, BERTScore, etc.

---

## Annotations

### Completeness
Scores range from 0 to 100, indicating the extent to which an answer addresses all essential points of the question.

### Relevance
Scores range from 0 to 100, reflecting how focused and pertinent the answer is to the original question.

### Inter-Annotator Agreement among Four Annotators
- **Completeness**: Intraclass Correlation Coefficient (ICC) of ~0.78  
- **Relevance**: Intraclass Correlation Coefficient (ICC) of ~0.58  

See the paper (section [Dataset Construction](#)) for a detailed analysis of the annotation process and agreement metrics.

---

## License

This project is licensed under the [MIT License](LICENSE), which allows free, open-source distribution and reuse.

---

## Citation

If you use this dataset in your research or application, please cite:

> **LongAnswerQA-Metrics: A Dataset for Evaluating Completeness and Relevance in Long Answers**  
> *[Will be made available.]*

---

## Contact

For inquiries, suggestions, or further collaborations, please contact at eduardogcortes8@gmail.com.

---
