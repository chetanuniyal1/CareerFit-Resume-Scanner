from sentence_transformers import SentenceTransformer, util
import torch

# Load a lightweight model for semantic matching
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def calculate_similarity(resume_text, job_desc_text):
    if not model:
        return 0.0
    
    # Compute embeddings
    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(job_desc_text, convert_to_tensor=True)

    # Compute cosine similarity
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    
    # Convert to percentage
    return round(cosine_scores.item() * 100, 2)
