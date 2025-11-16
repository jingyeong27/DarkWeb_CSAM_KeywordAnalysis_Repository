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

---

## Citation
If you use this dataset, please cite:

> Kim, J.G., & Kim, J. (2025). *Hybrid Text Mining Models for Expanding Investigative Clues on Child Sexual Abuse in the Dark Web*. PLOS ONE.

---

## Funding
This work was supported by  
‘Tech. Challenge for Future Program Policing’ (www.kipot.or.kr)
funded by the Ministry of Science and ICT (MSIT, Korea) and the Korean National Police Agency (KNPA, Korea).[Project Name] Development of Active Dark Web Information Collection, Analysis and Tracking Technology to Prevent Dark Web Crime [Project Number]RS-2023-00244362  
*The funders had no role in study design, data collection and analysis, decision to publish, or preparation of the manuscript.*

---

## Contact
**Corresponding Author:**  
Dr. Jiyeon Kim  
Department of Computer Engineering, Daegu University  
Email: [your-email@example.com]

---

> ⚠️ **Disclaimer:**  
> This repository does **not** contain any illegal, harmful, or explicit material.  
> All data are non-sensitive and intended solely for academic reproducibility and verification.
