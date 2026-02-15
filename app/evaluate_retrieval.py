import json
from rag_query import retrieve_chunks

EVAL_FILE = "data/eval_questions.json"
TOP_K = 3

with open(EVAL_FILE, "r", encoding="utf-8") as f:
    eval_data = json.load(f)

total = len(eval_data)

precision_total = 0
recall_total = 0
mrr_total = 0

for item in eval_data:
    question = item["question"]
    expected = item["expected_keyword"].lower()

    retrieved = retrieve_chunks(question, top_k=TOP_K)

    relevant_positions = []
    relevant_count = 0

    for i, chunk in enumerate(retrieved):
        if expected in chunk.lower():
            relevant_positions.append(i)
            relevant_count += 1

    # Precision@K
    precision = relevant_count / TOP_K
    precision_total += precision

    # Recall@K (since 1 relevant expected)
    recall = 1 if relevant_count > 0 else 0
    recall_total += recall

    # MRR
    if relevant_positions:
        rank = relevant_positions[0] + 1
        mrr_total += 1 / rank

    print("\nQuestion:", question)
    print("Precision@3:", precision)
    print("Recall@3:", recall)

avg_precision = precision_total / total
avg_recall = recall_total / total
mrr = mrr_total / total

print("\n--- RETRIEVAL METRICS ---")
print(f"Average Precision@{TOP_K}: {avg_precision:.2f}")
print(f"Average Recall@{TOP_K}: {avg_recall:.2f}")
print(f"MRR: {mrr:.2f}")
