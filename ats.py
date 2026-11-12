import spacy
import os

# Load English tokenizer, tagger, parser and NER
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    doc = nlp(text)
    keywords = set()
    # Extract noun chunks and entities as keywords
    for chunk in doc.noun_chunks:
        keywords.add(chunk.text.lower().strip())
    for ent in doc.ents:
        keywords.add(ent.text.lower().strip())
    return keywords

def get_missing_keywords(resume_text, job_desc_text):
    resume_keywords = extract_keywords(resume_text)
    jd_keywords = extract_keywords(job_desc_text)
    
    # Find what's in JD but not in Resume
    missing = jd_keywords - resume_keywords
    # Filter out very short or generic keywords (cleaning)
    missing = {k for k in missing if len(k) > 3}
    
    # Return top 15 missing keywords to avoid overwhelming the user
    return list(missing)[:15]
