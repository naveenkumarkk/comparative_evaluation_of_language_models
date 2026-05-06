# Prompt Variation used

### Variation 1 — Zero-shot strict binary output

```text
Task:
Decide whether R1 and R2 refer to the same app functionality and are semantically similar, using App Features 1 and App Features 2 as context.

Rules:
- 1 = same functionality / semantically similar
- 0 = different functionality / not semantically similar / uncertain
- If uncertain, return 0

Output constraint:
Return exactly one character: 0 or 1
No explanation.

Now classify:
App Features 1: "likes"
R1: "Is this true that the updated version of whatsapp will provide us video calling n likes & comments features???;I do wish there was a better(any) alert system like on your iPhone for when you get new alerts(comments, likes, messages)."
App Features 2: "liking"
R2: "Love the fact u can customize and listen offline ur play lists...also the up to date music you can Save instead of liking."

Answer:
```

### Variation 2 — JSON output with short reason

```text
You are a binary classifier.

Goal:
Given two app reviews (R1, R2) and their extracted features (F1 from R1, F2 from R2), decide whether F1 and F2 refer to the same app functionality in context of reviews R1 and R2.

Label rules:
- Return 1 if F1 and F2 describe the same functionality.
- Return 0 if they describe different functionality.
- Return 0 if uncertain.

Important:
- Use the review context, not feature words alone.
- If one feature is vague/noisy and cannot be confidently matched, return 0.

Output format:
Return exactly in this JSON format:
{"label": 0 or 1, "reason": "<one short sentence>"}

Input:
F1: "likes"
R1: "Is this true that the updated version of whatsapp will provide us video calling n likes & comments features???;I do wish there was a better(any) alert system like on your iPhone for when you get new alerts(comments, likes, messages)."

F2: "liking"
R2: "Love the fact u can customize and listen offline ur play lists...also the up to date music you can Save instead of liking."

Answer:
```

### Variation 3 — Detailed rule-based feature comparison prompt

```text
You are a feature comparison assistant.

Your task is to determine whether two app features refer to the same feature or different features.

Core principle:
Two app features are considered the same only if they act on the exact same task target.

The task target includes:
- the object the feature acts upon
- the action performed
- the context or method of use

If any of these differ, the features are different.

Rules:
1. If the action and target are the same, classify as Same Feature.
2. If the action is similar but the target differs, classify as Different Feature.
3. If one feature is specific and the other is general, classify as Different Feature.
4. Singular and plural forms of the same feature are considered the same.
5. Reviews are used only to clarify unclear feature names, not to redefine the feature.

Output:
Return 0 for Different Feature and 1 for Same Feature.
Include a brief explanation.

Now analyze:

Feature 1: likes
Review 1: Is this true that the updated version of whatsapp will provide us video calling n likes & comments features???;I do wish there was a better(any) alert system like on your iPhone for when you get new alerts(comments, likes, messages).

Feature 2: liking
Review 2: Love the fact u can customize and listen offline ur play lists...also the up to date music you can Save instead of liking.

Output:
```

### Variation 4 — Few-shot task-target prompt

```text
You are a feature comparison assistant.

Rules:
1. Two app features are considered the same only if they act on the same task target.
2. If the task targets differ, even if the general goal is similar, they are different features.
3. Singular vs plural variations are considered the same feature.
4. Focus on the task target described by the feature and review context.
5. Ignore superficial wording similarity.

Task:
Given two app features and their corresponding user reviews, determine whether they refer to the same feature or different features.

Respond with:
- 1 for Same Feature
- 0 for Different Feature

Examples:

Feature 1: "clip selected text"
Review 1: "I clip selected text, web pages and links and can access them later on any of my devices."

Feature 2: "clip web pages"
Review 2: "I clip selected text, web pages and links and can access them later on any of my devices."

Classification: 0
Explanation: The targets differ: one refers to selected text, while the other refers to web pages.

Feature 1: "likes"
Review 1: "Is this true that the updated version of WhatsApp will provide us video calling n likes & comments features???"

Feature 2: "liking"
Review 2: "Love the fact u can customize and listen offline ur playlists...also the up to date music you can Save instead of liking."

Classification: 0
Explanation: The action is similar, but the targets and app contexts differ: WhatsApp likes/comments versus liking music.

Now analyze:

Feature 1: likes
Review 1: Is this true that the updated version of whatsapp will provide us video calling n likes & comments features???;I do wish there was a better(any) alert system like on your iPhone for when you get new alerts(comments, likes, messages).

Feature 2: liking
Review 2: Love the fact u can customize and listen offline ur play lists...also the up to date music you can Save instead of liking.

Output:
```

### Variation 5 — Senior Product Manager / semantic analyst prompt

```text
Role:
You are a Senior Product Manager and Semantic Analyst.

Task:
Determine whether two extracted app features are functionally equivalent.

Decision logic:
- Output 1 if both features describe the same job-to-be-done, same action, and same target.
- Output 0 if they describe different user journeys, different objects, or different app contexts.
- Ignore small wording differences such as plural/singular or verb/noun form.
- Do not rely only on surface word similarity.

Examples:

Review 1: Works amazingly, along with Skitch, but I wish there was a way to import notes into a type of presentation app.
Feature 1: import notes

Review 2: I had my items to sell listed in minutes and there was even the option of importing pictures from my phone.
Feature 2: importing pictures

Output: 0

Review 1: I have so much fun sending voice messages, songs, videos, and pictures.
Feature 1: sending pictures

Review 2: The icon for sending images is there but no options for pics or stickers come up.
Feature 2: sending images

Output: 1

Data:

Review 1: Is this true that the updated version of whatsapp will provide us video calling n likes & comments features???;I do wish there was a better(any) alert system like on your iPhone for when you get new alerts(comments, likes, messages).
Feature 1: likes

Review 2: Love the fact u can customize and listen offline ur play lists...also the up to date music you can Save instead of liking.
Feature 2: liking

Output:
```
