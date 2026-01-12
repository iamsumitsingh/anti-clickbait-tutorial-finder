
from googleapiclient.discovery import build

def get_youtube_service(api_key):
    return build('youtube', 'v3', developerKey=api_key)

def search_videos(youtube, query, max_results=50):
    request = youtube.search().list(
        q=query,
        part="id,snippet",
        type="video",
        maxResults=max_results,
        relevanceLanguage="en"
    )
    response = request.execute()
    
    video_ids = []
    for item in response.get('items', []):
        video_ids.append(item['id']['videoId'])
    
    return video_ids

def get_video_details(youtube, video_ids):
    if not video_ids:
        return []
    
    all_videos = []
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(batch_ids)
        )
        response = request.execute()
        all_videos.extend(response.get('items', []))
        
    return all_videos
