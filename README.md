# Steam-lit: Word Embeddings and LDA-based NLP Recommendation System

Welcome to **Steam-lit**, a personalized game recommendation system that leverages Natural Language Processing (NLP) techniques such as BERT word embeddings and Latent Dirichlet Allocation (LDA) for topic modeling to suggest games based on user descriptions.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Mathematical Foundations](#mathematical-foundations)
  - [BERT Word Embeddings](#bert-word-embeddings)
  - [Latent Dirichlet Allocation (LDA)](#latent-dirichlet-allocation-lda)
  - [Cosine Similarity](#cosine-similarity)
- [Data](#data)
- [Project Structure](#project-structure)
- [Contributing](#contributing)


## Introduction
Steam-lit is an NLP-based game recommendation system that combines the power of BERT for capturing semantic meaning from text with LDA to discover latent topics in game reviews. By merging these features, the system can accurately recommend games based on user-inputted descriptions.

## Features
- **BERT Word Embeddings**: Utilizes pre-trained BERT models to convert user input into dense vectors that capture semantic meanings.
- **LDA Topic Modeling**: Discovers underlying topics from user reviews to enrich the feature set for each game.
- **Cosine Similarity**: Calculates the similarity between user input and game descriptions to generate top recommendations.
- **Streamlit Interface**: A user-friendly web app to input descriptions and receive game recommendations.

## Mathematical Foundations

### BERT Word Embeddings
BERT (Bidirectional Encoder Representations from Transformers) is a deep learning model that generates context-aware word embeddings. Unlike traditional word embeddings (e.g., Word2Vec, GloVe), BERT considers the entire sentence, making it effective for understanding nuances in language.

**Mathematics**: 
- For a given sentence \(S\), BERT generates an embedding \(E_S\) by encoding the sentence using a Transformer architecture. The final output is a dense vector where each dimension captures semantic information of the sentence.
- The word embeddings are calculated by averaging the hidden states from the last layer of BERT.

### Latent Dirichlet Allocation (LDA)
LDA is a generative probabilistic model used to discover latent topics in a collection of documents. Each document is represented as a mixture of topics, and each topic is represented as a mixture of words.

**Mathematics**:
- For each document \(d\) in the corpus, LDA assumes the following generative process:
  1. Choose \( \theta_d \sim \text{Dirichlet}(\alpha) \)
  2. For each word \(w_i\) in \(d\):
     - Choose a topic \(z_i \sim \text{Multinomial}(\theta_d)\)
     - Choose a word \(w_i\) from \(P(w_i|z_i,\beta)\), a multinomial probability conditioned on the topic \(z_i\).
- Here, \( \alpha \) and \( \beta \) are Dirichlet priors, and the model learns the topic distribution \( \theta_d \) and word distribution \( \phi_k \) for each topic \( k \).

### Cosine Similarity
Cosine similarity measures the cosine of the angle between two non-zero vectors in an inner product space. It is often used to measure document similarity in text analysis.

**Mathematics**:
- The cosine similarity between two vectors \( A \) and \( B \) is given by:
  \[
  \text{cosine\_similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}
  \]
- In this project, cosine similarity is used to compute the similarity between the user's input embedding and the game description embeddings.

## Data

The data for this project was sourced from the Steam Web API, which provides game details and user reviews. The data processing involves:
- Removing irrelevant entries (e.g., soundtracks, DLCs).
- Tokenizing and cleaning review texts.
- Generating embeddings and topic distributions for games.

## Project Structure

```plaintext
steam-lit/
│
├── data/                     # Contains the SQLite database and CSV files
├── models/                   # Contains the pre-trained models and feature matrices
├── notebooks/                # Jupyter notebooks for development and testing
├── streamlit_app.py          # Main Streamlit app script
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation
└── LICENSE                   # License file
```

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or improvements, feel free to fork the repository and create a pull request.

