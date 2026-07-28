"""Builds answers.csv/parquet and pairs.csv/parquet from data/final_dataset.json.

Run: python build_dataset.py
"""

import json
import os

import pandas as pd

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
LABELS = {"Human": "human", "GPT-4": "gpt4"}


def build_answers(questions):
    rows = [
        {
            "question_id": q["id"],
            "question": q["question"],
            "answer": ans["answer"],
            "answer_source": LABELS[ans["source"]],
            "completeness": float(ans["completeness_avg"]),
            "relevance": float(ans["relevance_avg"]),
            "reference_answer": q["reference_answer"],
        }
        for q in questions
        for ans in q["answers"]
    ]
    rows.sort(key=lambda r: (r["question_id"], r["answer_source"]))
    return pd.DataFrame(rows)


def build_pairs(questions):
    rows = []
    for q in questions:
        by_source = {a["source"]: a for a in q["answers"]}
        human, gpt4 = by_source["Human"], by_source["GPT-4"]
        rows.append({
            "question_id": q["id"],
            "question": q["question"],
            "reference_answer": q["reference_answer"],
            "human_answer": human["answer"],
            "human_completeness": float(human["completeness_avg"]),
            "human_relevance": float(human["relevance_avg"]),
            "gpt4_answer": gpt4["answer"],
            "gpt4_completeness": float(gpt4["completeness_avg"]),
            "gpt4_relevance": float(gpt4["relevance_avg"]),
        })
    rows.sort(key=lambda r: r["question_id"])
    return pd.DataFrame(rows)


def check(answers, pairs):
    assert len(answers) == 212 and len(pairs) == 106
    assert answers["question_id"].nunique() == 106
    assert set(answers["answer_source"]) == {"human", "gpt4"}
    for column in ("completeness", "relevance"):
        assert answers[column].between(0, 100).all()
        assert ((answers[column] * 4) % 1 == 0).all()
    assert answers.notna().all().all()


def main():
    with open(os.path.join(DATA, "final_dataset.json"), encoding="utf-8") as f:
        questions = json.load(f)

    answers, pairs = build_answers(questions), build_pairs(questions)
    check(answers, pairs)

    for df, name in [(answers, "answers"), (pairs, "pairs")]:
        df.to_csv(os.path.join(DATA, f"{name}.csv"), index=False, encoding="utf-8")
        df.to_parquet(os.path.join(DATA, f"{name}.parquet"), index=False)
        print(f"{name}: {len(df)} rows")


if __name__ == "__main__":
    main()
