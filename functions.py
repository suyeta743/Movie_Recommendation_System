import numpy as np
import pandas as pd
import re
import requests
import streamlit as st
import os
from bs4 import BeautifulSoup
import ast
import webbrowser

df = pd.read_csv("data/mrs2.csv")
filter_df = pd.read_csv("data/filter.csv")

def get_movie_details(movie_id):
    api_key = "3222076ed226933d3e1302ce9f3b73dc"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    # if response.status_code == 200:

    try:
        doc = response.json()
    except:
        st.write("Unable to fetch")
        return

    genres_list = []
    for i in doc['genres']:genres_list.append(i['name'])
    dict_ =  {
        "overview" : doc['overview'],
        "genres" : genres_list,
        "poster_path" : doc['poster_path'],
        "release_date" : doc['release_date'],
        "tagline" : doc['tagline'],
        "runtime" : doc['runtime'],
        "vote_count" : doc['vote_count'],
        "vote_average" : doc['vote_average']
    }

    # Trailer
    url = f"https://www.themoviedb.org/movie/{movie_id}"
    needed_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    response = requests.get(url, headers = needed_headers )
    # req = requests.get("https://www.themoviedb.org/person/52763-aamir-khan")
    doc = BeautifulSoup(response.content, 'html.parser')
    trailer = "https://www.youtube.com/watch?v=" + doc.find_all("a",class_="no_click play_trailer")[0]['data-id']

    dict_['trailer'] = trailer

    # OTT
    url = f"https://www.themoviedb.org/movie/{movie_id}/watch"
    needed_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    response = requests.get(url, headers = needed_headers )
    # req = requests.get("https://www.themoviedb.org/person/52763-aamir-khan")
    doc = BeautifulSoup(response.content, 'html.parser')
    ott = doc.find_all("div",class_="ott_provider")
    if ott==[]:
        ott = "https://www.netflix.com/in/"
    else:
        ott = ott[0].find_all("a")[0]['href']

    dict_["ott"] = ott
    return dict_


def get_cast_detail(movie_id):
    api_key = "3222076ed226933d3e1302ce9f3b73dc"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=en-US"
    response = requests.get(url)
    doc = response.json()

    list_of_casts = []
    for cast in doc['cast'][:6]:
        dict_ = {
            'cast_id' : cast['id'],
            'name' : cast['name'],
            'character' : cast['character'],
            'profile_path' : cast['profile_path'],
            'known_for' : []
        }

        cast_url = f"https://www.themoviedb.org/person/{dict_['cast_id']}"
        needed_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
        response = requests.get(cast_url, headers = needed_headers )
        # req = requests.get("https://www.themoviedb.org/person/52763-aamir-khan")
        doc = BeautifulSoup(response.content, 'html.parser')

        if doc.find("div",id="known_for_scroller") == None:
            all_known_for = []
        else:
            all_known_for = doc.find("div",id="known_for_scroller").find("ul").find_all("li")
        for known_for in all_known_for:
            poster = "https://www.themoviedb.org" + known_for.find("img")['src']
            title = known_for.find("p").text
            dict_['known_for'].append({
                'title' : title,
                'poster' : poster
            })

        list_of_casts.append(dict_)
    return list_of_casts

def get_recommended_movie_details(movie_id):
    api_key = "3222076ed226933d3e1302ce9f3b73dc"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        doc = response.json()

        genres_list = []
        for i in doc['genres']:genres_list.append(i['name'])
        dict_ =  {
            "name" : doc['title'],
            "genres" : genres_list,
            "poster_path" : "https://image.tmdb.org/t/p/original" + doc['poster_path'],
            "release_date" : doc['release_date']
        }
        return dict_
    return None


def get_recommended_movie_cast_detail(movie_id):
    api_key = "3222076ed226933d3e1302ce9f3b73dc"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        doc = response.json()

        list_of_casts = []
        for cast in doc['cast'][:6]:
            dict_ = {
                'name' : cast['name'],
                'character' : cast['character']
            }
            list_of_casts.append(dict_)
        return list_of_casts
    return None

