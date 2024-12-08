from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import numpy as np

def get_title(text: str) -> str:
    '''
    Generates a title for a given piece of context (text) using sentence embeddings
    and scikit-learn's TF-IDF for keyword extraction.
    
    Args:
        text (str): The context or body of the text for which a title is to be generated.
    
    Returns:
        str: A summary title generated for the input text.
    '''
    # Step 1: Use sentence-transformers to generate sentence embeddings for the input text
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
    sentences = text.split('. ')  # Split the text into sentences
    
    # Get embeddings for each sentence
    sentence_embeddings = model.encode(sentences)
    
    # Step 2: Use TF-IDF to extract the most important keywords
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', max_features=10)
    tfidf_matrix = tfidf_vectorizer.fit_transform(sentences)
    
    # Step 3: Apply KMeans clustering to find the most central terms (keywords)
    kmeans = KMeans(n_clusters=1, random_state=0)
    kmeans.fit(tfidf_matrix)
    
    # Get the cluster center (most relevant keywords)
    cluster_center = kmeans.cluster_centers_[0]
    feature_names = np.array(tfidf_vectorizer.get_feature_names_out())
    important_keywords = [feature_names[i] for i in cluster_center.argsort()[-5:]]  # Top 5 words
    
    # Step 4: Combine the embeddings and keywords to generate a title
    # We'll select a sentence that contains one of the important keywords
    selected_sentence = ''
    for sentence in sentences:
        if any(keyword in sentence for keyword in important_keywords):
            selected_sentence = sentence
            break
    
    # If no sentence is found with the important keywords, fall back to the longest sentence
    if not selected_sentence:
        selected_sentence = max(sentences, key=len)
    
    return selected_sentence.strip()


# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# import numpy as np

# def title(context: str) -> str:
#     """
#     Uses Sentence Transformers to generate embeddings for sentences in the context, 
#     then computes cosine similarity to rank sentences, returning the most relevant one as the title.
    
#     Args:
#     context (str): The input text from which the title is generated.
    
#     Returns:
#     str: The generated title.
#     """
#     # Initialize the SentenceTransformer model (use a pre-trained model like 'all-MiniLM-L6-v2')
#     model = SentenceTransformer('all-MiniLM-L6-v2')
    
#     # Split the context into sentences
#     sentences = context.split('.')
#     sentences = [s.strip() for s in sentences if s.strip()]
    
#     # Generate sentence embeddings
#     embeddings = model.encode(sentences)
    
#     # Compute cosine similarity between the embeddings of the sentences and the whole context
#     context_embedding = model.encode([context])[0]
    
#     # Calculate cosine similarities between context and each sentence
#     similarities = cosine_similarity([context_embedding], embeddings)
    
#     # Get the index of the sentence with the highest similarity
#     best_sentence_idx = np.argmax(similarities)
    
#     # Return the sentence with the highest similarity as the title
#     return sentences[best_sentence_idx]

