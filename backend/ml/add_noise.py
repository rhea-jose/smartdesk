"""
Adds controlled noise to the clean synthetic dataset so it behaves more
like real-world data, where labels aren't perfectly separable from text.
Run from backend: python ml/add_noise.py
"""
import pandas as pd
import numpy as np

INPUT_PATH = "../data/customer_support_tickets.csv"
OUTPUT_PATH = "../data/customer_support_tickets_noisy.csv"

LABEL_NOISE_RATE = 0.08   # 8% of rows get a randomly wrong category label
FILLER_INSERT_RATE = 0.25 # 25% of messages get a generic filler sentence added

# Generic phrases that could plausibly appear in ANY category's message,
# which dilutes the category-specific keyword signal.
FILLERS = [
    "Please let me know as soon as possible.",
    "I've been a customer for a while now.",
    "This is quite frustrating to deal with.",
    "Thanks in advance for your help.",
    "I tried restarting but it didn't help.",
    "Let me know if you need more details.",
    "I hope this gets resolved quickly.",
    "Looking forward to your response.",
]


def main():
    rng = np.random.default_rng(42)  # fixed seed so results are reproducible
    df = pd.read_csv(INPUT_PATH)
    categories = df["category"].unique().tolist()

    # --- Label noise: randomly reassign some rows to a wrong category ---
    n_flip = int(len(df) * LABEL_NOISE_RATE)
    flip_indices = rng.choice(df.index, size=n_flip, replace=False)
    for idx in flip_indices:
        current = df.at[idx, "category"]
        choices = [c for c in categories if c != current]
        df.at[idx, "category"] = rng.choice(choices)

    # --- Priority label noise: same idea, for the priority column ---
    priorities = df["priority"].unique().tolist()
    n_flip_priority = int(len(df) * LABEL_NOISE_RATE)
    flip_priority_indices = rng.choice(df.index, size=n_flip_priority, replace=False)
    for idx in flip_priority_indices:
        current = df.at[idx, "priority"]
        choices = [p for p in priorities if p != current]
        df.at[idx, "priority"] = rng.choice(choices)

    import re

    def strip_priority_hints(message):
        # Remove the literal "Urgent:" prefix pattern that leaks the label
        message = re.sub(r"^Urgent:\s*", "", message)
        # Remove other priority-coded phrases so the model can't shortcut on them
        message = re.sub(r"\s*Need this fixed ASAP\.?", "", message)
        message = re.sub(r"\s*heyP\.?", "", message)
        message = re.sub(r"\s*hi\.?", "", message)
        message = re.sub(r"\s*hello\.?", "", message)
        message = re.sub(r"\s*hello team\.?", "", message)
        return message.strip()

    # --- Text noise: insert a generic filler sentence into some messages ---
    def maybe_add_filler(message):
        if rng.random() < FILLER_INSERT_RATE:
            filler = rng.choice(FILLERS)
            return f"{message} {filler}"
        return message

    df["message"] = df["message"].apply(strip_priority_hints).apply(maybe_add_filler)

    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Flipped {n_flip} labels ({LABEL_NOISE_RATE:.0%})")
    print(f"Saved noisy dataset to {OUTPUT_PATH}")
    print(f"Shape: {df.shape}")


if __name__ == "__main__":
    main()