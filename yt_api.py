import os
import json
from dotenv import load_dotenv
import googleapiclient.discovery

from utils import get_video_id

load_dotenv()

api_key = os.getenv('API_KEY')

# Create a YouTube Data API client
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)

def get_video_data(video_url, type):
    video_id = get_video_id(video_url)
    video_response = ''

    if type == 'description':
        # # Define parameters for the API request
        video_response = youtube.videos().list(
            part='snippet,contentDetails',
            id=video_id
        ).execute()
        return video_response
    
    if type == 'comments':
        # Call the API to retrieve comments for the specified video
        comments = []
        next_page_token = None

        while True:
            response = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=100,
                pageToken=next_page_token
            ).execute()

            # Process each comment in the response
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append(comment)

            # Check if there are more pages of comments
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

        return comments