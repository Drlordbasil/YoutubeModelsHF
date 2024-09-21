import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Retrieve the API key from environment variables
api_key = os.environ.get('GOOGLE_API_KEY')

if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set")

# Create YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

def upload_video(file_path, title, description, tags, category_id='22', privacy_status='private'):
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status,
            'selfDeclaredMadeForKids': False
        }
    }

    media = MediaFileUpload(file_path, resumable=True)
    
    try:
        response = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        ).execute()
        print(f"Video uploaded successfully. Video ID: {response['id']}")
        return response['id']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def add_to_playlist(video_id, playlist_id):
    try:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        ).execute()
        print(f"Video added to playlist: {playlist_id}")
    except Exception as e:
        print(f"An error occurred while adding to playlist: {e}")

# Remove the direct function call here