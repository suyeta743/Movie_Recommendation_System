import streamlit as st
import pickle
import requests
from bs4 import BeautifulSoup
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import ToktokTokenizer
from nltk.corpus import stopwords

imdb_id = "tt0113497"
try:
    imdb_id = st.session_state.imdb_id
except:
    pass


def remove_html_and_noise(doc):
    doc = BeautifulSoup(doc,'html.parser')
    doc = doc.get_text()
    doc = re.sub('\[[^]]*\]', '', doc+"[a]") #removing the square
    return doc
# lister_items[i].find_all("div",class_="text show-more__control")[0].text
def removing_special_character(doc): #without space as special character
    doc = re.sub(r"[^A-Za-z0-9\s]",'',doc)
    return doc

def simple_potter_stemmer(doc):
    ps = PorterStemmer()
    return ' '.join([ps.stem(word) for word in doc.split()])

def removing_stop_words(doc):
    tokenizer = ToktokTokenizer()
    stop_words = set(stopwords.words('english'))
    stop_words_list = list(stop_words)
    tokens = tokenizer.tokenize(doc)

    tokens = [token.strip() for token in tokens] #token.strip is rem=moving extra space

    tokens = [token for token in tokens if token not in stop_words_list]

    return ' '.join(tokens)

cv = pickle.load(open("data/cv.pkl", "rb"))
lr_bow = pickle.load(open("data/lr_bow.pkl","rb"))

# print(st.session_state.imdb_id)

url = f"https://www.imdb.com/title/{imdb_id}/reviews"
response = requests.get(url)
doc = BeautifulSoup(response.content,'html.parser')
cards = doc.find_all(class_="imdb-user-review")
# print(len(cards))
for review_card in cards:
    title = review_card.find("a",class_="title").text
    content = review_card.find(class_="content").find(class_="text").text

    review = title + content
    review = remove_html_and_noise(review)
    review = removing_stop_words(review)
    review = simple_potter_stemmer(review)

    tranformerd_review = cv.transform([review]) #number representations
    predicted = lr_bow.predict(tranformerd_review)[0]
    if predicted == 'positive':
        st.markdown("<h3 style='color:green'>" + "Positive ✅😍: " + title + "</h3>",unsafe_allow_html=True)
        st.write(content)
    else:
        st.markdown("<h3 style='color:red'>" + "Negative ❌😞: " + title + "</h3>",unsafe_allow_html=True)
        st.write(content)

