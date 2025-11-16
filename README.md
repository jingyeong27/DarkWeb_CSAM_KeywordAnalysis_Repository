# Derived Non-Sensitive Dataset for "Hybrid Text Mining Models for Expanding Investigative Clues on Child Sexual Abuse in the Dark Web"

## Overview
This repository provides **derived, non-sensitive datasets** supporting the manuscript  
**“Hybrid Text Mining Models for Expanding Investigative Clues on Child Sexual Abuse in the Dark Web” (PLOS ONE submission).**

The data in this repository were generated from the original dark web text corpus used in the study,  
but **all harmful or illegal content (e.g., CSAM text or URLs) has been fully removed**.  
Only aggregated, anonymized, and semantically representative results are included to ensure compliance  
with ethical and legal standards.

---

## Contents
The repository contains the following non-sensitive, derived materials:

- **`Top 20 Keywords Extracted Using TF-IDF.csv`**  
  Top 20 keywords ranked by TF-IDF scores.

- **`Top 20 Keywords Extracted Using Eigenvector Centrality.csv`**  
  Top 20 keywords ranked by eigenvector centrality in the co-occurrence network.

- **`Top 20 Keywords Extracted Using Word2Vec.csv`**  
  Top 20 keywords derived from the Word2Vec model.

- **`word frequency distribution.csv`**  
  Word frequency distribution used for analysis and model validation.

- **`cooccurrence_network.pkl`**  
  Pickled NetworkX graph of the anonymized term co-occurrence network (nodes: terms, edges: co-occurrences).

- **`word2vec_embeddings.csv`**  
  Word2Vec embedding vectors for non-sensitive terms (first column: token, remaining columns: embedding dimensions).

---

## Ethical Compliance
The original dark web text data used in this study contained materials related to child sexual abuse (CSAM); therefore, the raw data cannot be disclosed due to legal and ethical restrictions.

All files in this repository are derived, filtered, and sanitized datasets, and while some potentially sensitive content may remain in minimal form, they are provided solely for academic reproducibility and verification purposes.
