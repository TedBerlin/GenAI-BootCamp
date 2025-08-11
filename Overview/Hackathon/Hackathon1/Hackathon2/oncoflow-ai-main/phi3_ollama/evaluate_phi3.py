import json
import math
from typing import List

import numpy as np
import pandas as pd
import torch
from rouge_score import rouge_scorer
import sacrebleu
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

from phi3_ollama.summarizer_core_phi3 import Retriever, Summarizer
from shared.utils import get_device

TOP_KS = [1, 3, 5, 10]

def precision_recall_at_k(retrieved: List[int], relevant: List[int], k: int):
    retrieved_k = retrieved[:k]
    rel = set(relevant)
    tp = sum(1 for r in retrieved_k if r in rel)
    precision = tp / k
    recall = tp / len(rel) if rel else 0.0
    return precision, recall

def compute_perplexity(text: str, model, tokenizer, device) -> float:
    if not text.strip():
        return float("nan")
    enc = tokenizer(text, return_tensors="pt")
    input_ids = enc["input_ids"].to(device)
    with torch.no_grad():
        out = model(input_ids, labels=input_ids)
        loss = out.loss.item()
    return math.exp(loss)

def main():
    with open("../data/test_set.json", "r") as f:
        test_set = json.load(f)

    device = get_device()

    summarizer = Summarizer()

    ppl_tok = GPT2TokenizerFast.from_pretrained("gpt2")
    ppl_model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)
    ppl_model.eval()

    rouge = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)

    search_rows = []
    sum_rows = []

    # optional: set a default guidance for all examples, or None
    default_guidance = None  # e.g. "Focus on AI architecture and give me a 100 word abstract"

    for ex_id, ex in enumerate(test_set):
        query = ex["query"]
        passages = ex["corpus_passages"]
        relevant_ids = ex["relevant_ids"]
        reference = ex["reference_summary"]

        # --- Search ---
        retriever = Retriever()
        retriever.build(passages)
        retrieved_idxs = retriever.search(query, top_k=max(TOP_KS))

        for k in TOP_KS:
            p, r = precision_recall_at_k(retrieved_idxs, relevant_ids, k)
            search_rows.append({"example_id": ex_id, "k": k, "precision": p, "recall": r})

        # --- Summarize top-k retrieved (largest k)
        top_passages = [passages[i] for i in retrieved_idxs[:max(TOP_KS)]]
        # Summarizer internally chunks, filters, restores entities, formats, etc.
        system_summary = summarizer.summarize_text(" ".join(top_passages), guidance=default_guidance)

        # BLEU
        bleu = sacrebleu.corpus_bleu([system_summary], [[reference]]).score

        # ROUGE
        r = rouge.score(reference, system_summary)
        rouge1 = r["rouge1"].fmeasure
        rouge2 = r["rouge2"].fmeasure
        rougeL = r["rougeL"].fmeasure

        # Perplexity
        ppl = compute_perplexity(system_summary, ppl_model, ppl_tok, device)

        sum_rows.append({
            "example_id": ex_id,
            "BLEU": bleu,
            "ROUGE-1(f)": rouge1,
            "ROUGE-2(f)": rouge2,
            "ROUGE-L(f)": rougeL,
            "Perplexity": ppl,
            "system_summary": system_summary,
            "reference_summary": reference
        })

    # Aggregate & print
    search_df = pd.DataFrame(search_rows)
    sum_df = pd.DataFrame(sum_rows)

    print("\n=== Search metrics per example ===")
    print(search_df.round(4).to_string(index=False))

    print("\n=== Mean Search metrics by k ===")
    print(search_df.groupby("k")[["precision", "recall"]].mean().round(4).to_string())

    print("\n=== Summarization metrics per example ===")
    print(sum_df.drop(columns=["system_summary", "reference_summary"]).round(4).to_string(index=False))

    print("\n=== Mean Summarization metrics ===")
    print(sum_df[["BLEU", "ROUGE-1(f)", "ROUGE-2(f)", "ROUGE-L(f)", "Perplexity"]].mean().round(4).to_string())

if __name__ == "__main__":
    main()
