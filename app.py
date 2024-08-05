import streamlit as st
import pandas as pd
import seaborn as sns

@st.cache_data
def load_data():
    return pd.read_csv("your_data.csv")

def plot_data(df, x_col, y_col):
    fig = sns.scatter(df, x=x_col, y=y_col)
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