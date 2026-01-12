
import isodate
import pandas as pd

def parse_duration(duration_str):
    try:
        duration = isodate.parse_duration(duration_str)
        return duration.total_seconds() / 60
    except:
        return 0

def calculate_quality_metrics(video_data, query):
    processed_data = []
    
    for video in video_data:
        stats = video.get('statistics', {})
        snippet = video.get('snippet', {})
        content_details = video.get('contentDetails', {})
        
        view_count = int(stats.get('viewCount', 0))
        like_count = int(stats.get('likeCount', 0))
        comment_count = int(stats.get('commentCount', 0))
        
        if view_count == 0:
            continue

        duration_mins = parse_duration(content_details.get('duration', 'PT0M'))
        
        # Metric Engineering
        # Engagement Score = (Likes + 2*Comments) / Views
        engagement_raw = (like_count + (comment_count * 2))
        engagement_ratio = (engagement_raw / view_count) if view_count > 0 else 0
        
        # Classification Logic
        video_type = "Standard"
        
        # Heuristic Thresholds
        # Hidden Gem: Low-Medium Views, High Engagement
        if view_count < 100000 and engagement_ratio > 0.03: 
             video_type = "Hidden Gem"
        # Overhyped: High Views, Low Engagement
        elif view_count > 500000 and engagement_ratio < 0.01:
             video_type = "Potentially Overhyped"
             
        processed_data.append({
            'video_id': video['id'],
            'title': snippet.get('title'),
            'channel_title': snippet.get('channelTitle'),
            'published_at': snippet.get('publishedAt'),
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'duration_minutes': round(duration_mins, 2),
            'engagement_score': round(engagement_ratio, 5),
            'video_type': video_type,
            'search_query': query
        })
        
    return pd.DataFrame(processed_data)
