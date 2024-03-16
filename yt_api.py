import os
import json
from dotenv import load_dotenv
import googleapiclient.discovery
from yt_api_utils import extract_video_duration, extract_video_timestamps_from_comments, extract_video_timestamps_from_description

load_dotenv()

api_key = os.getenv('API_KEY')

# Create a YouTube Data API client
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
video_id='UMruSyngNaY'

def get_fake_video_length():
    # Opening JSON file
    f = open('contentDetails.json')
    # returns JSON object as a dictionary
    video_response_json = json.load(f)
    # Closing file
    f.close()

    return video_response_json

def get_fake_video_comments():
    # Opening JSON file
    f = open('snippet.json')
    # returns JSON object as a dictionary
    response_json = json.load(f)
    # Closing file
    f.close()

    comments_response = []

    for item in response_json['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments_response.append(comment)

    return comments_response

# def get_video_length(video_id):
#     # # Define parameters for the API request
#     video_response = youtube.videos().list(
#         part='snippet,contentDetails',
#         id=video_id
#     ).execute()

#     return video_response
    

def get_video_data(video_id, type):
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

    
# def get_video_comments():
#     # Call the API to retrieve comments for the specified video
#     comments = []
#     next_page_token = None

#     while True:
#         response = youtube.commentThreads().list(
#             part="snippet",
#             videoId=video_id,
#             maxResults=100,
#             pageToken=next_page_token
#         ).execute()

#         # Process each comment in the response
#         for item in response['items']:
#             comment = item['snippet']['topLevelComment']['snippet']
#             comments.append(comment)

#         # Check if there are more pages of comments
#         next_page_token = response.get('nextPageToken')
#         if not next_page_token:
#             break

#     return comments

# Extract duration from response:
# video_response = get_fake_video_length()
# video_length = extract_video_duration(video_response)

# # Extract timestamps from comments response:
# comments_response = get_fake_video_comments()
# video_timestamps = extract_video_timestamps_from_comments(comments_response, video_length)

# Extract timestamps from description response:
# description_response = get_video_length()
# description = description_response['items'][0]['snippet']['description']
# video_timestamps = extract_video_timestamps_from_description(description, video_length)