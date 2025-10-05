import streamlit as st
from pathlib import Path
import pandas as pd
from typing import Optional

# Difficulty configuration
DEFAULT_DIFFICULTY = "medium"  # medium -> Iowa, hard -> Texas
_DIFFICULTY_MAP = {
    "medium": "Iowa_Interpolated_Data.csv",
    "hard": "Texas_Interpolated_Data.csv",
}

def set_difficulty(level: str) -> None:
    """Persist the chosen difficulty in session state.
    Falls back to DEFAULT_DIFFICULTY if invalid.
    """
    level = (level or "").lower().strip()
    if level not in _DIFFICULTY_MAP:
        level = DEFAULT_DIFFICULTY
    st.session_state["difficulty"] = level


def get_difficulty() -> str:
    """Return current difficulty (session or default)."""
    return st.session_state.get("difficulty", DEFAULT_DIFFICULTY)


def get_dataset_filename() -> str:
    """Return the CSV filename mapped to current difficulty."""
    return _DIFFICULTY_MAP.get(get_difficulty(), _DIFFICULTY_MAP[DEFAULT_DIFFICULTY])


@st.cache_data(show_spinner=False)
def _load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def load_interpolated_dataframe(base_dir: str = "data/interpolated") -> Optional[pd.DataFrame]:
    """Load the interpolated dataset for the active difficulty.

    Returns an empty DataFrame if file not found (instead of raising), so UI can handle gracefully.
    """
    filename = get_dataset_filename()
    path = Path(base_dir) / filename
    if not path.exists():
        return pd.DataFrame()
    try:
        return _load_csv(str(path))
    except Exception:
        return pd.DataFrame()


def debug_difficulty_info() -> str:
    """Utility string for quick debugging / display."""
    return f"Difficulty: {get_difficulty()} -> file: {get_dataset_filename()}"
