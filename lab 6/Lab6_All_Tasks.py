"""
Lab 6: NLP Fundamentals — Tokenization, Embeddings and Text Chunking
Combined single-file submission.

Run:
    pip install numpy scikit-learn
    python Lab6_All_Tasks.py

Optional embedding comparison:
    pip install sentence-transformers
    python Lab6_All_Tasks.py

The corpus and query set are included in this file so that this script can
run without separate JSON files. The documents are synthetic teaching data.
"""

import re
import csv
import time
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


# ---------------------------------------------------------------------
# DATA: synthetic documents and labeled questions
# ---------------------------------------------------------------------

CORPUS = {
    "late": (
        "Late submission is normally penalized in this synthetic assessment guide. "
        "A student who cannot submit on time should contact the course coordinator "
        "as early as possible. Illness extensions require medical evidence before "
        "the deadline. The evidence should identify the relevant period and should "
        "be sent through the official learning portal. A request is reviewed by "
        "the coordinator; an extension is not automatic. Students should keep a "
        "copy of the request and any response. The normal submission method is the "
        "learning portal, and the final assignment should be uploaded as a PDF. "
        "This example is teaching data only and is not an actual university rule."
    ),
    "password": (
        "A forgotten account password can be reset using the recovery link on the "
        "sign-in page. The user should enter the email address registered with the "
        "account and follow the instructions sent to that address. Recovery codes "
        "are private and should never be shared with another person. If the recovery "
        "email does not arrive, check the spam folder and confirm that the registered "
        "address was typed correctly. If access is still unavailable, contact the "
        "help desk through the official support channel. Staff should not ask a user "
        "to disclose their password. This synthetic guide describes a general "
        "demonstration process, not a live service."
    ),
    "assignment": (
        "Assignments in this synthetic learning portal are submitted through the "
        "assignment upload page. Students should select the correct course, open "
        "the relevant assignment, and attach the final file. The final file should "
        "be saved in PDF format unless the task instructions specify another format. "
        "Before submitting, check that the file opens and that the correct version "
        "is attached. After upload, review the confirmation shown by the portal and "
        "keep a copy for personal records. If the upload page is unavailable, contact "
        "the course support team and explain the issue. This is demonstration content "
        "and does not describe a real institution's current system."
    ),
    "contractor": (
        "In this synthetic workplace guide, contractors may work remotely only if "
        "the signed contract explicitly permits remote work. A general statement "
        "about employee flexibility does not change the contractor condition. "
        "Employees may request remote work with manager approval, but employee "
        "rules do not automatically apply to contractors. The relevant contract "
        "version should be checked before a decision is made. If the wording is "
        "unclear, the contract owner should be asked for clarification. A retrieval "
        "result is only a passage to inspect and should not be treated as a legal "
        "or employment decision. This document is fictional teaching material."
    ),
    "printer": (
        "For blank printer pages in this synthetic troubleshooting guide, first "
        "check whether the printer has paper and whether the ink or toner level is "
        "sufficient. Next, check that the selected printer matches the device being "
        "used. Run the printer cleaning utility when the device manual recommends it. "
        "After the checks, print a test page and inspect whether text appears. If the "
        "problem continues, record the printer model and any displayed message before "
        "contacting technical support. Do not apply scanner instructions to a printer "
        "because the devices have different functions. Follow the device manual. "
        "This is fictional troubleshooting content for a classroom exercise."
    ),
}

