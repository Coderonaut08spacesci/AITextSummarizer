import heapq
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

def advanced_summarize(text, num_sentences=3):
    clean_text = re.sub(r'\[[0-9]*\]', ' ', text)
    clean_text = re.sub(r'\s+', ' ', clean_text)

    sentences = sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text
      
    # Use TF-IDF Vectorizer to score word importance automatically
    stop_words = list(stopwords.words('english'))
    vectorizer = TfidfVectorizer(stop_words=stop_words)

    try:
        tfidf_matrix = vectorizer.fit_transform(sentences)
    except ValueError:
        # Fallback if text contains only stopwords
        return ' '.join(sentences[:num_sentences])
    # Calculate sentence scores from TF-IDF matrix
    sentence_scores = {}
    for idx, sent in enumerate(sentences):
        # Sum TF-IDF scores of all words in the sentence
        score = tfidf_matrix[idx].sum()

        # Length Normalization: Avoid favoring unusually long sentences
        word_count = len(sent.split())
        if word_count > 5 and word_count < 40:
            sentence_scores[sent] = score / word_count
    
    # Extract Top N Sentences
    summary_sentences = heapq.nlargest(
        num_sentences, sentence_scores, key=sentence_scores.get
    )
    summary_sentences.sort(key=lambda s: sentences.index(s))

    return ' '.join(summary_sentences)
