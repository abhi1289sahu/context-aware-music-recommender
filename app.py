
import streamlit as st
import pandas as pd

from src.recommender import recommend_songs

st.set_page_config(
    page_title="Music Recommendation System",
    page_icon="🎵",
    layout="wide"
)

st.title("🎵 Context-Aware Music Recommendation System")

st.write(
    "Discover music based on your preferences, "
    "weather, time and activity."
)

# Load song dataset
@st.cache_data
def load_songs():
    return pd.read_csv("data/synthetic/songs.csv")

songs = load_songs()

st.sidebar.header("Your Preferences")

genre = st.sidebar.selectbox(
    "Preferred Genre",
    sorted(songs["genre"].unique())
)

weather = st.sidebar.selectbox(
    "Current Weather",
    ["sunny", "rain", "cloudy", "winter", "summer"]
)

time = st.sidebar.selectbox(
    "Time of Day",
    ["morning", "afternoon", "evening", "night"]
)

activity = st.sidebar.selectbox(
    "Current Activity",
    ["study", "workout", "travel", "relaxing"]
)

if st.sidebar.button("Recommend Songs"):

    baseline, context = recommend_songs(
        songs,
        genre,
        weather,
        time,
        activity,
        top_n=5
    )

    st.subheader("Baseline Recommendations")
    st.caption("Based on genre and activity preferences.")

    st.dataframe(
        baseline[
            ["song_title", "artist", "genre",
             "mood", "baseline_score"]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Context-Aware Recommendations")
    st.caption("Includes weather and time context.")

    st.dataframe(
        context[
            ["song_title", "artist", "genre",
             "mood", "context_score"]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.success("Recommendations generated successfully!")

st.divider()

st.subheader("About This Project")

st.write(
    "This project compares a baseline music recommendation "
    "approach with a context-aware approach using song metadata "
    "and user-selected contextual information."
)

st.caption("Academic prototype | Python | Pandas | Streamlit")
