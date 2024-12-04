from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import numpy as np
from typing import List

def generate_flashcards(text: List[str], num_clusters: int, model_name: str = 'all-MiniLM-L6-v2') -> List[List[str]]:
    """
    Generates flashcards by clustering sentences into groups based on semantic similarity
    and frequency-based importance using Sentence Transformers and TF-IDF.

    Args:
        text (List[str]): A list of sentences to process.
        num_clusters (int): Number of clusters to divide sentences into.
        model_name (str): Pre-trained Sentence Transformer model to use.

    Returns:
        List[List[str]]: A list of clusters, where each cluster is a list of sentences.
    """
    # Load the pre-trained Sentence Transformer model
    model = SentenceTransformer(model_name)
    
    # Encode sentences into embeddings using Sentence Transformer
    embeddings = model.encode(text)
    
    # Generate TF-IDF vectors
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(text)
    tfidf_features = tfidf_matrix.toarray()
    
    # Combine embeddings and TF-IDF features
    combined_features = np.hstack([normalize(embeddings), normalize(tfidf_features)])
    
    # Cluster similar sentences using KMeans
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(combined_features)
    clusters = kmeans.labels_
    
    # Create flashcards
    flashcards = []
    for cluster_id in range(num_clusters):
        cluster_sentences = [text[i] for i in range(len(text)) if clusters[i] == cluster_id]
        flashcards.append(cluster_sentences)
    
    return flashcards

if __name__ == "__main__":
    # Example usage
    sample_text = [
        "This is a sample text.",
        "We can use it to create flashcards.",
        "Sentence Transformers is a powerful tool for semantic search.",
        "TF-IDF captures word importance.",
        "Flashcards are helpful for studying concepts."
    ]
    num_clusters = 2
    flashcards = generate_flashcards(sample_text, num_clusters)

    print(flashcards)
    
    # Print flashcards for visualization
    for i, cluster in enumerate(flashcards):
        print(f"Flashcard Deck {i + 1}:")
        for sentence in cluster:
            print(f" - {sentence}")
