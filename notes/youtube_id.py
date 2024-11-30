from urllib.parse import urlparse, parse_qs

def get_video_id_from_url(url):
    try:
        # Parse the URL using urlparse
        parsed_url = urlparse(url)

        # Check for a standard YouTube URL (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
        if parsed_url.hostname == 'www.youtube.com' or parsed_url.hostname == 'youtube.com':
            # Extract the video ID from the 'v' query parameter
            video_id = parse_qs(parsed_url.query).get('v', [None])[0]
            return video_id

        # Check for shortened YouTube URL (e.g., https://youtu.be/VIDEO_ID)
        elif parsed_url.hostname == 'youtu.be':
            # Extract video ID from the path (e.g., /VIDEO_ID)
            video_id = parsed_url.path.strip('/')
            return video_id

        # Return None if not a valid YouTube URL
        return None

    except Exception as e:
        print(f"Error extracting video ID: {e}")
        return None
