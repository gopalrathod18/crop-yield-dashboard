from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Crop Yield Explorer", page_icon="🌱", layout="wide")

DATA_PATH = Path(__file__).parent / "Crop_Yield_Prediction.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    numeric = ["Nitrogen", "Phosphorus", "Potassium", "Temperature", "Humidity", "pH_Value", "Rainfall", "Yield"]
    for column in numeric:
        df[column] = pd.to_numeric(df[column], errors="coerce")
    df["Crop"] = df["Crop"].astype("string").str.strip()
    return df.dropna(subset=["Crop", "Yield"])


df = load_data()
st.title("🌱 Crop Yield Explorer")
st.caption("Explore crop yields alongside soil nutrients and weather conditions.")

with st.sidebar:
    st.header("Filters")
    all_crops = sorted(df["Crop"].dropna().unique().tolist())
    selected_crops = st.multiselect("Choose crops", all_crops, default=all_crops)
    yield_min, yield_max = float(df["Yield"].min()), float(df["Yield"].max())
    selected_yield = st.slider("Yield range", min_value=yield_min, max_value=yield_max,
                               value=(yield_min, yield_max), step=max((yield_max-yield_min)/1000, 1.0))

filtered = df[df["Crop"].isin(selected_crops) & df["Yield"].between(*selected_yield)]
if filtered.empty:
    st.info("No rows match these filters. Adjust the crop or yield range.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records", f"{len(filtered):,}")
c2.metric("Crops selected", f"{filtered['Crop'].nunique():,}")
c3.metric("Average yield", f"{filtered['Yield'].mean():,.1f}")
c4.metric("Median yield", f"{filtered['Yield'].median():,.1f}")

st.subheader("Average yield by crop")
by_crop = (filtered.groupby("Crop", as_index=False)["Yield"].mean()
           .sort_values("Yield", ascending=False))
fig = px.bar(by_crop, x="Crop", y="Yield", color="Yield", color_continuous_scale="Greens",
             labels={"Yield": "Average yield", "Crop": "Crop"})
fig.update_layout(coloraxis_showscale=False, xaxis_tickangle=-35, margin=dict(t=15, b=10))
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Rainfall and yield")
    scatter = px.scatter(filtered, x="Rainfall", y="Yield", color="Crop",
                         hover_data=["Nitrogen", "Phosphorus", "Potassium"],
                         labels={"Rainfall": "Rainfall", "Yield": "Yield"})
    st.plotly_chart(scatter, use_container_width=True)
with right:
    st.subheader("Yield distribution")
    hist = px.histogram(filtered, x="Yield", color="Crop", nbins=30,
                        labels={"Yield": "Yield", "count": "Records"})
    st.plotly_chart(hist, use_container_width=True)

st.subheader("Dataset preview")
st.dataframe(filtered.head(20), use_container_width=True, hide_index=True)
st.download_button("Download filtered data", filtered.to_csv(index=False).encode("utf-8"),
                   file_name="filtered_crop_yield.csv", mime="text/csv")

with st.expander("About this dataset"):
    st.write(f"The file contains **{len(df):,} rows** and **{df['Crop'].nunique()} crop types**.")
    if df["Yield"].max() > df["Yield"].quantile(0.99) * 3:
        st.warning(f"Yield includes an unusually high value ({df['Yield'].max():,.0f}). Check the source units or record before interpreting averages.")
    st.write("Charts and summary values use the selected filters. Yield units are not specified in the CSV.")
