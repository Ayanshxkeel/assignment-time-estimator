# Assignment Time Estimator

Record your original hour estimate and actual time for completed coursework. With five or more varied examples, the app fits a simple linear regression from estimated to actual hours. With less data, it uses the median actual/estimated ratio; with fewer than three records it leaves your estimate unchanged. It prefers examples of the same task type when enough are available.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

## Try it

Log three Coding tasks, each estimated at 2 hours and completed in 3 hours. Enter a new Coding estimate of 4 hours. The suggested planning time should be 6 hours. After five records, the app compares your raw and adjusted errors by leaving each record out in turn.

Records are saved in `assignments.db`. The regression is a small model trained only on your own history, not a general-purpose AI system. A lower historical error is evidence it helped on your logged tasks only.
