---
license: mit
language:
  - en
pretty_name: QA-CompletenessRelevance
size_categories:
  - n<1K
task_categories:
  - question-answering
annotations_creators:
  - expert-generated
language_creators:
  - found
  - machine-generated
source_datasets:
  - extended|eli5
tags:
  - evaluation
  - meta-evaluation
  - evaluation-metrics
  - long-form-qa
  - non-factoid-qa
  - completeness
  - relevance
  - llm-as-a-judge
  - human-annotation
  - computer-science
configs:
  - config_name: answers
    default: true
    data_files:
      - split: test
        path: data/answers.parquet
  - config_name: pairs
    data_files:
      - split: test
        path: data/pairs.parquet
---

# QA-CompletenessRelevance

**How complete is an answer? How relevant is it? This dataset has human answers to both.**

[![GitHub](https://img.shields.io/badge/GitHub-QA--CompletenessRelevance-black)](https://github.com/eduardogc8/QA-CompletenessRelevance)
[![Model](https://img.shields.io/badge/%F0%9F%A4%97%20Model-qa--completeness--regressor-yellow)](https://huggingface.co/egcortes/qa-completeness-regressor)
[![Paper](https://img.shields.io/badge/Paper-Lang%20Resources%20%26%20Evaluation-blue)](https://doi.org/10.1007/s10579-026-09936-6)

106 "How to..." questions about Computer Science. Each one has two long answers, one written by a
Reddit user and one written by GPT-4. **Four annotators scored every answer from 0 to 100 for
completeness and for relevance.** Each question also comes with a reference answer written by an
expert.

Use it to check whether *your* evaluation metric agrees with human judgement.

A model that scores completeness without a reference answer is at
[egcortes/qa-completeness-regressor](https://huggingface.co/egcortes/qa-completeness-regressor).

From the paper *Beyond accuracy: completeness and relevance metrics for evaluating the quality of
long answers*, **Language Resources and Evaluation** 60(3), article 58 (2026). It is open access:
[doi.org/10.1007/s10579-026-09936-6](https://doi.org/10.1007/s10579-026-09936-6).

---

## Quick start

```python
from datasets import load_dataset

data = load_dataset("egcortes/qa-completeness-relevance")["test"]
print(data[0]["question"], data[0]["completeness"], data[0]["relevance"])
```

CSV and JSON versions, and the script that builds them, are on
[GitHub](https://github.com/eduardogc8/QA-CompletenessRelevance).

---

## Dataset

Two configurations, one `test` split each. This is an evaluation set, so there is no training split.

| Config | Rows | What it is |
|---|---|---|
| `answers` (default) | 212 | One row per scored answer. **Start here.** |
| `pairs` | 106 | One row per question, both answers side by side. |

Columns in `answers`:

| Column | Type | What it is |
|---|---|---|
| `question_id` | string | ELI5 / Reddit submission id |
| `question` | string | The question |
| `answer` | string | The answer that was scored |
| `answer_source` | string | `human` (Reddit user) or `gpt4` |
| `completeness` | float | 0 to 100, average of 4 annotators |
| `relevance` | float | 0 to 100, average of 4 annotators |
| `reference_answer` | string | Expert answer for this question. Not scored itself. |

Columns in `pairs`: `question_id`, `question`, `reference_answer`, `human_answer`,
`human_completeness`, `human_relevance`, `gpt4_answer`, `gpt4_completeness`, `gpt4_relevance`.

**Completeness**: does the answer cover everything the question asks for?
**Relevance**: is everything in the answer about what was asked?

The two scores only correlate at **r = 0.41**, so they really do measure different things.

The human answers are Reddit comments from r/explainlikeimfive, taken from the
[ELI5 dataset](https://huggingface.co/datasets/defunct-datasets/eli5) (Fan et al., 2019), and belong
to the people who wrote them. If you wrote one of them and want it removed, email
eduardogcortes8@gmail.com.

---

## Statistics

| | n | mean | median | sd |
|---|---|---|---|---|
| Completeness, all | 212 | 61.9 | 63.0 | 24.0 |
| Completeness, human | 106 | 52.1 | 54.6 | 20.3 |
| Completeness, GPT-4 | 106 | 71.6 | 80.0 | 23.5 |
| Relevance, all | 212 | 76.8 | 83.0 | 20.9 |
| Relevance, human | 106 | 65.9 | 67.0 | 22.8 |
| Relevance, GPT-4 | 106 | 87.8 | 90.5 | 10.6 |

Agreement between the four annotators, ICC(3,k): **0.78** for completeness [0.73, 0.83] and **0.58**
for relevance [0.48, 0.67]. Relevance is the harder, more subjective one.

The annotators preferred the GPT-4 answer in 96 of 106 questions on completeness, and 81 of 106 on
relevance.

---

## Evaluating a metric

Score every answer, then compare with the humans the same two ways the paper does. Running this on
the paper's Gemini Flash scores reproduces its published numbers exactly (Spearman 0.7943,
accuracy 85.85%).

```python
from datasets import load_dataset
from scipy.stats import spearmanr

answers = load_dataset("egcortes/qa-completeness-relevance")["test"].to_pandas()
answers["my_score"] = [my_metric(q, a) for q, a in zip(answers.question, answers.answer)]

# 1. Correlation with the human scores, across all 212 answers.
print(spearmanr(answers.my_score, answers.completeness).statistic)

# 2. Pairwise accuracy: how often you pick the answer the annotators preferred.
#    A tie counts as wrong, because the metric did not actually choose.
w = answers.pivot(index="question_id", columns="answer_source",
                  values=["my_score", "completeness"])
mine, gold = w["my_score"], w["completeness"]
hit = (mine.gpt4 > mine.human) == (gold.gpt4 > gold.human)
print((hit & (mine.gpt4 != mine.human)).mean())
```

Swap `completeness` for `relevance` to evaluate the other criterion.

---

## Results

Spearman correlation with the human scores, across all 212 answers.

| Metric | Completeness | Relevance |
|---|---|---|
| GPT-4 (prompt-based) | **0.72** | **0.59** |
| ROUGE (vs reference answer) | 0.70 | 0.40 |
| GPT-3.5 (prompt-based) | 0.67 | 0.51 |
| Regression model (BERT, synthetic training) | 0.67 | 0.20 |
| Information Units (vs reference answer) | 0.63 | 0.51 |
| BERTScore (vs reference answer) | 0.55 | 0.54 |
| BLEU (vs reference answer) | 0.51 | 0.27 |
| BLEURT (vs reference answer) | 0.39 | 0.43 |

The paper has the rest: Kendall and Pearson coefficients, p-values, pairwise accuracy, separate
results for human and GPT-4 answers, and a check for self-preference bias using Llama 3.2, Mistral 7B
and Gemini Flash as judges.

---

## Citation

Please cite the paper:

```bibtex
@article{cortes2026beyond,
  title   = {Beyond accuracy: completeness and relevance metrics for
             evaluating the quality of long answers},
  author  = {Cortes, Eduardo G. and Vieira, Renata and Barone, Dante A. C.},
  journal = {Language Resources and Evaluation},
  volume  = {60},
  number  = {3},
  pages   = {58},
  year    = {2026},
  doi     = {10.1007/s10579-026-09936-6}
}
```

---

## Contact

eduardogcortes8@gmail.com
