import streamlit as st
import numpy as np
import pandas as pd
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import torch

# Define a function to load data
@st.cache_data
def load_data():
    item_feature_matrix = np.load('item_feature_matrix.npy')
    user_feature_matrix = np.load('user_feature_matrix.npy')
    games_df = pd.read_csv('games_df.csv')
    return item_feature_matrix, user_feature_matrix, games_df

# Function to get text embedding
def get_embedding(text):
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).cpu().detach().numpy()

# Function to recommend games
def recommend_games(user_input, item_feature_matrix, games_df):
    user_embedding = get_embedding(user_input)
    similarities = cosine_similarity(user_embedding, item_feature_matrix)
    top_n = 5
    recommendations = similarities[0].argsort()[-top_n:][::-1]
    return recommendations

# Streamlit app
st.title("Steam Game Recommendation System")

# Load data
item_feature_matrix, user_feature_matrix, games_df = load_data()

# User input
user_input = st.text_area("Enter a description of the type of game you want to play:")

if st.button("Get Recommendations"):
    recommendations = recommend_games(user_input, item_feature_matrix, games_df)
    st.write("Top 5 Recommended Games:")
    for idx in recommendations:
        game_info = games_df[games_df['appid'] == idx].iloc[0]
        st.write(f"Name: {game_info['name']}")
        st.write(f"Description: {game_info['description']}")
        st.write(f"Price: {game_info['price']}")
        st.write(f"Release Date: {game_info['release_date']}")
        st.write(f"Developer: {game_info['developer']}")
        st.write(f"Publisher: {game_info['publisher']}")
        st.write(f"Tags: {game_info['tags']}")
        st.write("---")
