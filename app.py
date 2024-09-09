import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load data
popular_df = pickle.load(open('./popular.pkl', 'rb'))
pt = pickle.load(open('./pt.pkl', 'rb'))
books = pickle.load(open('./books.pkl', 'rb'))
similarity_scores = pickle.load(open('./similarity_scores.pkl', 'rb'))

# Function to recommend books
def recommend(book_name):
    index = np.where(pt.index == book_name)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    return data

# Set up the Streamlit app
st.set_page_config(page_title="Book Recommender", page_icon="📚")

# Tabs for navigation
tab1, tab2 = st.tabs(["Top 50 Books", "Book Recommender"])

# Page 1: Top 50 Books
with tab1:
    st.title("Top 50 Books")
    cols = st.columns(5)  # Create 5 columns for grid layout
    for index, row in popular_df.iterrows():
        col = cols[index % 5]  # Cycle through columns
        with col:
            st.image(row['Image-URL-M'], width=100)
            st.write(f"**{row['Book-Title']}** by {row['Book-Author']}")
            st.write(f"Avg Rating: {row['avg_rating']}, Num Ratings: {row['num_ratings']}")
            st.markdown(f"[Link to Book](#)", unsafe_allow_html=True)  # Replace # with actual link if available

# Page 2: Book Recommender
with tab2:
    st.title("Book Recommender")
    book_list = popular_df['Book-Title'].values
    selected_book = st.selectbox("Select a book to get recommendations:", book_list)
    if st.button("Recommend"):
        recommendations = recommend(selected_book)
        st.write("Here are some books you might like:")
        rec_cols = st.columns(4)  # Create 4 columns for recommendations
        for i, rec in enumerate(recommendations):
            with rec_cols[i]:
                st.image(rec[2], width=100)
                st.write(f"**{rec[0]}** by {rec[1]}")





