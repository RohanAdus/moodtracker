import streamlit as st
import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# connect to Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "service-account.json", scope
)
gc = gspread.authorize(creds)
SHEET_ID = "1ZC7Lk3SYWpaEOq16RBRQLC0Is_dI7RO6QpERBRizIqQ"
ws = gc.open_by_key(SHEET_ID).sheet1

# function to fetch data without altering sheet
def fetch_df():
    rows = ws.get_all_values()
    if len(rows) <= 1:
        return pd.DataFrame(columns=["timestamp", "mood", "note"])
    header = rows[0]
    data = rows[1:]
    clean = [r for r in data if r and r[0].strip()]
    df = pd.DataFrame(clean, columns=header)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["date"] = df["timestamp"].dt.date
    return df

# app header
st.title("🧪 Ops Queue Mood Tracker")
st.markdown("Capture your real-time mood logs in Google Sheets and visualize trends.")

# mood entry section
st.header("Log Your Mood")
mood = st.radio(
    "Current vibe:",
    ["😊", "😠", "😕", "🎉"],
    horizontal=True
)
note = st.text_input("Note (optional)", placeholder="e.g. half-day outage")
if st.button("Add Entry"):
    timestamp = datetime.datetime.now().isoformat()
    ws.append_row([timestamp, mood, note])
    st.success("Added!")

# display and filter data
st.header("View and Filter Logs")
df = fetch_df()
if df.empty:
    st.info("No entries yet—add a mood above!")
else:
    today = pd.Timestamp.now().date()
    start = st.date_input("Start date", today - pd.Timedelta(days=7))
    end = st.date_input("End date", today)
    subset = df[(df["date"] >= start) & (df["date"] <= end)]

    # grouping choice
    group_by = st.selectbox("Group by", ["Date", "Hour of Day"])
    if group_by == "Hour of Day":
        subset["hour"] = subset["timestamp"].dt.hour
        index = "hour"
    else:
        index = "date"

    pivot = (
        subset
        .groupby([index, "mood"]).size()
        .unstack(fill_value=0)
        .reindex(columns=["😊", "😠", "😕", "🎉"], fill_value=0)
    )
    st.write(pivot)
    st.bar_chart(pivot)

# today's summary
st.header("Today's Mood Breakdown")
df_all = fetch_df()
if df_all.empty:
    st.info("No entries to summarize.")
else:
    today_df = df_all[df_all["date"] == pd.Timestamp.now().date()]
    counts = (
        today_df["mood"].value_counts()
        .reindex(["😊", "😠", "😕", "🎉"], fill_value=0)
    )
    st.bar_chart(counts)