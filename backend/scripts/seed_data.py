"""
One-time script to load the Kaggle dataset into our tickets table.
Run from the backend folder: python scripts/seed_data.py
"""

import sys
import os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from app.database import SessionLocal,Base,engine

from app import models
CSV_PATH="../data/customer_support_tickets.csv"
import random

STATUS_WEIGHTS = ["open"] * 5 + ["in_progress"] * 3 + ["resolved"] * 2  # ~50/30/20
# Map the dataset's free-text message into our title/description split.
# We use the first ~60 chars as a title since the dataset has no subject line.

def make_title(message:str) -> str:
    message=message.strip()
    if len(message)<=60:
        return message
    return message[:57]+"..."

def main():
    Base.metadata.create_all(bind=engine)
    df=pd.read_csv(CSV_PATH)
    print(f"Loaded {len(df)} rows from CSV")

    db=SessionLocal()
    inserted=0
    try:
        for _,row in df.iterrows():
            ticket=models.Ticket(
                title=make_title(row["message"]),
                description=row["message"],
                category=row['category'],
                priority=row["priority"],
                product=row.get("product"),
                channel=row.get("channel"),
                sentiment=row.get("sentiment"),
                status=random.choice(STATUS_WEIGHTS)
            )
            db.add(ticket)
            inserted+=1
            if inserted%500==0:
                db.commit()
                print(f"..{inserted} rows inserted")

        db.commit()

    finally:
        db.close()
        print(f"Done. Inserted {inserted} tickets.")

if __name__=='__main__':
    main()