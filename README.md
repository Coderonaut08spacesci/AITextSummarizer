# AITextSummarizer
Hello! This is an NLP-based AI Text Summarizer Project developed by me.

⚡ SummarizeAI Pro (# v4.0)

Introducing version 4.0 of AI Text Summarizer; A modern, production-grade Natural Language Processing (NLP) web application built with Python.
**SummarizeAI Pro** utilizes an extractive **TF-IDF (Term Frequency-Inverse Document Frequency)** algorithm to generate concise, 
contextually relevant summaries from raw text or uploaded documents (`.txt` and `.pdf`), complete with multi-language translation support.

---

## 🌟 Key Features

* **Multi-Format Document Support:** Paste raw text directly or upload `.txt` and `.pdf` files.
* **TF-IDF Scoring Engine:** Upgraded from simple word counts to `scikit-learn`'s `TfidfVectorizer` to eliminate positional sentence bias and accurately weigh critical keywords.
* **Multi-Language Translation:** Built-in integration with `deep-translator` allowing summaries to be translated instantly into Spanish, French, German, Hindi, Marathi, and more.
* **Customizable Summary Length:** Interactive sidebar slider to fine-tune outputs from 1 to 10 sentences dynamically.
* **Modern SaaS UI & Custom CSS:** Styled interface featuring clean cards, responsiveness, and side-by-side metric visualizers.

---

## 🛠️ Tech Stack

* **Language:** Python 3.10+
* **NLP & ML:** `scikit-learn` (TF-IDF), `NLTK` (Tokenization, Stopwords)
* **Web UI Framework:** `Streamlit`
* **Translation & File Parsing:** `deep-translator`, `pypdf`

---

## 📂 Project Structure

```text
AITextSummarizer/
├── app.py              # Main Streamlit web UI and translation handler
├── summarizer.py       # Core TF-IDF summarization engine logic
├── requirements.txt    # Application dependencies
├── .gitignore          # Version control ignore file
└── README.md           # Documentation
## 🚀 Local Installation & Setup
Clone the repository:
git clone [https://github.com/YOUR_GITHUB_USERNAME/AITextSummarizer.git](https://github.com/YOUR_GITHUB_USERNAME/AITextSummarizer.git)
cd AITextSummarizer

Install dependencies:
pip install -r requirements.txt
Run the Streamlit app:
streamlit run app.py

⚙️ How the TF-IDF Algorithm Works
Unlike simple word-counting algorithms that often favor introductory "hook" sentences, SummarizeAI Pro scores sentences based on information density:Preprocessing: Removes citations ([1], [2]) and flattens excess whitespace via regular expressions.Tokenization: Splits text into sentences and individual words using NLTK tokenizers.TF-IDF Matrix Generation: Evaluates word importance across sentences. Unique, domain-specific keywords receive higher scores, while generic words are down-weighted.Length Normalization: Sentence scores are normalized against sentence length to prevent unusually long sentences from skewing results.Ordered Extraction: Extracts the top $N$ scoring sentences and restores their original chronological order for natural reading flow.
