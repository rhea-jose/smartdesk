# SmartDesk — AI-Powered Support Ticket Triage

## Problem

Support teams manually read and route incoming tickets, which is slow and inconsistent.
SmartDesk automatically classifies tickets by category and priority, and gives agents
a dashboard to manage the queue.

## Users

- **Customers** submit tickets through a simple form.
- **Agents** view a dashboard, update ticket status, and rely on AI-suggested category/priority.

## Success criteria

- Tickets are auto-classified into category and priority on submission.
- Agents can update ticket status through the dashboard.
- The app is deployed, tested, and documented.

## Tech stack

- **Backend:** FastAPI, SQLAlchemy, SQLite (dev)
- **ML:** scikit-learn (TF-IDF + Logistic Regression)
- **Frontend:** React (Vite) — coming Day 5
- **Testing:** pytest
- **Deployment:** Azure / AWS — coming Day 6

## Dataset

20,000 synthetic customer support tickets (Kaggle, MIT license), covering 8 fictional
products (CloudDrive, PayWallet, FitBand X, StreamPlus, etc.), with fields: message,
category, priority, sentiment, channel, product.

## ML Model Notes

- Trained TF-IDF + Logistic Regression for both `category` and `priority` prediction.
- **Category:** 92% accuracy. The raw dataset gave 100% because the text is
  template-generated with disjoint vocabulary per category (e.g. Shipping messages
  always contain "arrived"/"damaged"). Added 8% label noise and filler-sentence
  injection to simulate real-world messiness, bringing accuracy to a believable range.
- **Priority:** initially 100% accuracy due to a literal leak — an "Urgent:" prefix
  and phrases like "Need this fixed ASAP" directly encoded the label in the text.
  After stripping these phrases and adding label noise, accuracy dropped to 81%.
  Inspecting the model's top coefficients showed the remaining signal was incidental
  phrasing correlated with category (e.g. greeting words, product-inquiry phrasing),
  not genuine urgency cues. This suggests the dataset's priority labels aren't
  strongly grounded in message text — in a real system, priority would likely need
  additional signals (customer tier, SLA rules, sentiment) beyond raw text alone.

## API

- `POST /tickets` — creates a ticket; `category` and `priority` are predicted
  automatically from the description at creation time (no manual labeling needed).
- `POST /predict` — standalone endpoint that returns `{category, priority}` for
  any text, without creating a ticket. Useful for testing the model directly.
- `GET /tickets`, `GET /tickets/{id}`, `PATCH /tickets/{id}`, `DELETE /tickets/{id}`
  — standard ticket CRUD (see Day 1).
  
## Frontend

React (Vite) single-page app with two parts:
- **Ticket submission form** — customers submit a title and description; the
  ticket is created via `POST /tickets` and immediately shows its AI-predicted
  category and priority.
- **Agent dashboard** — lists all tickets with category, priority, and a status
  dropdown (open / in_progress / resolved), filterable by status. Status changes
  are saved via `PATCH /tickets/{id}` with an optimistic UI update.

### Running the frontend

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Requires the backend running separately on `http://127.0.0.1:8000` (CORS is
configured to allow `http://localhost:5173`).

## Setup
This project has two parts: `backend/` (FastAPI + ML) and `frontend/` (React).
Run both simultaneously in separate terminals.

\`\`\`bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`

Seed the database (requires the dataset CSV in `data/`):

\`\`\`bash
python scripts/seed_data.py
\`\`\`

Run tests:

\`\`\`bash
python -m pytest -v
\`\`\`

Train models:

\`\`\`bash
python ml/add_noise.py
python ml/train_category.py
python ml/train_priority.py
\`\`\`


## Status

- [x] Day 1: Backend, ticket CRUD, tests
- [x] Day 2: Dataset seeded (20k tickets)
- [x] Day 3: Category and priority classifiers trained and evaluated
- [x] Day 4: Wire models into `/predict` API endpoint
- [x] Day 5: React frontend
- [ ] Day 6: Integration, CI, deployment
- [ ] Day 7: Polish, demo video