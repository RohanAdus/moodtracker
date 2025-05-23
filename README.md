# Ops Queue Mood Tracker

A Streamlit application that logs timestamped mood entries to Google Sheets and displays interactive charts.

## Features

* Record mood entries (😊, 😠, 😕, 🎉) with optional notes
* Filter logs by date range
* Pivot table and bar chart visualizations by date or hour
* Summary chart showing today's mood distribution

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<YOUR_USERNAME>/mood-tracker.git
   cd mood-tracker
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Google Sheets**

   * In Google Cloud, create a service account and download the JSON key as `service-account.json`.
   * Share your target Google Sheet with the service account’s email address.
   * In `app.py`, replace the `SHEET_ID` string with your sheet’s ID.

4. **Run the app**

   ```bash
   streamlit run app.py
   ```

