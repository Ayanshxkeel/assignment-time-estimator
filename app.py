from datetime import date
import pandas as pd
import streamlit as st
from logic import add_task, backtest, connect, predict, tasks

st.set_page_config(page_title="Assignment Time Estimator", page_icon="⏱️", layout="wide")
st.title("Assignment Time Estimator")
st.caption("Learn from how long your coursework actually takes. Your records stay on this computer.")
db = connect()
categories = ["Problem set", "Coding", "Reading", "Writing", "Exam study", "Other"]
with st.form("completed"):
    st.subheader("Log completed work")
    title = st.text_input("Task title")
    category = st.selectbox("Type", categories)
    c1, c2, c3 = st.columns(3)
    estimated = c1.number_input("Original estimate (hours)", 0.25, 100.0, 2.0, 0.25)
    actual = c2.number_input("Actual time (hours)", 0.25, 100.0, 3.0, 0.25)
    due = c3.date_input("Completion date", date.today())
    if st.form_submit_button("Save completed task"):
        try:
            add_task(db, title, category, estimated, actual, str(due))
            st.success("Saved.")
        except ValueError as error:
            st.error(str(error))
rows = tasks(db)
st.subheader("Plan new work")
new_category = st.selectbox("New task type", categories, key="new_type")
new_estimate = st.number_input("Your first estimate (hours)", 0.25, 100.0, 2.0, 0.25, key="new_estimate")
predicted, method, count = predict(rows, new_category, new_estimate)
st.metric("Suggested planning time", f"{predicted:.1f} hours")
st.caption(f"Method: {method}. Based on {count} records. With at least five varied estimates, the app fits a simple linear regression; otherwise it uses a median ratio or your original estimate.")
if rows:
    st.subheader("Your history")
    frame = pd.DataFrame(rows, columns=["ID", "Task", "Type", "Estimated hours", "Actual hours", "Date"])
    st.dataframe(frame.drop(columns="ID"), hide_index=True, width="stretch")
    result = backtest(rows)
    if result:
        st.write(f"**Leave-one-out error:** original estimates {result[0]:.2f} hours; adjusted estimates {result[1]:.2f} hours. Lower is better.")
        if result[1] >= result[0]:
            st.info("The adjustment has not beaten your original estimates yet. More history may help; use your own judgment.")
else:
    st.info("Log a few completed tasks to see whether you tend to underestimate or overestimate your work.")
