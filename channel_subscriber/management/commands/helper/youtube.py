import httpx

BASE_URL = 'https://youtube.googleapis.com/youtube/v3/search'


# Function to send a YouTube API request
def send_youtube_request( api_key  , page_token = None ):
    # API parameters
    params = {
        'part': 'snippet' ,
        'order': 'videoCount' ,
        'q': 'python' ,  # Query
        'type': 'channel' ,
        'key': api_key ,  # Your API key
    }

    if page_token:
        # Add page token to fetch the next set of results
        params['pageToken'] = page_token

    # Headers for the request
    headers = {
        # 'Authorization': f'Bearer {access_token}' ,  # Your access token
        'Accept': 'application/json'
    }

    with httpx.Client() as client:
        response = client.get(BASE_URL , params = params , headers = headers)
        response.raise_for_status()

    return response.json()


# Function to extract channel information and page token
def extract_channel_data( youtube_response ):
    items = youtube_response.get('items' , [])
    next_page_token = youtube_response.get('nextPageToken' , None)

    channel_info_list = []

    # Loop through the response items to extract channel information
    for item in items:
        snippet = item.get('snippet' , {})
        channel_id = snippet.get('channelId' , None)
        title = snippet.get('title' , None)
        description = snippet.get("description", None)

        if channel_id and title:
            channel_info_list.append({
                'channelId': channel_id ,
                'title': title,
                'content': description
            })

    return channel_info_list , next_page_token