import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Spotify Music Analytics Dashboard",
    page_icon="🎵",
    layout="wide"
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("spotify_data clean.csv")

df = load_data()

# -------------------------------
# Sidebar UI
# -------------------------------
st.sidebar.title("🎧 Spotify Filters")

artist = st.sidebar.multiselect(
    "Select Artist",
    options=df["artist_name"].unique()
)

album_type = st.sidebar.multiselect(
    "Album Type",
    options=df["album_type"].unique()
)

explicit_filter = st.sidebar.selectbox(
    "Explicit Content",
    options=["All", True, False]
)

# -------------------------------
# Apply Filters
# -------------------------------
filtered_df = df.copy()

if artist:
    filtered_df = filtered_df[filtered_df["artist_name"].isin(artist)]

if album_type:
    filtered_df = filtered_df[filtered_df["album_type"].isin(album_type)]

if explicit_filter != "All":
    filtered_df = filtered_df[filtered_df["explicit"] == explicit_filter]

# -------------------------------
# Header Section
# -------------------------------
st.title("🎵 Spotify Music Data Analysis & Popularity Dashboard")
st.markdown(
    """
    Analyze **Spotify tracks**, explore **artist popularity**,  
    and gain insights into **music trends** using interactive visuals.
    """
)

# -------------------------------
# KPI Metrics
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Tracks", len(filtered_df))
col2.metric("Avg Track Popularity", round(filtered_df["track_popularity"].mean(), 2))
col3.metric("Avg Artist Popularity", round(filtered_df["artist_popularity"].mean(), 2))
col4.metric("Avg Duration (min)", round(filtered_df["track_duration_min"].mean(), 2))

# -------------------------------
# Popularity Distribution
# -------------------------------
st.subheader("Track Popularity Distribution")

fig_pop = px.histogram(
    filtered_df,
    x="track_popularity",
    nbins=30,
    color_discrete_sequence=["#1DB954"]
)
st.plotly_chart(fig_pop, use_container_width=True)

# -------------------------------
# Top Artists
# -------------------------------
st.subheader("🌟 Top Artists by Popularity")

top_artists = (
    filtered_df.groupby("artist_name")["artist_popularity"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_artist = px.bar(
    top_artists,
    x="artist_popularity",
    y="artist_name",
    orientation="h",
    color="artist_popularity",
    color_continuous_scale="greens"
)
st.plotly_chart(fig_artist, use_container_width=True)

# -------------------------------
# Album Type Analysis
# -------------------------------
st.subheader("💿 Album Type vs Popularity")

fig_album = px.box(
    filtered_df,
    x="album_type",
    y="track_popularity",
    color="album_type"
)
st.plotly_chart(fig_album, use_container_width=True)

# -------------------------------
# Duration vs Popularity
# -------------------------------
st.subheader("⏱ Track Duration vs Popularity")

fig_duration = px.scatter(
    filtered_df,
    x="track_duration_min",
    y="track_popularity",
    size="artist_popularity",
    color="album_type",
    hover_name="track_name"
)
st.plotly_chart(fig_duration, use_container_width=True)

# -------------------------------
# Data Preview
# -------------------------------
st.subheader("Dataset Preview")
st.dataframe(filtered_df.head(20), use_container_width=True)

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown(
    "🎶 **Spotify Music Data Analysis Project** | Built with Streamlit"
)

