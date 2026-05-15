import pandas as pd
import os

def build_data_only_prompt(f1, r1, f2, r2) -> str:
    # Keep it consistent and minimal; the SYSTEM prompt already defines the task.
    return f"""
You are a feature comparison assistant.

Your task is to determine whether two app features refer to the same feature or different features.

CORE PRINCIPLE

Two app features are considered the same only if they act on the exact same task target.

The task target includes:

- the object the feature acts upon
- the action performed
- the context or method of use

If any of these differ, the features are different.

STRICT EVALUATION PROCESS

Follow these steps in order before making a decision:

Step 1: Identify the Task

Determine the action described in each feature.

Step 2: Identify the Task Target

Determine the object the action applies to, using the feature name first.

Step 3: Use Reviews Only for Clarification

Reviews are supporting context only. Do not change the task target defined in the feature name unless the feature name is unclear.

Step 4: Compare the Task Targets

If the targets differ in object, method, or context, classify them as Different Feature.

IMPORTANT RULES

Rule 1 — Specific vs Generic Targets

If one feature refers to a specific object and the other refers to general or unspecified access, they are Different Features.

Example:

"access notes" vs "have access" → Different Feature

Rule 2 — Different Objects

If the action is the same but the object differs, they are Different Features.

Example:

"clip selected text" vs "clip web pages" → Different Feature

Rule 3 — Context or Mode Differences

If features involve different controls, icons, modes, or contexts, they are Different Features.

Example:

"plus icon reactions" vs "smiley icon reactions" → Different Feature

Rule 4 — Singular vs Plural

Singular vs plural forms of the same feature refer to the same functionality.

Example:

"playlist" vs "playlists" → Same Feature

Rule 5 — Review Content Cannot Redefine the Feature

If reviews introduce new objects or contexts not mentioned in the feature name, ignore them when determining the task target.

OUTPUT FORMAT

Return the classification as:

1 → Same Feature

0 → Different Feature

Also include a brief explanation (1–2 sentences).

EXAMPLE

Feature 1: "clip selected text"

Review 1: "I clip selected text, web pages and links and can access them later."

Feature 2: "clip web pages"

Review 2: "I clip selected text, web pages and links and can access them later."

Classification: 0

Explanation: The task targets differ. One feature clips selected text while the other clips entire web pages.

NOW ANALYZE THE FOLLOWING PAIR


Feature 1: {f1}
Review 1: {r1}
Feature 2: {f2}
Review 2: {r2}

Return the output classification as : 0 for Different and 1 for same

"""


def generate_csv_prompts(input_path: str, output_path: str):
    df = pd.read_csv(input_path).fillna("")

    required = ["APP Features 1", "Review 1", "APP Features 2", "Review 2"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Missing required columns: {missing}. Found: {list(df.columns)}"
        )

    df_out = df.copy()
    df_out["Prompt"] = df_out.apply(
        lambda row: build_data_only_prompt(
            row["APP Features 1"],
            row["Review 1"],
            row["APP Features 2"],
            row["Review 2"],
        ),
        axis=1,
    )

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    df_out.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Saved: {output_path}")


# Example usage
generate_csv_prompts(
    input_path="hard_1000_reviews_fast_all_api_preds.csv",
    output_path="31_03/1000_data_sample_1.csv",
)
