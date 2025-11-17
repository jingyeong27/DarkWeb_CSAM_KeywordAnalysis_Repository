## Contents

### 1. Data Files

The repository contains the following **non-sensitive, derived datasets**:

- **`Top 20 Keywords Extracted Using TF-IDF.csv`**  
  Top 20 keywords ranked by TF–IDF scores.

- **`Top 20 Keywords Extracted Using Eigenvector Centrality.csv`**  
  Top 20 keywords ranked by eigenvector centrality in the term co-occurrence network.

- **`Top 20 Keywords Extracted Using Word2Vec.csv`**  
  Top 20 keywords derived from the Word2Vec model.

- **`word frequency distribution.csv`**  
  Word frequency distribution used for analysis and model validation.

- **`cooccurrence_network.pkl`**  
  Pickled NetworkX graph of the anonymized term co-occurrence network  
  (nodes: terms, edges: co-occurrence relationships).

- **`word2vec_embeddings.csv`**  
  Word2Vec embedding vectors for non-sensitive terms  
  (first column: token, remaining columns: embedding dimensions).

---

### 2. Analysis Code

This repository also includes the **analysis code** used to implement the methods described in the manuscript:

- **`tfidf_extraction.py`**  
  Implementation of TF–IDF–based keyword extraction.

- **`eigenvector_centrality.py`**  
  Construction of the co-occurrence network and computation of eigenvector centrality.

- **`word2vec_extraction.py`**  
  Training of the Word2Vec model and computation of semantic similarity scores.

- **`hybrid_model.py`**  
  Implementation of the **proposed hybrid model** that combines:
  - eigenvector centrality (structural centrality),
  - TF–IDF–based statistical rarity, and
  - Word2Vec–based semantic similarity  
  to improve investigative keyword precision and contextual relevance.

- **`visualization.py`**  
  Utility functions for visualizing term–term and keyword–term relationships  
  (e.g., NetworkX / Pyvis–based visualizations).

All scripts are implemented in **Python 3.10+** and rely on open-source libraries such as  
`gensim`, `networkx`, `scikit-learn`, and `pandas`.  
They are shared to promote **reproducibility, transparency, and independent validation** of the study.

---

## Ethical Compliance

The original dark web text data used in this study contained materials related to child sexual abuse (CSAM);  
therefore, the **raw corpus (including original text and URLs) cannot be disclosed** due to legal and ethical restrictions.

All files in this repository are **derived, filtered, and fully sanitized**.  
While certain terms may still be related to crime contexts at a lexical level,  
no directly harmful, explicit, or operationally actionable content is included.  
The datasets and code are provided **solely for academic reproducibility and verification purposes**.

Researchers who wish to replicate the study are expected to:

- obtain and process their own datasets in accordance with
  institutional review procedures, relevant laws, and ethical guidelines, and  
- apply the data collection, preprocessing, and analysis pipeline described in the manuscript  
  using the code and derived resources published in this repository.

