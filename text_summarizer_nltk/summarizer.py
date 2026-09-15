import heapq
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)


def is_valid_sentence(sentence):
    """Filter out headers, email addresses, phone numbers, and title fragments."""
    words = sentence.split()

    # Ignore lines with fewer than 5 words (headers like "CURRICULUM VITAE")
    if len(words) < 5:
        return False

    # Ignore contact details containing emails or phone numbers
    if re.search(
        r"@|http|www|\d{10}|\+?\d{1,3}[-.\s]?\d{10}", sentence, re.IGNORECASE
    ):
        return False

    return True


def clean_and_normalize_text(text):
    """Normalize line breaks and special characters into continuous paragraphs."""
    # Remove bullet symbols
    text = re.sub(r"[•\-\*]", " ", text)

    # Normalize multiple whitespace and newlines
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Join lines with proper punctuation boundaries
    formatted_text = ""
    for line in lines:
        if not line.endswith((".", "?", "!")):
            line += "."
        formatted_text += line + " "

    return re.sub(r"\s+", " ", formatted_text).strip()


def advanced_summarize(text, num_sentences=3):
    cleaned_input = clean_and_normalize_text(text)
    raw_sentences = sent_tokenize(cleaned_input)

    # Filter out headers and contact lines
    candidate_sentences = [
        s for s in raw_sentences if is_valid_sentence(s)
    ]

    # Fallback to raw sentences if filtering removes too much content
    if not candidate_sentences:
        candidate_sentences = raw_sentences

    if len(candidate_sentences) <= num_sentences:
        return " ".join(candidate_sentences)

    stop_words = list(stopwords.words("english"))
    vectorizer = TfidfVectorizer(stop_words=stop_words)

    try:
        tfidf_matrix = vectorizer.fit_transform(candidate_sentences)
    except ValueError:
        return " ".join(candidate_sentences[:num_sentences])

    # Score candidate sentences using TF-IDF and length normalization
    sentence_scores = {}
    for idx, sent in enumerate(candidate_sentences):
        score = tfidf_matrix[idx].sum()
        word_count = len(sent.split())
        sentence_scores[sent] = score / word_count

    # Extract N top-ranked sentences in chronological order
    summary_sentences = heapq.nlargest(
        num_sentences, sentence_scores, key=sentence_scores.get
    )
    summary_sentences.sort(key=lambda s: candidate_sentences.index(s))

    return " ".join(summary_sentences)