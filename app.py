import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def load_data():
    return pd.read_csv("./data/raw/steam_games_partial.csv")

def plot_data(df, x_col, y_col):
    fig = px.scatter(df, x=x_col, y=y_col)
    return st.plotly_chart(fig)

def main():
    st.title("Data Explorer")

    df = load_data()

    with st.sidebar:
        x_col = st.selectbox("Select X column", df.columns)
        y_col = st.selectbox("Select Y column", df.columns)

    if st.button("Plot Data"):
        plot_data(df, x_col, y_col)

if __name__ == "__main__":
    main()