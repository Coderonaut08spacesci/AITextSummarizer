from deep_translator import GoogleTranslator
from pypdf import PdfReader
import streamlit as st
from nltk.tokenize import sent_tokenize
from summarizer import advanced_summarize

# --- Page Configuration ---
st.set_page_config(
    page_title="SummarizeAI Pro", page_icon="⚡", layout="wide"
)

# --- Custom CSS Styling ---
st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        border: none;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #4338CA;
        color: white;
        transform: translateY(-1px);
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- File Helper Functions ---
def read_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")


def read_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    extracted_text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            extracted_text += page_text + "\n"
    return extracted_text


# --- App Header ---
st.title("⚡ SummarizeAI Pro")
st.caption(
    "Advanced TF-IDF Extractive Engine with Multi-Format Uploads & Multi-Language Translation"
)

# --- Sidebar Configuration ---
st.sidebar.header("⚙️ Configuration")
sentence_count = st.sidebar.slider("Summary Length (Sentences)", 1, 10, 3)

target_lang = st.sidebar.selectbox(
    "Output Language",
    ["English", "Spanish", "French", "German", "Hindi", "Marathi"],
)

lang_codes = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Hindi": "hi",
    "Marathi": "mr",
}

# --- Input Selection Tabs ---
tab1, tab2 = st.tabs(["📋 Paste Text", "📁 Upload Document"])

input_text = ""

with tab1:
    pasted_text = st.text_area(
        "Source Text",
        height=220,
        placeholder="Paste long text or article here...",
    )
    if pasted_text:
        input_text = pasted_text

with tab2:
    uploaded_file = st.file_uploader(
        "Upload a document:", type=["txt", "pdf"]
    )
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            input_text = read_txt(uploaded_file)
        elif uploaded_file.type == "application/pdf":
            input_text = read_pdf(uploaded_file)

        if input_text.strip():
            st.success(
                f"Loaded '{uploaded_file.name}' successfully! ({len(input_text)} characters)"
            )
            with st.expander("Preview Document Content"):
                st.write(
                    input_text[:1000] + "..."
                    if len(input_text) > 1000
                    else input_text
                )

# --- Summarization Trigger ---
st.divider()

if st.button("Generate Smart Summary"):
    if not input_text.strip():
        st.warning("⚠️ Please paste text or upload a document first!")
    else:
        with st.spinner("Analyzing text using TF-IDF and translating..."):
            # 1. Generate Extractive Summary via TF-IDF
            raw_summary = advanced_summarize(
                input_text, num_sentences=sentence_count
            )

            # 2. Translate if non-English language selected
            if target_lang != "English":
                final_summary = GoogleTranslator(
                    source="auto", target=lang_codes[target_lang]
                ).translate(raw_summary)
            else:
                final_summary = raw_summary

        st.success("Summary Ready!")
        st.markdown(f"### 📌 Summary Result ({target_lang}):")
        st.info(final_summary)

        # --- Metrics Dashboard ---
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Original Sentences", len(sent_tokenize(input_text)))
        with col2:
            st.metric("Summary Sentences", len(sent_tokenize(raw_summary)))
