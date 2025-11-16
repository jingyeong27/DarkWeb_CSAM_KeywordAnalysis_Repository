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
- All raw dark web text data originally used in this study contained CSAM-related materials.  
  These raw datasets **cannot be shared** due to legal and ethical restrictions.  
- The files provided here are **derived, filtered, and fully sanitized** to ensure that  
  **no illegal or harmful material** is present.


> ⚠️ **Disclaimer:**  
> This repository does **not** contain any illegal, harmful, or explicit material.  
> All data are non-sensitive and intended solely for academic reproducibility and verification.
