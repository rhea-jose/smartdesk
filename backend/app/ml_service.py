import os
import joblib

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ML_DIR=os.path.join(BASE_DIR,"ml")

_category_model =joblib.load(
    os.path.join(ML_DIR,"category_model.joblib")
)

_category_vectorizer=joblib.load(
    os.path.join(ML_DIR,"category_vectorizer.joblib")
)

_priority_model = joblib.load(
    os.path.join(ML_DIR, "priority_model.joblib")
)

_priority_vectorizer = joblib.load(
    os.path.join(ML_DIR, "priority_vectorizer.joblib")
)

def predict_category(text:str) ->str:
    vec=_category_vectorizer.transform([text])
    return _category_model.predict(vec)[0]

def predict_priority(text:str) ->str:
    vec=_priority_vectorizer.transform([text])
    return _priority_model.predict(vec)[0]

def predict_ticket(text:str) -> dict:
    return {
        "category": predict_category(text),
        "priority":predict_priority(text)
    }