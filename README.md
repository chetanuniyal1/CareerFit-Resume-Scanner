# CareerFit-Resume-Scanner
An applicant facing resume scanner made using python.
# CareerFit | Applicant ATS Scanner 💼

**CareerFit** is an AI-powered, applicant-centric resume and job matching system. Instead of acting as a corporate filter, it empowers job seekers to test their master resume against multiple job descriptions simultaneously—identifying their highest-probability matches, highlighting skill overlaps, and pinpointing exact keyword gaps before applying.

---

## ✨ Key Features

* **Applicant-First Batch Matching:** Upload one master resume (PDF) and evaluate it against multiple job description PDFs at once.
* **Semantic AI Similarity:** Goes beyond basic exact-word counting by using dense vector embeddings to understand context (e.g., matching *"backend development"* with *"server-side engineering"*).
* **Actionable Resume Gap Analysis:** Uses Natural Language Processing (NLP) to extract key noun chunks and entities from job descriptions that are missing from your resume.
* **Interactive Skill Radar Charts:** Dynamically plots your extracted skills against job requirements for immediate visual feedback.
* **Ranked Match Leaderboard:** Displays an interactive, sortable leaderboard with inline progress bars ranking your best-fit roles.
* **100% Local & Private:** All document parsing and embedding calculations run locally on your machine; your resume data is never uploaded to external APIs.

---

## 🛠️ Tech Stack

* **Frontend & UI:** [Streamlit](https://streamlit.io/) (with custom CSS & column configurations)
* **Semantic AI & Embeddings:** [Sentence-Transformers](https://sbert.net/) (`all-MiniLM-L6-v2` model) & PyTorch
* **NLP & Keyword Extraction:** [spaCy](https://spacy.io/) (`en_core_web_sm` pipeline) & Regular Expressions
* **PDF Parsing:** [pdfplumber](https://github.com/jsvine/pdfplumber) (layout-aware text extraction)
* **Data Handling & Visualization:** [Pandas](https://pandas.pydata.org/) & [Plotly](https://plotly.com/)

---

## 📂 Project Structure

```text
CareerFit-ATS-Scanner/
├── app.py               # Main Streamlit dashboard, UI layout, and Plotly radar charts
├── matcher.py           # Semantic similarity engine using Sentence-Transformers
├── ats.py               # spaCy-based noun-chunk and entity extraction for gap analysis
├── skills.py            # Regex-based technical and soft skill extractor
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
