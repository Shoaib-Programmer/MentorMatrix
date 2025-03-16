import cv2
import pytesseract


def extract_key_frames(video_path, interval=5):
    """
    Extracts frames from a video at specified intervals.

    Parameters:
        video_path (str): Path to the video file.
        interval (int): Interval in seconds between each extracted frame.

    Returns:
        list of np.array: List of frames (as images) extracted from the video.

    The function uses OpenCV to capture frames from the video at regular intervals.
    It calculates the interval in frames based on the video's FPS, and appends each
    extracted frame to a list. This is useful for processing or analyzing key moments
    in a video.
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_interval = interval * fps

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            frames.append(frame)
        frame_count += 1

    cap.release()
    return frames


def extract_text_from_image(image):
    """
    Extracts text from an image using OCR (Optical Character Recognition).

    Parameters:
        image (np.array): The image to process for text extraction.

    Returns:
        str: Text detected in the image.

    This function uses Tesseract OCR to detect and extract text from an image.
    It first converts the image to grayscale, then applies OCR to extract any
    text present in the image. It returns the detected text as a string.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()


def analyze_frames(frames):
    """
    Analyzes a list of frames to detect and summarize text content.

    Parameters:
        frames (list of np.array): List of frames to analyze.

    Returns:
        str: A summary of the detected text from each frame.

    This function loops through each frame in the list, applies OCR to extract any text
    content, and creates a summary with frame-specific information. If text is detected
    in a frame, it adds the extracted text to the summary; otherwise, it notes that no
    text was detected in the frame.
    """
    summary = ""
    for i, frame in enumerate(frames):
        text = extract_text_from_image(frame)
        summary += f"\n--- Frame {i + 1} ---\n"
        if text:
            summary += f"Detected Text: {text}\n"
        else:
            summary += "No text detected.\n"
    return summary


def transcribe_video_without_audio(video_path, frame_interval=5):
    """
    Transcribes a video by analyzing visual frames when audio is unsuitable.

    Parameters:
        video_path (str): Path to the video file.
        frame_interval (int): Interval in seconds to sample frames for analysis.

    Returns:
        str: A visual "transcription" or summary of the video content based on text
             detected in the sampled frames.

    This function serves as a fallback for videos with unusable audio. It extracts frames
    at the specified intervals, analyzes each frame to detect text, and returns a summary
    of the visual content. It combines the `extract_key_frames` and `analyze_frames`
    functions to generate a visual transcription.
    """
    frames = extract_key_frames(video_path, interval=frame_interval)
    visual_summary = analyze_frames(frames)
    return visual_summary