QUESTIONS = [
    {"query": "What evidence is needed for an illness extension?", "doc": "late",
     "evidence": "Illness extensions require medical evidence before the deadline.", "split": "dev"},
    {"query": "How can I recover a forgotten account password?", "doc": "password",
     "evidence": "A forgotten account password can be reset using the recovery link on the sign-in page.", "split": "dev"},
    {"query": "Where do students upload their coursework?", "doc": "assignment",
     "evidence": "Assignments in this synthetic learning portal are submitted through the assignment upload page.", "split": "dev"},
    {"query": "Can a contractor work remotely?", "doc": "contractor",
     "evidence": "contractors may work remotely only if the signed contract explicitly permits remote work.", "split": "dev"},
    {"query": "What should I check if my printer makes blank pages?", "doc": "printer",
     "evidence": "For blank printer pages in this synthetic troubleshooting guide, first check whether the printer has paper and whether the ink or toner level is sufficient.", "split": "test"},
    {"query": "I cannot get into my account; how do I regain access?", "doc": "password",
     "evidence": "A forgotten account password can be reset using the recovery link on the sign-in page.", "split": "test"},
    {"query": "How should I hand in the final assignment file?", "doc": "assignment",
     "evidence": "The final file should be saved in PDF format unless the task instructions specify another format.", "split": "test"},
    {"query": "What proof is required when a student is ill?", "doc": "late",
     "evidence": "Illness extensions require medical evidence before the deadline.", "split": "test"},
    {"query": "What are tomorrow's flight prices?", "doc": None,
     "evidence": None, "split": "test"},
    {"query": "Who won yesterday's football match?", "doc": None,
     "evidence": None, "split": "test"},
]


# ---------------------------------------------------------------------
# TASK 1 — TOKENIZATION
# ---------------------------------------------------------------------

def run_task1():
    print("\n" + "=" * 68)
    print("TASK 1 — TOKENIZATION")
    samples = [
        "AI, search!", "I can't log in.", "help@example.com",
        "CS4944 version 2.1", "", "یہ ایک مثال ہے"
    ]
    for original in samples:
        whitespace = original.split()
        word_like = re.findall(r"\b\w+\b", original, flags=re.UNICODE)
        print("\nOriginal:", repr(original))
        print("Whitespace tokens:", whitespace, "| count:", len(whitespace))
        print("Word-like tokens:", word_like, "| count:", len(word_like))

    print("\nObservations:")
    print("- Whitespace splitting keeps punctuation attached to nearby words.")
    print("- Regex tokenization separates some punctuation and contractions.")
    print("- Email addresses can be split into multiple pieces.")
    print("- This simple regex is not a complete Urdu tokenizer.")

    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
        )
        print("\nOptional model subword tokenization:")
        for sample in samples[:2]:
            print(repr(sample), "=>", model.tokenizer.tokenize(sample))
    except Exception as exc:
        print("\nOptional subword comparison skipped:", exc)


# ---------------------------------------------------------------------
# TASK 2 — TEXT CHUNKING WITH SOURCE OFFSETS
# ---------------------------------------------------------------------

def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size.")
    spans = word_spans(text)
    result = []
    step = size - overlap
    for i in range(0, len(spans), step):
        last = min(i + size, len(spans))
        result.append((offset + spans[i][0], offset + spans[last - 1][1]))
        if last == len(spans):
            break
    return result


def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("size must be positive.")
    cuts = [0] + [m.end() for m in re.finditer(r"[.!?]\s+", text)] + [len(text)]
    output, pending, count = [], None, 0
    for start, end in zip(cuts, cuts[1:]):
        segment = text[start:end]
        word_count = len(segment.split())
        if not word_count:
            continue
        if word_count > size:
            if pending is not None:
                output.append(pending)
            output.extend(windows(segment, size=size, overlap=0, offset=start))
            pending, count = None, 0
        elif pending is not None and count + word_count <= size:
            pending, count = (pending[0], end), count + word_count
        else:
            if pending is not None:
                output.append(pending)
            pending, count = (start, end), word_count
    if pending is not None:
        output.append(pending)
    return output


