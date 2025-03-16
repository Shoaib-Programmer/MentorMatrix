from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
from icecream import ic

# Load the pre-trained sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


def clean_text(text):
    """
    Cleans the text by lowercasing and removing extra spaces and punctuation.
    """
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^\w\s]", "", text)  # Remove punctuation
    return text.strip()


def evaluate_answer(user_answer, correct_answer, threshold=0.65):
    """
    Evaluates if the user's answer is correct by comparing it to the correct answer
    using cosine similarity of their embeddings.

    Args:
    - user_answer (str): The answer provided by the user.
    - correct_answer (str): The correct answer.
    - threshold (float): The similarity threshold to consider the answer correct.

    Returns:
    - bool: True if the answer is correct (similarity > threshold), False otherwise.
    """
    # Clean both the user answer and correct answer
    user_answer = clean_text(user_answer)
    correct_answer = clean_text(correct_answer)

    # Generate embeddings for both answers
    embeddings = model.encode([user_answer, correct_answer])

    # Calculate cosine similarity between the embeddings
    similarity_score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    ic(f"Similarity Score: {similarity_score}")

    # If the similarity score is above the threshold, consider the answer correct
    return similarity_score >= threshold


if __name__ == "__main__":
    # Example sentence and correct answer
    question = "Who built the Great Wall of China?"
    correct_answer = "Emperor Qin Shi Huang"

    # Test with user input
    user_input = "Qin Shi Huang built the Great Wall of China."

    # Evaluate the user's response
    is_correct = evaluate_answer(user_input, correct_answer)
    print("Is the user's answer correct?", is_correct)
