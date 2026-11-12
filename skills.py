import re

# Extended list of common tech/professional skills for extraction
COMMON_SKILLS = [
    'python', 'java', 'c++', 'javascript', 'react', 'node.js', 'sql', 'nosql', 'mysql',
    'machine learning', 'deep learning', 'aws', 'azure', 'gcp', 'docker', 'cloud',
    'kubernetes', 'git', 'agile', 'scrum', 'html', 'css', 'django', 'flask', 'api',
    'spring boot', 'linux', 'nlp', 'data structures', 'algorithms', 'pandas', 'numpy',
    'scikit-learn', 'tensorflow', 'pytorch', 'excel', 'tableau', 'power bi', 'leadership',
    'project management', 'communication', 'problem solving', 'teamwork'
]

def extract_skills(text):
    text = text.lower()
    found_skills = set()
    for skill in COMMON_SKILLS:
        # Match exact word boundaries to avoid false positives
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found_skills.add(skill.title())
    return list(found_skills)
