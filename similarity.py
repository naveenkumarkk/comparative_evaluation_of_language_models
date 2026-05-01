import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import accuracy_score, f1_score, cohen_kappa_score, confusion_matrix

# ==============================
# 1. Load data
# ==============================
# Replace with your actual file name
INPUT_CSV = "100_GT.csv"
OUTPUT_CSV = "pair_similarity_results.csv"
THRESHOLD_GRID_STEP = 0.01

df = pd.read_csv(INPUT_CSV)

# Expected columns:
# "APP Features 1", "Review 1", "APP Features 2", "Review 2", "Annotation"

# ==============================
# 2. Clean text columns
# ==============================
feature2_col = "APP Features 2" if "APP Features 2" in df.columns else "App Features 2"
text_cols = ["APP Features 1", "Review 1", feature2_col, "Review 2"]

for col in text_cols:
    df[col] = df[col].fillna("").astype(str).str.strip()

# Ground truth column:
# 1 = Same / Grouped
# 0 = Different / Separate
df["Annotation"] = df["Annotation"].astype(int)

# ==============================
# 3. Function to compute cosine similarity row by row
# ==============================
def pairwise_tfidf_cosine(text1, text2):
    """
    Compute TF-IDF cosine similarity between two texts.
    Returns a value between 0 and 1 in most practical cases.
    """
    # Create a vectorizer
    vectorizer = TfidfVectorizer()

    # Fit and transform the two texts together
    tfidf_matrix = vectorizer.fit_transform([text1, text2])

    # Compute cosine similarity between the two vectors
    sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

    return sim


def evaluate_threshold(y_true, sims, threshold):
    y_pred = (sims >= threshold).astype(int)
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    kappa = cohen_kappa_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
    tn, fp, fn, tp = cm.ravel()
    return {
        "threshold": threshold,
        "accuracy": acc,
        "f1": f1,
        "kappa": kappa,
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
    }


def pick_best(rows, metric):
    # Tie-break: higher F1, then threshold closest to 0.5 for stability
    return max(rows, key=lambda r: (r[metric], r["f1"], -abs(r["threshold"] - 0.5)))

# ==============================
# 4. Calculate similarities for each row
# ==============================
feature_sims = []
review_sims = []
combined_sims = []

for _, row in df.iterrows():
    feature_1 = row["APP Features 1"]
    review_1 = row["Review 1"]
    feature_2 = row[feature2_col]
    review_2 = row["Review 2"]

    # Feature-only similarity
    feature_sim = pairwise_tfidf_cosine(feature_1, feature_2)
    feature_sims.append(feature_sim)

    # Review-only similarity
    review_sim = pairwise_tfidf_cosine(review_1, review_2)
    review_sims.append(review_sim)

    # Combined text similarity
    left_text = feature_1 + " " + review_1
    right_text = feature_2 + " " + review_2
    combined_sim = pairwise_tfidf_cosine(left_text, right_text)
    combined_sims.append(combined_sim)

df["feature_similarity"] = feature_sims
df["review_similarity"] = review_sims
df["combined_similarity"] = combined_sims

# ==============================
# 5. Threshold search for best Kappa and Accuracy
# ==============================
thresholds = [round(i * THRESHOLD_GRID_STEP, 4) for i in range(int(1 / THRESHOLD_GRID_STEP) + 1)]
y_true = df["Annotation"]

all_eval_rows = []
for sim_col in ["feature_similarity", "review_similarity", "combined_similarity"]:
    sims = df[sim_col]
    for t in thresholds:
        res = evaluate_threshold(y_true, sims, t)
        res["similarity_type"] = sim_col
        all_eval_rows.append(res)

eval_df = pd.DataFrame(all_eval_rows)

best_rows = []
for sim_col in ["feature_similarity", "review_similarity", "combined_similarity"]:
    subset = eval_df[eval_df["similarity_type"] == sim_col].to_dict(orient="records")
    best_kappa = pick_best(subset, "kappa")
    best_acc = pick_best(subset, "accuracy")
    best_rows.append((sim_col, best_kappa, best_acc))

# ==============================
# 6. Save predictions using best threshold by Kappa on combined similarity
# ==============================
best_combined_kappa = [r for s, r, _ in best_rows if s == "combined_similarity"][0]
best_threshold = best_combined_kappa["threshold"]
df["Prediction"] = (df["combined_similarity"] >= best_threshold).astype(int)

y_pred = df["Prediction"]
accuracy = accuracy_score(y_true, y_pred)
f1 = f1_score(y_true, y_pred, zero_division=0)
kappa = cohen_kappa_score(y_true, y_pred)
cm = confusion_matrix(y_true, y_pred, labels=[0, 1])
tn, fp, fn, tp = cm.ravel()

print("Best threshold (combined_similarity) by Kappa:", best_threshold)
print("Accuracy:", accuracy)
print("F1 Score:", f1)
print("Cohen's Kappa:", kappa)
print("Confusion Matrix [[TN, FP], [FN, TP]]:")
print([[int(tn), int(fp)], [int(fn), int(tp)]])

# ==============================
# 7. Save output files
# ==============================
df.to_csv(OUTPUT_CSV, index=False)
eval_df.to_csv("threshold_search_results.csv", index=False)

lines = []
lines.append("TF-IDF Cosine Similarity Threshold Report")
lines.append(f"Input file: {INPUT_CSV}")
lines.append("")

for sim_col, bk, ba in best_rows:
    lines.append(f"Similarity Type: {sim_col}")
    lines.append("  Best by Kappa")
    lines.append(f"    Threshold: {bk['threshold']:.2f}")
    lines.append(f"    Kappa: {bk['kappa']:.4f}")
    lines.append(f"    Accuracy: {bk['accuracy']:.4f}")
    lines.append(f"    F1: {bk['f1']:.4f}")
    lines.append(f"    Confusion [[TN, FP], [FN, TP]]: [[{bk['tn']}, {bk['fp']}], [{bk['fn']}, {bk['tp']}]]")
    lines.append("  Best by Accuracy")
    lines.append(f"    Threshold: {ba['threshold']:.2f}")
    lines.append(f"    Accuracy: {ba['accuracy']:.4f}")
    lines.append(f"    Kappa: {ba['kappa']:.4f}")
    lines.append(f"    F1: {ba['f1']:.4f}")
    lines.append(f"    Confusion [[TN, FP], [FN, TP]]: [[{ba['tn']}, {ba['fp']}], [{ba['fn']}, {ba['tp']}]]")
    lines.append("")

report_path = "similarity_threshold_metrics.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("Saved:", OUTPUT_CSV)
print("Saved: threshold_search_results.csv")
print("Saved:", report_path)