def make_chunks(docs, strategy):
    chunks = []
    for doc_id, source_text in docs.items():
        if strategy == "sentence":
            spans = sentence_chunks(source_text, size=40)
        elif strategy in {"0", "10"}:
            spans = windows(source_text, size=40, overlap=int(strategy))
        else:
            raise ValueError("Strategy must be '0', '10', or 'sentence'.")
        for index, (start, end) in enumerate(spans):
            chunks.append({
                "id": f"{doc_id}:{index}", "doc": doc_id,
                "source": f"{doc_id}.txt", "start": start, "end": end,
                "text": source_text[start:end]
            })
    return chunks


def run_task2():
    print("\n" + "=" * 68)
    print("TASK 2 — TEXT CHUNKING")
    demo = "Late work is penalized. Illness may qualify for an extension with medical evidence. Ask the coordinator first."
    assert windows("") == []
    assert windows("short text") == [(0, 10)]
    try:
        windows("a b", size=2, overlap=2)
    except ValueError:
        print("Invalid overlap test passed.")
    else:
        raise AssertionError("Invalid overlap was accepted.")

    for strategy in ("0", "10", "sentence"):
        spans = (sentence_chunks(demo, 12) if strategy == "sentence"
                 else windows(demo, size=12, overlap=int(strategy)))
        print("\nStrategy:", strategy)
        for start, end in spans:
            print({"start": start, "end": end, "text": demo[start:end]})


# ---------------------------------------------------------------------
# TASK 3 — RETRIEVAL, TOP-3 RESULTS, HIT@3 AND MRR@3
# ---------------------------------------------------------------------

def retrieval_scores(method, chunks, query_texts):
    texts = [item["text"] for item in chunks]
    started = time.perf_counter()
    if method == "tfidf":
        vectorizer = TfidfVectorizer()
        doc_vectors = vectorizer.fit_transform(texts)
        query_vectors = vectorizer.transform(query_texts)
        scores = (query_vectors @ doc_vectors.T).toarray()
    elif method == "embedding":
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2", device="cpu"
        )
        for item in texts + query_texts:
            ids = model.tokenizer(item, truncation=False)["input_ids"]
            if len(ids) > model.max_seq_length:
                raise ValueError("Text exceeds model token limit.")
        doc_vectors = model.encode(texts, normalize_embeddings=True)
        query_vectors = model.encode(query_texts, normalize_embeddings=True)
        scores = query_vectors @ doc_vectors.T
    else:
        raise ValueError("Unknown retrieval method.")
    elapsed = time.perf_counter() - started
    return scores, elapsed


def calculate_metrics(scores, chunks, questions):
    hits, reciprocal_ranks = [], []
    for row, question in zip(scores, questions):
        if question["doc"] is None:
            continue
        top = np.argsort(-row, kind="stable")[:3]
        ranks = [
            rank for rank, idx in enumerate(top, 1)
            if chunks[idx]["doc"] == question["doc"]
            and question["evidence"] in chunks[idx]["text"]
        ]
        hits.append(bool(ranks))
        reciprocal_ranks.append(1 / ranks[0] if ranks else 0)
    if not hits:
        return None, None
    return float(np.mean(hits)), float(np.mean(reciprocal_ranks))


