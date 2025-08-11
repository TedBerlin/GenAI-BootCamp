import streamlit as st
from t5_pipeline.summarizer_core_t5 import Summarizer
from shared.pdf_extract import extract_text_from_pdf

st.title("📄 Single PDF Summarizer (v2)")

uploaded_files = st.file_uploader("Upload PDF file(s)", type="pdf", accept_multiple_files=True)

guidance = st.text_area(
    "Optional Prompt (e.g., 'Focus on AI architecture and give me a 100 word abstract')",
    height=80
)

if uploaded_files and st.button("Summarize"):
    with st.spinner("Extracting and summarizing document(s)..."):
        texts = []
        for uploaded_file in uploaded_files:
            text = extract_text_from_pdf(uploaded_file)
            if text.strip():
                texts.append(text)

        if not texts:
            st.error("No extractable text found in the uploaded PDF(s).")
        else:
            summarizer = Summarizer(model_name="t5-small")
            summary = summarizer.summarize_multiple_texts(texts, guidance=guidance.strip() if guidance else None)

            if summary.strip():
                st.subheader("Summary")
                st.write(summary)
            else:
                st.warning("Summary was empty or no meaningful content found.")

    # Optional: show raw extracted texts for debugging
    with st.expander("Show extracted raw text"):
        for i, t in enumerate(texts):
            st.markdown(f"**Document {i+1}:**")
            st.write(t)
