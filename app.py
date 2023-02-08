import streamlit as st
import webbrowser
from functions import df
import pyttsx3
from filter_functions import get_image_with_text,get_youtube_trailler

with open("design.css") as filename:
    st.markdown(f"<style>{filename.read()}</style>",unsafe_allow_html=True)

st.markdown("<h1>Movie Recommendation System</h1>",unsafe_allow_html=True)

selected_movie = st.selectbox(
    label="Type or Select a movie",
    options=df['title']
)


from functions import *

# if st.button("Get Details"):
movie_id = df[df['title'] == selected_movie].id.values[0]
st.session_state.id = movie_id
st.session_state.imdb_id = df[df['title'] == selected_movie].imdb_id.values[0]
st.session_state.name = selected_movie

# try:
#     doc = get_movie_details(movie_id)
# except:
#     doc = None
doc=get_movie_details(movie_id)

left,right = st.columns(2)
with left:
    try:
        st.image("https://image.tmdb.org/t/p/original" + doc['poster_path'] if doc else "")
    except:
        st.image("https://th.bing.com/th/id/OIP.svp_xDT7rtBajr3qbm43JwHaK")
with right:
    st.title("Title : " + selected_movie)
    st.markdown("**Tagline :** " + doc['tagline'] if doc!=None else "")
    st.markdown("**Genres :** " + list_to_str(doc["genres"]) if doc!=None else "")
    st.markdown("**Rating :** " + str(doc["vote_average"]) if doc!=None else "")
    st.markdown("**Votes :** " + str(doc['vote_count']) if doc!=None else "")
    st.markdown("**Release Date :** " + doc["release_date"] if doc!=None else "")
    st.markdown("**Duration :** " + str(doc["runtime"] if doc!=None else "") + " Min.")
    # link = '[Watch Trailer]({})'.format(doc['trailer'] if doc!=None else "")
    # if st.button('Trailer'):
    #     webbrowser.open_new_tab(get_youtube_trailler(movie_name=selected_movie))
    st.markdown(
        f"""
                <a href="{get_youtube_trailler(movie_name=selected_movie)}" style="padding: 8px 12px; background-color: blue; color: white; border-radius: 4px; text-decoration: none;">Watch Trailer</a>
                """,
        unsafe_allow_html=True,
    )

    if st.button('OTT'):
        webbrowser.open_new_tab(doc['ott'] if doc!=None else "")

if st.button('Overview'):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 120)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(doc["overview"] if doc!=None else "")
    engine.runAndWait()
st.markdown("**Overview :** " + doc['overview'] if doc!=None else "")

st.markdown("---")

st.subheader("Top Casts")
cast_dict = get_cast_detail(movie_id)


for i in range(0,len(cast_dict),3):
    left, mid, right = st.columns(3)
    with left:
        st.subheader(cast_dict[i]["name"])
        st.markdown("**Played as : " + cast_dict[i]["character"] + "**")
        try:
            st.image("https://www.themoviedb.org/t/p/w300_and_h450_bestv2" +
                 cast_dict[i]['profile_path'])
        except:
            st.image("https://th.bing.com/th/id/OIP.svp_xDT7rtBajr3qbm43JwHaK")
    with mid:
        st.subheader(cast_dict[i+1]["name"])
        st.markdown("**Played as : " + cast_dict[i+1]["character"] + "**")
        try:
            st.image("https://www.themoviedb.org/t/p/w300_and_h450_bestv2" +
                 cast_dict[i+1]['profile_path'])
        except:
            st.image("https://th.bing.com/th/id/OIP.svp_xDT7rtBajr3qbm43JwHaK")

    with right:
        st.subheader(cast_dict[i+2]["name"])
        st.markdown("**Played as : " + cast_dict[i+2]["character"] + "**")
        try:
            st.image("https://www.themoviedb.org/t/p/w300_and_h450_bestv2" +
                 cast_dict[i+2]['profile_path'])
        except:
            st.image("https://th.bing.com/th/id/OIP.svp_xDT7rtBajr3qbm43JwHaK")
    st.markdown("---")

for i in range(6):
    st.markdown("<h3>Popular Movies of " + cast_dict[i]['name'] + "</h3>",unsafe_allow_html=True)
    # print("Popular Movies of " + cast_dict[i]['name'])
    c1,c2,c3 = st.columns(3)
    len_ = len(cast_dict[i]['known_for'])
    if len_ > 0:
        with c1:
            try:
                st.image(cast_dict[i]['known_for'][0]['poster'])
            except:
                st.image(get_image_with_text(text=cast_dict[i]['known_for'][0]['title'], width=150, height=225,
                                             font_width=20))
            st.markdown("**" + cast_dict[i]['known_for'][0]['title'] + "**")
    if len_ > 1:
        with c2:
            try:
                st.image(cast_dict[i]['known_for'][1]['poster'])
            except:
                st.image(get_image_with_text(text=cast_dict[i]['known_for'][1]['title'], width=150, height=225,
                                             font_width=20))
            st.markdown("**" + cast_dict[i]['known_for'][1]['title'] + "**")
    if len_ > 2:
        with c3:
            try:
                st.image(cast_dict[i]['known_for'][2]['poster'])
            except:
                st.image(get_image_with_text(text=cast_dict[i]['known_for'][2]['title'], width=150, height=225,
                                             font_width=20))
            st.markdown("**" + cast_dict[i]['known_for'][2]['title'] + "**")

    st.markdown("----")

    c1,c2,c3 = st.columns(3)
    len_ = len(cast_dict[i]['known_for'])
    if len_ > 3:
        with c1:
            try:
                st.image(cast_dict[i]['known_for'][3]['poster'])
            except:
                st.image(get_image_with_text(text=cast_dict[i]['known_for'][3]['title'], width=150, height=225,
                                             font_width=20))

            st.markdown("**" + cast_dict[i]['known_for'][3]['title'] + "**")
    if len_ > 4:
        with c2:
            # st.write(cast_dict[i]['known_for'][4]['poster'])
            try:
                st.image(cast_dict[i]['known_for'][4]['poster'])
            except :
                st.image(get_image_with_text(text= cast_dict[i]['known_for'][4]['title'],width=150,height=225,font_width=20))
            st.markdown("**" + cast_dict[i]['known_for'][4]['title'] + "**")
    if len_ > 5:
        with c3:

            try:
                st.image(cast_dict[i]['known_for'][5]['poster'])
            except:
                st.image(get_image_with_text(text=cast_dict[i]['known_for'][5]['title'], width=150, height=225,
                                             font_width=20))
            st.markdown("**" + cast_dict[i]['known_for'][5]['title'] + "**")
    st.markdown("----")
    st.markdown("----")

    # if len_ > 1:c2.image(cast_dict[i]['known_for'][1]['poster'])
    # if len_ > 2:c3.image(cast_dict[i]['known_for'][2]['poster'])
    # if len_ > 3:c4.image(cast_dict[i]['known_for'][3]['poster'])
    # if len_ > 4:c5.image(cast_dict[i]['known_for'][4]['poster'])
