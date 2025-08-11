# 🏥 OncoFlow AI – Oncology Research Summarizer

> 💡 OncoFlow AI is a lightweight LLM-powered pipeline for extracting, summarizing, and analyzing clinical oncology studies from PDFs. Designed to run efficiently on local CPUs—even a Raspberry Pi.

![Demo](assets/demo.gif)  
<!-- Replace with your own Loom link or animated GIF -->

---

## 🔍 Key Features

- **🗂️ Multi-document Summarization**: Compare multiple clinical studies side-by-side. [See Example](#multi-doc)
- **⚠️ Error Detection**: Detects 5 types of dosage-related inconsistencies using hybrid rules + ML.
- **🧠 LLM Support**: Works with both `phi-3-mini` (via Ollama) and `t5-small` (via HuggingFace pipeline).
- **💻 CPU-Friendly**: Tested on Raspberry Pi 4 and other low-spec machines.

---

## 🛠️ Technical Stack

| Component         | Technology                    | Notes / Improvements            |
|------------------|-------------------------------|----------------------------------|
| Summarization     | `t5-small` / `phi-3-mini`     | phi3 version uses Ollama for local inference |
| Multi-doc Search  | `FAISS-CPU`, `sentence-transformers` | Handles 1000+ documents efficiently |
| Error Detection   | Rule-based + lightweight ML   | 5 alert classes: dosage, frequency, etc. |
| Text Parsing      | `pypdf`, `spaCy`              | Clean and normalize PDF content |
| UI                | `Streamlit`                   | One-click web UI for demo or prototyping |

---

## 🚀 Quick Start

### 0. Install Ollama application (only for phi3)
https://ollama.com/download

### 1. Run `.sh` setup script (Mac/Linux only)
./run_phi3.sh
# OR
./run_t5.sh


### OR

### 1. Clone the repository
git clone https://github.com/your-org/oncoflow-ai.git
cd oncoflow-ai

### 2. Set up a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

### 3. Install dependencies
# For phi-3-mini version (Ollama backend)
pip install -r requirements-phi3.txt
# OR for t5-small version (Transformers pipeline)
pip install -r requirements-t5.txt

### 4. Run from command line
# Single document mode
python phi3_ollama/pipeline_phi3.py --input=pdfs/my_study.pdf
# Multi-document mode
python phi3_ollama/pipeline_phi3.py --input=pdfs/ --multi

### 5. Launch Streamlit UI
# For phi-3-mini
streamlit run phi3_ollama/streamlit_phi3.py
# For t5-small
streamlit run t5_pipeline/streamlit_t5.py

---

### Project Structure

oncoflow-ai/
├── phi3_ollama/
│   ├── summarizer_core_phi3.py
│   ├── streamlit_phi3.py
│   └── evaluate_phi3.py
│
├── t5_pipeline/
│   ├── summarizer_core_t5.py
│   ├── streamlit_t5.py
│   └── evaluate_t5.py
│
├── shared/
│   ├── pdf_extract.py
│   ├── semantic_filter.py
│   └── utils.py
│
├── data/
│   └── test_set.json
│
├── requirements-phi3.txt
├── requirements-t5.txt
└── run_phi3.sh

---

### Example Prompt (Streamlit UI)

Focus on treatment strategies for triple-negative breast cancer. Provide a 100-word abstract comparing studies.

---

### Evaluation metrics
# t5-pipeline
=== Search metrics per example ===
 example_id  k  precision  recall
          0  1     0.0000     0.0
          0  3     0.3333     0.5
          0  5     0.4000     1.0
          0 10     0.2000     1.0

=== Mean Search metrics by k ===
    precision  recall
k
1      0.0000     0.0
3      0.3333     0.5
5      0.4000     1.0
10     0.2000     1.0

=== Summarization metrics per example ===
 example_id    BLEU  ROUGE-1(f)  ROUGE-2(f)  ROUGE-L(f)  Perplexity
          0 11.2133      0.4138      0.1481      0.2759    110.7362

=== Mean Summarization metrics ===
BLEU           11.2133
ROUGE-1(f)      0.4138
ROUGE-2(f)      0.1481
ROUGE-L(f)      0.2759
Perplexity    110.7362

## phi3-ollama
=== Search metrics per example ===
 example_id  k  precision  recall
          0  1     0.0000     0.0
          0  3     0.3333     0.5
          0  5     0.4000     1.0
          0 10     0.2000     1.0

=== Mean Search metrics by k ===
    precision  recall
k
1      0.0000     0.0
3      0.3333     0.5
5      0.4000     1.0
10     0.2000     1.0

=== Summarization metrics per example ===
 example_id   BLEU  ROUGE-1(f)  ROUGE-2(f)  ROUGE-L(f)  Perplexity
          0 0.5131      0.0615      0.0104      0.0615     54.6385

=== Mean Summarization metrics ===
BLEU           0.5131
ROUGE-1(f)     0.0615
ROUGE-2(f)     0.0104
ROUGE-L(f)     0.0615
Perplexity    54.6385


