
# 💎 Anti-Clickbait Tutorial Finder

**Mission:** finding high-quality educational content by prioritizing engagement over raw view counts.

##  Project Overview

This project implements an end-to-end Data Engineering pipeline to identify "Hidden Gems" on YouTube—tutorials with high engagement but potentially lower view counts—filtering out clickbait.

### 1) Architecture

*   **Extraction**: `etl/extract.py` - Fetches data from YouTube Data API v3.
*   **Transformation**: `etl/transform.py` - Calculates `engagement_score`, parses durations, and classifies videos (Hidden Gem vs Overhyped).
*   **Loading**: `etl/load.py` - Persists data into a local SQLite database (`tutorials.db`) with idempotency checks.
*   **Visualization**: `dashboard.py` - Streamlit-based interactive dashboard.

### 2) Tech Stack

*   **Python 3.10+**
*   **YouTube Data API v3** (Google)
*   **Pandas** (Data Manipulation)
*   **SQLite** (Storage)
*   **Streamlit** (UI/Dashboard)

##  3) How to Run

1.  **Install Dependencies**:
    *   **google-api-python-client**
    *   **pandas**
    *   **streamlit**
    *   **isodate**

2.  **Run the Dashboard**:
    ```bash
    streamlit run dashboard.py
    ```

3.  **Using the App**:
    *   **Open** the link provided (usually `http://localhost:8501`).
    *   **Enter API Key**: To search real topics, input your YouTube Data API Key in the sidebar.
    *   **Demo Mode**: If you don't have a key handy, click **"Load Demo Data 🧪"** to see the pipeline in action with synthetic data.

##  4) Validation & Testing

*   **Demo Mode** validates the full `Extract -> Transform -> Load -> Visualize` flow.
*   **Duplicate Prevention**: The loading module checks for existing Video IDs to ensure idempotency.
*   **Visual Proof**: The dashboard features a Scatter Plot (Views vs Engagement) to visually separate popular content from high-quality gems.

##  5) Logic

*   **Engagement Score**: `(Likes + 2 * Comments) / Views`
*   **Hidden Gem**: Engagement > 3% AND Views < 100k
*   **Overhyped**: Engagement < 1% AND Views > 500k

