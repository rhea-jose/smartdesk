"""
Trains a model to predict ticket `priority` from the ticket `description`.
Run from backend: python ml/train_priority.py
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib

CSV_PATH = "../data/customer_support_tickets_noisy.csv"
MODEL_OUT = "ml/priority_model.joblib"
VECTORIZER_OUT = "ml/priority_vectorizer.joblib"


def main():
    df = pd.read_csv(CSV_PATH)
    X = df["message"]
    y = df["priority"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words="english")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_test_vec)

    print("=== Priority Classifier ===")
    print(classification_report(y_test, y_pred))
    print("Confusion matrix (rows=actual, cols=predicted):")
    print(confusion_matrix(y_test, y_pred, labels=model.classes_))
    print("Labels order:", list(model.classes_))

    joblib.dump(model, MODEL_OUT)
    joblib.dump(vectorizer, VECTORIZER_OUT)
    print(f"\nSaved model to {MODEL_OUT}")
    print(f"Saved vectorizer to {VECTORIZER_OUT}")


if __name__ == "__main__":
    main()