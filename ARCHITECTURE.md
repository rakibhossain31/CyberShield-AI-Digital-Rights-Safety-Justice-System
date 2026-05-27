# Architecture Guide

## High-level flow

```text
Victim/support worker report
  -> Redaction and validation
  -> Case classification
  -> Risk and escalation scoring
  -> RAG-style legal/support guidance retrieval
  -> FIR/complaint draft generation
  -> Evidence vault hashing and chain-of-custody log
  -> Anonymized repeat-pattern detection
  -> Dashboard, audit logs, and monitoring
```

## Components

### 1. User Interaction Layer
Implemented through FastAPI and Streamlit. The API exposes machine-readable endpoints. The dashboard provides a non-technical view for demo, review, and monitoring.

### 2. AI Victim Advocate Service
`src/cybershield_ai/services/victim_advocate.py` orchestrates the complete workflow. It calls the classifier, RAG engine, risk scorer, FIR generator, awareness engine, database, and audit logger.

### 3. Case Classification Model
`case_classifier.py` uses deterministic keyword logic. This keeps the prototype safe, explainable, and runnable without paid APIs. In a production design, this could be replaced by a trained classifier with bias testing and human review.

### 4. RAG-style Legal Knowledge Engine
`legal_rag.py` loads local guidance from `data/demo/legal_knowledge.md`, indexes sections with TF-IDF, and retrieves the most relevant guidance for a report. It does not provide legal advice. It only gives context for human review.

### 5. Evidence Vault
`evidence_vault.py` hashes evidence using SHA-256 and links evidence records using a hash chain. This simulates blockchain-style integrity without requiring external blockchain infrastructure.

### 6. Repeat Pattern Tracker
`offender_graph.py` anonymizes identifiers with hashes and counts repeated patterns. It never stores public-facing offender names. This is designed for privacy-aware intelligence.

### 7. Monitoring and Audit
The SQLite database stores cases, evidence, feedback, and audit events. Monitoring scripts create JSON and HTML reports from stored activity.

## Why this architecture is realistic

Real sensitive AI systems need more than prediction. They need safe input handling, traceability, human review, explainability, evidence integrity, abuse prevention, privacy controls, and monitoring. This project demonstrates those ideas in a runnable portfolio system.
