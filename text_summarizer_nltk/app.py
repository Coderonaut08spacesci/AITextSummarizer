import heapq
import re
import nltk
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
#---Streamlit Page Configuration---
st.set_page_config(
    page_title="AI Text Summarizer",page_icon="📝",layout="centered"
)
#---NLTK Resource Downloader (Cached so it runs only once)---
@st.cache_resource
def download_nltk_resources():
    nltk.download("punkt",quiet=True)
    nltk.download("stopwords",quiet=True)
    nltk.download("punkt_tab",quiet=True)

download_nltk_resources
#---Core Summarization Logic---
def summarize_text(text, num_sentences=3):
    #1. Clean text
    clean_text= re.sub(r'\[[0-9]*\]',' ',text)
    clean_text=re.sub(r'\s+',' ',clean_text)
    sentences=sent_tokenize(text)
    words=word_tokenize(clean_text.lower())

    if len(sentences)<=num_sentences:
       return text
    stop_words=set(stopwords.words('english'))
    word_frequencies={}
    for word in words:
        if word.isalnum() and word not in stopwords:
            word_frequencies[word]=word_frequencies.get(word,0)+1
    max_frequency=max(word_frequencies.values(),default=1)
    for word in word_frequencies.keys():
        word_frequencies[word]/=max_frequency

    #4. Score Sentences
    sentence_scores={}
    for sent in sentences:
        for word in word_tokenize(sent.lower()):
            if word in word_frequencies:
                if len(sent.split(" "))<30:
                    sentence_scores[sent]=(
                        sentence_scores.get(sent,0)+word_frequencies[word]
                    )
    #5. Extract Top N sentences
    summary_sentences=heapq.nlargest(
        num_sentences, sentence_scores, key=sentence_scores.get
    )
    summary_sentences.sort(key=lambda)