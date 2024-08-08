import streamlit as st
import pandas as pd
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
import pickle

# Load data and model
@st.cache(allow_output_mutation=True)
def load_data():
    item_feature_matrix = np.load('item_feature_matrix.npy', allow_pickle=True)
    with open('user_feature_matrix.pkl', 'rb') as f:
        user_feature_matrix = pickle.load(f)
    return item_feature_matrix, user_feature_matrix

@st.cache_resource
def load_model():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    return tokenizer, model

item_feature_matrix, user_feature_matrix = load_data()
tokenizer, model = load_model()

# Function to get embeddings
def get_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).cpu().detach().numpy()

# Streamlit UI
st.title("Game Recommendation System")
st.write("Enter a description of the type of game you want to play:")

user_input = st.text_area("Game description")

if st.button("Get Recommendations"):
    if user_input:
        user_embedding = get_embedding(user_input)
        similarities = np.dot(user_embedding, item_feature_matrix.T)
        top_n = 5
        recommendations = np.argsort(similarities[0])[-top_n:][::-1]

        st.write("Top 5 Recommended Games:")
        for idx in recommendations:
            game_info = item_feature_matrix.iloc[idx]
            st.write(f"**{game_info['name']}**")
            st.write(f"Description: {game_info['description']}")
            st.write(f"Price: {game_info['price']}")
            st.write("---")
    else:
        st.write("Please enter a game description.")
