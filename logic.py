import sqlite3
from statistics import linear_regression, median, mean


def connect(path="assignments.db"):
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, estimated REAL NOT NULL, actual REAL NOT NULL, due TEXT NOT NULL)")
    db.commit()
    return db


def add_task(db, title, category, estimated, actual, due):
    if not title.strip() or estimated <= 0 or actual <= 0:
        raise ValueError("Enter a title and positive estimated and actual hours.")
    db.execute("INSERT INTO tasks(title,category,estimated,actual,due) VALUES(?,?,?,?,?)", (title.strip(), category, estimated, actual, due))
    db.commit()


def tasks(db):
    return db.execute("SELECT id,title,category,estimated,actual,due FROM tasks ORDER BY due DESC,id DESC").fetchall()


def predict(rows, category, estimate):
    same = [row for row in rows if row[2] == category]
    examples = same if len(same) >= 3 else rows
    if len(examples) >= 5 and len({row[3] for row in examples}) >= 2:
        slope, intercept = linear_regression([row[3] for row in examples], [row[4] for row in examples])
        return round(max(0.25, intercept + slope * estimate), 1), "linear regression", len(examples)
    ratios = [row[4] / row[3] for row in examples] if len(examples) >= 3 else []
    factor = median(ratios) if ratios else 1.0
    return round(estimate * factor, 1), f"median time ratio × {factor:.2f}", len(ratios)


def backtest(rows):
    if len(rows) < 5:
        return None
    baseline, corrected = [], []
    for row in rows:
        rest = [other for other in rows if other[0] != row[0]]
        baseline.append(abs(row[3] - row[4]))
        corrected.append(abs(predict(rest, row[2], row[3])[0] - row[4]))
    return round(mean(baseline), 2), round(mean(corrected), 2)
