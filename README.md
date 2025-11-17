Derived Non-Sensitive Dataset and Analysis Code for

“Hybrid Text Mining Models for Expanding Investigative Clues on Child Sexual Abuse in the Dark Web”

Overview

This repository provides derived, non-sensitive datasets and analysis codes supporting the manuscript
“Hybrid Text Mining Models for Expanding Investigative Clues on Child Sexual Abuse in the Dark Web” (PLOS ONE submission).

All harmful or illegal content (e.g., CSAM-related text or URLs) has been completely removed.
Only anonymized, aggregated, and ethically compliant data and code are shared to ensure legal and research integrity.

Contents
🧾 Data Files

Top 20 Keywords Extracted Using TF-IDF.csv – Top 20 keywords ranked by TF-IDF scores.

Top 20 Keywords Extracted Using Eigenvector Centrality.csv – Top 20 keywords ranked by eigenvector centrality in the co-occurrence network.

Top 20 Keywords Extracted Using Word2Vec.csv – Top 20 keywords derived from the Word2Vec model.

word frequency distribution.csv – Word frequency distribution used for analysis and model validation.

cooccurrence_network.pkl – Pickled NetworkX graph of the anonymized term co-occurrence network (nodes: terms, edges: co-occurrences).

word2vec_embeddings.csv – Word2Vec embedding vectors for non-sensitive terms (first column: token, remaining columns: embedding dimensions).

💻 Analysis Code

This repository also includes the source code used for the analytical experiments described in the manuscript:

tfidf_extraction.py – Implementation of TF–IDF-based keyword extraction.

eigenvector_centrality.py – Co-occurrence network construction and eigenvector centrality computation.

word2vec_extraction.py – Word2Vec model training and keyword similarity scoring.

hybrid_model.py – Proposed hybrid model combining eigenvector centrality with TF–IDF and Word2Vec to enhance investigative keyword precision and contextual relevance.

visualization.py – Network visualization utilities for keyword–term relations (using Pyvis or NetworkX).

All codes were developed in Python (v3.10+), relying on open libraries such as gensim, networkx, and scikit-learn.
They are shared for academic reproducibility, transparency, and independent validation.

Ethical Compliance

The original dark web text data used in this study contained materials related to child sexual abuse (CSAM);
therefore, the raw corpus is not disclosed due to legal and ethical restrictions.
All datasets and codes provided here are fully sanitized and intended for academic replication only.
Researchers reproducing this work must ensure compliance with their own institutional ethical review processes.
