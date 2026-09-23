# Assignment Time Estimator

Plan coursework using your own history of estimated and actual hours. Log completed tasks, then enter a first estimate for new work to see an adjusted planning time.

## Features

- Records task title, type, original estimate, actual hours, and completion date.
- Uses tasks of the same type when at least three are available; otherwise uses all records.
- With five or more varied examples, fits a simple linear regression from estimated to actual hours.
- With three or four examples, adjusts by the median actual/estimated ratio; with fewer, preserves your estimate.
- Compares original and adjusted errors by leaving one logged task out at a time.

## Run locally

```bash
git clone https://github.com/Ayanshxkeel/assignment-time-estimator.git
cd assignment-time-estimator
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit. On Windows, activate with `.venv\Scripts\activate`.

## Try it

Log three **Coding** tasks, each estimated at 2 hours and completed in 3 hours. For a new Coding task estimated at 4 hours, the suggestion should be 6 hours. Add two more tasks with different estimates to activate the regression and leave-one-out error comparison.

## How it works

`logic.py` stores tasks in SQLite. `predict()` first chooses relevant history, then fits `statistics.linear_regression()` when enough varied data exists. Otherwise, it uses a median ratio or your original estimate. `backtest()` holds each task out in turn to compare the adjusted estimate with the original estimate. `app.py` builds the interface.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Forms, metrics, and history display |
| `logic.py` | SQLite storage, estimation, and backtest |
| `requirements.txt` | Python dependencies |

## Data and limitations

Records stay in a local `assignments.db` file. Stop the app and delete that file to start fresh. The model learns only from your small history; future tasks may differ. If the adjusted error is worse than your original estimates, the app tells you rather than claiming an improvement.