def run_task3():
    print("\n" + "=" * 68)
    print("TASK 3 — RETRIEVAL EVALUATION")
    all_logs = []
    query_texts = [item["query"] for item in QUESTIONS]

    for strategy in ("0", "10", "sentence"):
        chunks = make_chunks(CORPUS, strategy)
        for method in ("tfidf", "embedding"):
            try:
                scores, elapsed = retrieval_scores(method, chunks, query_texts)
            except Exception as exc:
                print(f"\nSkipping {strategy}/{method}: {exc}")
                continue

            print(f"\nStrategy={strategy}, method={method}, chunks={len(chunks)}")
            for split in ("dev", "test"):
                indices = [i for i, q in enumerate(QUESTIONS) if q["split"] == split]
                split_scores = scores[indices]
                split_questions = [QUESTIONS[i] for i in indices]
                hit, mrr = calculate_metrics(split_scores, chunks, split_questions)
                print(split, "Hit@3 =", hit, "MRR@3 =", mrr)

            print("Total fit/encode + query time (seconds):", round(elapsed, 4))
            for row, question in zip(scores, QUESTIONS):
                top = np.argsort(-row, kind="stable")[:3]
                for rank, idx in enumerate(top, 1):
                    chunk = chunks[idx]
                    log = {
                        "strategy": strategy, "method": method,
                        "query": question["query"], "split": question["split"],
                        "rank": rank, "score": float(row[idx]),
                        "chunk_id": chunk["id"], "doc": chunk["doc"],
                        "start": chunk["start"], "end": chunk["end"],
                        "text": chunk["text"],
                        "answerable": question["doc"] is not None,
                        "elapsed_seconds_total": elapsed
                    }
                    all_logs.append(log)
                    print(f"Top {rank}: {chunk['id']} score={row[idx]:.3f}")

    if all_logs:
        with open("retrieval_log.csv", "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(all_logs[0]))
            writer.writeheader()
            writer.writerows(all_logs)
        print("\nSaved retrieval_log.csv in the current folder.")


# ---------------------------------------------------------------------
# FAQ CHATBOT — exact match, suggestions and empty input handling
# ---------------------------------------------------------------------

FAQ = [
    {"id": "faq:password", "question": "How do I reset my password?",
     "answer": "Use the recovery link on the login page.", "source": "it_help.txt"},
    {"id": "faq:submit", "question": "Where do I submit my assignment?",
     "answer": "Use the assignment upload page in the learning portal.", "source": "assessment.txt"},
    {"id": "faq:late", "question": "Can illness justify a late submission?",
     "answer": "Request an extension with medical evidence before the deadline.", "source": "handbook.txt"},
    {"id": "faq:contact", "question": "How can I contact the help desk?",
     "answer": "Use the official help desk contact channel.", "source": "support.txt"},
    {"id": "faq:pdf", "question": "Which file format should I upload?",
     "answer": "Use PDF unless the assignment instructions specify another format.", "source": "assessment.txt"},
]


def run_faq_chatbot():
    records = [
        {"id": item["id"], "question": item["question"],
         "text": item["question"] + " " + item["answer"],
         "answer": item["answer"], "source": item["source"]}
        for item in FAQ
    ]
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform([r["text"] for r in records])
    print("\nFAQ assistant started. Type 'exit' to stop.")
    while True:
        query = input("You: ").strip()
        if query.lower() == "exit":
            break
        if not query:
            print("Bot: Please enter a question.")
            continue
        exact = next((r for r in records
                      if query.casefold() == r["question"].casefold()), None)
        if exact:
            print("Bot:", exact["answer"], "[source:", exact["source"] + "]")
            continue
        qv = vectorizer.transform([query])
        if qv.nnz == 0:
            print("Bot: No matching FAQ. Please contact the help desk.")
            continue
        scores = (qv @ matrix.T).toarray()[0]
        top = np.argsort(-scores, kind="stable")[:3]
        print("Bot: Possible matches; choose or rephrase:")
        for idx in top:
            if scores[idx] > 0:
                print("-", records[idx]["question"], f"(score {scores[idx]:.3f})")


# ---------------------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------------------

def main():
    while True:
        print("\n" + "=" * 50)
        print("LAB 6 — NLP FUNDAMENTALS")
        print("1. Run Task 1: Tokenization")
        print("2. Run Task 2: Chunking")
        print("3. Run Task 3: Retrieval evaluation")
        print("4. Start FAQ chatbot")
        print("5. Run all tasks")
        print("0. Exit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            run_task1()
        elif choice == "2":
            run_task2()
        elif choice == "3":
            run_task3()
        elif choice == "4":
            run_faq_chatbot()
        elif choice == "5":
            run_task1()
            run_task2()
            run_task3()
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose 0 to 5.")


if __name__ == "__main__":
    main()
