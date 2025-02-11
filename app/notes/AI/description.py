from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def generate_description(text, num_sentences=3):
    # Step 1: Initialize the SentenceTransformer model
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Step 2: Split the input text into sentences
    sentences = text.split('. ')
    
    # Step 3: Generate embeddings for each sentence
    sentence_embeddings = model.encode(sentences)
    
    # Step 4: Calculate cosine similarities between sentences
    similarity_matrix = cosine_similarity(sentence_embeddings)

    # Step 5: Rank sentences by their relevance to each other (similarity score)
    sentence_scores = np.sum(similarity_matrix, axis=1)

    # Step 6: Get the top N sentences (you can adjust num_sentences)
    top_sentence_indices = sentence_scores.argsort()[-num_sentences:][::-1]

    # Step 7: Combine the top sentences into a description
    description = ' '.join([sentences[i] for i in top_sentence_indices])

    return description
