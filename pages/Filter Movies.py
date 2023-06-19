import streamlit as st
from filter_functions import get_all_genres_pages_link, get_language_by_values, get_country_code, get_all_page_last_part,get_soup, show_card
import datetime

genres_multiselect_button = st.multiselect(label="Select Genre",options=list(get_all_genres_pages_link().keys()),default='History')

selected_url = ""
for genre in genres_multiselect_button:
    selected_url += genre.lower() + ","
selected_url = selected_url[:-1]

url = f"https://www.imdb.com/search/title/?genres={selected_url}"

start_date = st.date_input("From :",min_value=datetime.date(1901,1,1),max_value=datetime.date.today())
end_date = st.date_input("To :",min_value=datetime.date(1901,1,1),max_value=datetime.date.today())

url += "&release_date=" + str(start_date) + "," + str(end_date)

# minimum_rating_slider = st.slider(label="Select Minimum Rating : ",value=8.5,step=0.1,min_value=0.0,max_value=10.0)
#
# url += "&user_rating=" + str(minimum_rating_slider)

get_language_by_values_dict = get_language_by_values()

language_multiselect = st.multiselect(label="Select Language : ",options=list(get_language_by_values_dict.keys()),max_selections=1,default='Bengali')

url += "&languages=" + get_language_by_values_dict[language_multiselect[0]]

country_code_dict = get_country_code()
country_multiselect = st.multiselect(label="Select Country : ", options=list(country_code_dict.keys()),max_selections=1,default="India")

url += "&countries=" + country_code_dict[country_multiselect[0]]



try:
    last_part_dict = get_all_page_last_part(url=url)
    recent_page = st.multiselect(label="Select Page",options=last_part_dict.keys(),default=list(last_part_dict.keys())[0],max_selections=1)
    url += f"&start={last_part_dict[recent_page[0]]}&ref_=adv_nxt"

    soup = get_soup(url)
    cards = soup.find_all("div",class_="lister-item mode-advanced")
    for card in cards:
        show_card(card)

except:
    st.write("No results found")