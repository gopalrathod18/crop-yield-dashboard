# Crop Yield Explorer

A simple interactive Python dashboard for exploring the supplied crop yield dataset. It includes crop and yield filters, summary metrics, crop comparison, rainfall scatter plot, yield distribution, a data preview, and filtered CSV download.

## Run it

1. Install Python 3.9 or newer.
2. Open Terminal in this folder.
3. Install the packages:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Start the dashboard:

   ```bash
   python3 -m streamlit run app.py
   ```

5. Open the local address Streamlit prints (usually http://localhost:8501).

The CSV is included beside `app.py`, so no separate path setup is needed.

## Dataset note

The file has 2,200 records across 22 crops, with columns for nutrients, temperature, humidity, pH, rainfall, crop, and yield. Yield units are not specified. One record has a yield of 120,000, far above the rest, so check the original source before interpreting averages.
