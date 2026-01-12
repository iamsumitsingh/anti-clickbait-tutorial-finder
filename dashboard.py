
import streamlit as st
import pandas as pd
from etl import extract, transform, load

# Set Page Config
st.set_page_config(page_title="Anti-Clickbait Tutorial Finder", page_icon="💎", layout="wide")

# Custom CSS for aesthetics
st.markdown("""
<style>
    .reportview-container {
        background: #0e1117;
    }
    .main {
        color: #fafafa;
    }
    h1 {
        font-family: 'Outfit', sans-serif;
        color: #ff4b4b;
    }
    h2, h3 {
        font-family: 'Outfit', sans-serif;
    }
    .metric-container {
        background-color: #262730;
        padding: 10px;
        border-radius: 5px;
    }
    div[data-testid="stExpander"] div[role="button"] p {
        font-size: 1.1rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.title("💎 Anti-Clickbait Tutorial Finder")
    st.markdown("### Find Quality, Not Hype.")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        user_api_key = st.text_input("YouTube Data API Key(optional)", type="password", help="Get one from Google Cloud Console")
        if user_api_key:
            api_key = user_api_key
        else:
            api_key = st.secrets["YOUTUBE_API_KEY"]
        st.info("Note: The API Key is required to fetch new data.")
        
        st.divider()
        st.markdown("### 🎯 Mission")
        st.markdown("""
        **Objective**: Filter out high-view, low-quality content.
        
        **Metrics**:
        - **Hidden Gem**: < 100k views, > 3% engagement
        - **Overhyped**: > 500k views, < 1% engagement
        """)
        
    # Main Input
    query = st.text_input("🔍 Enter a Technical Topic", placeholder="e.g., 'Python FastAPI', 'Rust vs Go'")
    
    col1, _ = st.columns([1, 4])
    
    # Search Action
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Run Pipeline 🚀", type="primary") and query:
            if not api_key:
                st.error("⚠️ Please enter a YouTube API Key in the sidebar.")
            else:
                with st.spinner(f"Running ETL Pipeline for '{query}'..."):
                    try:
                        # ETL Process
                        status = st.empty()
                        
                        status.info("1. EXTRACTING data from YouTube API...")
                        youtube = extract.get_youtube_service(api_key)
                        video_ids = extract.search_videos(youtube, query)
                        video_details = extract.get_video_details(youtube, video_ids)

                        status.info("2. TRANSFORMING data & calculating metrics...")
                        df = transform.calculate_quality_metrics(video_details, query)
                        
                        status.info("3. LOADING data into SQLite...")
                        load.save_to_db(df)
                        
                        status.success("✅ Pipeline Finished Successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Pipeline Failed: {e}")

    with col2:
        if st.button("Load Demo Data 🧪"):
             with st.spinner("Generating demo data..."):
                # create dummy data
                dummy_data = [
                    {'id': 'vid1', 'snippet': {'title': 'Hidden Gem Python', 'channelTitle': 'EduCoder', 'publishedAt': '2025-01-01'}, 'statistics': {'viewCount': 5000, 'likeCount': 500, 'commentCount': 50}, 'contentDetails': {'duration': 'PT10M'}},
                    {'id': 'vid2', 'snippet': {'title': 'Overhyped Clickbait', 'channelTitle': 'HypeMan', 'publishedAt': '2025-01-02'}, 'statistics': {'viewCount': 1000000, 'likeCount': 2000, 'commentCount': 100}, 'contentDetails': {'duration': 'PT5M'}},
                    {'id': 'vid3', 'snippet': {'title': 'Standard Tut', 'channelTitle': 'DailyCode', 'publishedAt': '2025-01-03'}, 'statistics': {'viewCount': 50000, 'likeCount': 1000, 'commentCount': 20}, 'contentDetails': {'duration': 'PT15M'}},
                ]
                df = transform.calculate_quality_metrics(dummy_data, "Demo Topic")
                load.save_to_db(df)
                st.success("Demo Data Loaded!")
                st.rerun()

    # Visualization Section
    st.divider()
    
    try:
        if query:
            df = load.load_data(query)
        else:
            df = load.load_data() 
            
        if not df.empty:
            # Filters
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                topic_filter = st.selectbox("Filter by Topic", ["All"] + list(df['search_query'].unique()))
            
            if topic_filter != "All":
                df = df[df['search_query'] == topic_filter]

            # KPIS
            kpi1, kpi2, kpi3, kpi4 = st.columns(4)
            kpi1.metric("📚 Total Tutorials", len(df))
            kpi2.metric("💎 Hidden Gems", len(df[df['video_type'] == 'Hidden Gem']))
            kpi3.metric("⚠️ Overhyped", len(df[df['video_type'] == 'Potentially Overhyped']))
            kpi4.metric("📊 Avg Engagement", f"{df['engagement_score'].mean():.2%}")
            
            # Charts
            tab1, tab2 = st.tabs(["📈 Engagement Analysis", "📋 Video Lists"])
            
            with tab1:
                st.subheader("Engagement vs. Popularity")
                st.markdown("Videos in the **top-left** (High Engagement, Low Views) are the *Hidden Gems*.")
                
                st.scatter_chart(
                    df,
                    x='view_count',
                    y='engagement_score',
                    color='video_type',
                    size='like_count',
                    use_container_width=True
                )
            
            with tab2:
                st.subheader("💎 Hidden Gems List")
                gems = df[df['video_type'] == 'Hidden Gem'].sort_values(by='engagement_score', ascending=False)
                
                if not gems.empty:
                    for _, row in gems.iterrows():
                        with st.expander(f"💎 {row['title']}"):
                            c1, c2 = st.columns([1, 3])
                            with c1:
                                st.write(f"**Channel**: {row['channel_title']}")
                                st.write(f"**Duration**: {row['duration_minutes']} min")
                            with c2:
                                st.write(f"**Views**: {row['view_count']:,}")
                                st.write(f"**Engagement**: {row['engagement_score']:.2%}")
                                st.markdown(f"[Watch Video](https://www.youtube.com/watch?v={row['video_id']})")
                else:
                    st.info("No Hidden Gems found yet. Try a different topic!")

                st.subheader("📺 All Videos (Sorted by Engagement)")
                st.dataframe(
                    df.sort_values(by='engagement_score', ascending=False)[
                        ['title', 'channel_title', 'view_count', 'engagement_score', 'video_type']
                    ],
                    use_container_width=True
                )
        else:
            st.info("👋 Welcome! Enter a topic above to start finding Hidden Gems.")
            
    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

if __name__ == "__main__":
    main()

