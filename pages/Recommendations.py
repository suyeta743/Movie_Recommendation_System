import streamlit as st
import ast
from functions import *
# from filter_functions import get_youtube_trailler

movie_name = "Jumanji"
try:
    movie_name = st.session_state.name
except:
    st.write("You Have Not Selected Any Movie")

st.header(f"Recommended Movies of {movie_name}")

recommended_movie_id = ast.literal_eval(df[df['title'] == movie_name].
                                        recommendations.values[0])

for i in range(0,9,3):
    col1,col2,col3 = st.columns(3)
    with col1:show_recommendations(recommended_movie_id[i])
    with col2: show_recommendations(recommended_movie_id[i+1])
    with col3: show_recommendations(recommended_movie_id[i+2])
    st.markdown("---")
