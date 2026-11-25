
import pandas as pd


def recommend_songs(
    songs,
    preferred_genre,
    current_weather,
    time_of_day,
    activity,
    top_n=5
):
    """Generate baseline and context-aware recommendations."""

    df = songs.copy()

    # Normalize text columns
    text_columns = [
        "genre", "mood", "weather_theme", "time_theme"
    ]

    for column in text_columns:
        df[column] = df[column].fillna("").astype(str).str.lower()

    preferred_genre = preferred_genre.lower()
    current_weather = current_weather.lower()
    time_of_day = time_of_day.lower()
    activity = activity.lower()

    # Activity-based mood preferences
    activity_moods = {
        "workout": ["energetic", "party"],
        "study": ["calm", "neutral"],
        "travel": ["happy", "energetic"],
        "relaxing": ["calm", "romantic"]
    }

    preferred_moods = activity_moods.get(activity, [])

    # Baseline recommendation score
    df["baseline_score"] = 0

    df.loc[
        df["genre"] == preferred_genre,
        "baseline_score"
    ] += 3

    df.loc[
        df["mood"].isin(preferred_moods),
        "baseline_score"
    ] += 2

    # Context-aware recommendation score
    df["context_score"] = df["baseline_score"]

    df.loc[
        df["weather_theme"] == current_weather,
        "context_score"
    ] += 2

    df.loc[
        df["time_theme"] == time_of_day,
        "context_score"
    ] += 2

    # Generate recommendations
    baseline = df.sort_values(
        "baseline_score", ascending=False
    ).head(top_n)

    context_aware = df.sort_values(
        "context_score", ascending=False
    ).head(top_n)

    return baseline, context_aware

