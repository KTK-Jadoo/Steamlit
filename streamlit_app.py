import streamlit as st
import numpy as np
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load pre-trained BERT model and tokenizer
bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

@st.cache_data
def load_data():
    games_df = pd.read_csv('filtered_games_df.csv')
    reduced_item_feature_matrix = np.load('reduced_item_feature_matrix.npy')
    return games_df, reduced_item_feature_matrix

# Function to get text embedding
def get_embedding(text):
    inputs = bert_tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
    outputs = bert_model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).cpu().detach().numpy()

# Recommendation function
def recommend_games(user_input, item_feature_matrix, games_df):
    user_embedding = get_embedding(user_input)
    similarities = cosine_similarity(user_embedding, reduced_item_feature_matrix)
    top_n = 5
    recommendations = similarities[0].argsort()[-top_n:][::-1]
    return recommendations

# Load data
games_df, reduced_item_feature_matrix = load_data()

# Streamlit app
st.markdown("<h1 class='title' style='text-align: center;'>Steam Game Recommendation System</h1>", unsafe_allow_html=True)
st.markdown("<h2 class='header' style='text-align: center;'>Find Your Next Favorite Game!</h2>", unsafe_allow_html=True)

# User input
st.markdown("<h3 class='subheader' style='text-align: center;'>Describe your ideal game:</h3>", unsafe_allow_html=True)
user_input = st.text_input("Enter a description of the game you want to play (e.g., 'I want a History focussed RPG.')", key="user_input")
st.write("<p style='text-align: center;'>Hit Enter to get your recommendations!</p>", unsafe_allow_html=True)

if user_input:
    st.markdown("<h3 class='subheader' style='text-align: center;'>Top 5 Recommended Games</h3>", unsafe_allow_html=True)
    recommendations = recommend_games(user_input, reduced_item_feature_matrix, games_df)
    for idx in recommendations:
        game_info = games_df.iloc[idx]
        st.image(f"https://steamcdn-a.akamaihd.net/steam/apps/{game_info['appid']}/header.jpg", width=300)
        st.markdown(f"<div style='text-align: center;'><strong>{game_info['name']}</strong></div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'><strong>Description:</strong> {game_info['description']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'><strong>Price:</strong> {game_info['price']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'><strong>Release Date:</strong> {game_info['release_date']}</div>", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