def list_to_str(lst):
    str_ = ""
    for i in lst:
        str_ += i + ", "
    return str_[:-2]

def get_trailler(movie_id):
    # Trailer
    url = f"https://www.themoviedb.org/movie/{movie_id}"
    needed_headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
    response = requests.get(url, headers = needed_headers )
    # req = requests.get("https://www.themoviedb.org/person/52763-aamir-khan")
    doc = BeautifulSoup(response.content, 'html.parser')
    if doc.find_all("a",class_="no_click play_trailer") == []:
        return "https://www.youtube.com/watch?v="
    trailer = "https://www.youtube.com/watch?v=" + doc.find_all("a",class_="no_click play_trailer")[0]['data-id']
    return trailer

def show_recommendations(movie_id):
    dict_= get_recommended_movie_details(movie_id)
    link = "[Trailler]({})".format(get_trailler(movie_id))
    try:
        st.image(dict_['poster_path'])
    except:
        st.image("https://th.bing.com/th/id/OIP.svp_xDT7rtBajr3qbm43JwHaK")
    try:
        st.subheader(dict_['name'])
    except:
        st.subheader("Name not found")
    try:
        st.markdown("**Genres :** " + list_to_str(dict_['genres']))
    except:
        st.markdown("**Genres :** Not Found")
    try:
        st.markdown("**Release Date :** " + dict_['release_date'])
    except:
        st.markdown("**Release Date :** " + "Not Found")
    try:
        st.markdown(link)
    except:
        st.markdown("Error")


def list_to_strURL(dict_,lst):
    ans = ""
    for i in lst:
        ans += str(dict_[i]) + "-"
    return ans[:-1]

def main_page_to_trailer(main_page):
    response = requests.get(main_page)
    if response.status_code != 200:
        return "https://wwww.youtube.com"
    doc = BeautifulSoup(response.content,'html.parser')
    trailer = doc.find(id="iframe-trailer")
    if trailer == None:
        return "https://wwww.youtube.com"
    return trailer['data-src']

def get_card(card):
    poster = card.find(class_="film-poster").find("img")['data-src']
    movie_name = card.find(class_="film-detail film-detail-fix").find("h2").text[:-1]
    runtime = card.find(class_="film-detail film-detail-fix").find("span", class_="fdi-item fdi-duration").text[:-1]
    year = card.find(class_="film-detail film-detail-fix").find("span", class_="fdi-item").text
    main_movie_page = "https://myflixer.to" + card.find(class_="film-poster-ahref flw-item-tip")['href']

    st.image(poster)
    st.markdown(f"<h3>{movie_name}</h3>",unsafe_allow_html=True)
    st.markdown("**Runtime :** " + str(runtime))
    st.markdown(f"**{year}**")
    # if st.button("Trailer of " + f"{movie_name}"):
    #     webbrowser.open_new_tab(main_page_to_trailer(main_movie_page))
    st.write('[Trailer](' + f"{main_page_to_trailer(main_movie_page)})")

def get_total_pages(doc):
    total_page = 0
    try:
        link = doc.find_all("a",class_="page-link")[-1]["href"]
        ind = link.find("page=")
        total_page = int(link[ind+5:])
    except:
        pass
    return total_page


def print_filter_cards_from_pages(url):
    while True:
        indicator = True
        # st.write("Running....")
        try:
            response = requests.get(url, timeout=2)
        except:
            indicator = False
            continue
        if indicator: break

    st.write(url)
    # response = requests.get(url)
    # req = requests.get("https://www.themoviedb.org/person/52763-aamir-khan")
    doc = BeautifulSoup(response.content, 'html.parser')
    # print(doc.prettify())
    cards = doc.find_all(class_="flw-item")
    for i in range(0, len(cards), 4):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if i >= len(cards): break
            get_card(cards[i])
        with col2:
            if i + 1 >= len(cards): break
            get_card(cards[i + 1])
        with col3:
            if i + 2 >= len(cards): break
            get_card(cards[i + 2])
        with col4:
            if i + 3 >= len(cards): break
            get_card(cards[i + 3])
        st.markdown("---")