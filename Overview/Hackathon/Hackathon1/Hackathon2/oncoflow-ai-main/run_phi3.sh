#!/bin/bash

VENV_DIR=".venv_summarier"
REQ_FILE="requirements.txt"
EVAL_SCRIPT="phi3_ollama/evaluate_phi3.py"
STREAMLIT_SCRIPT="phi3_ollama/summarizer_streamlit_phi3.py"

# Step 1: Create venv if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo "🔧 Creating virtual environment in $VENV_DIR"
    python3 -m venv "$VENV_DIR"
fi

# Step 2: Activate venv
source "$VENV_DIR/bin/activate"

# Step 3: Install requirements if needed
if [ -f "$REQ_FILE" ]; then
    echo "📦 Installing dependencies from $REQ_FILE"
    pip install --upgrade pip
    pip install -r "$REQ_FILE"
else
    echo "❌ Requirements file $REQ_FILE not found."
    exit 1
fi

# Step 4: Run evaluation script
if [ -f "$EVAL_SCRIPT" ]; then
    echo "🧪 Running evaluation..."
    python "$EVAL_SCRIPT"
else
    echo "⚠️ Evaluation script $EVAL_SCRIPT not found."
fi

# Step 5: Run Streamlit app
if [ -f "$STREAMLIT_SCRIPT" ]; then
    echo "🚀 Launching Streamlit app..."
    streamlit run "$STREAMLIT_SCRIPT"
else
    echo "⚠️ Streamlit script $STREAMLIT_SCRIPT not found."
fi
