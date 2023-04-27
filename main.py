import streamlit as st
from PIL import Image
import requests
import pandas as pd
import json
import random

main_df = pd.read_csv('main_df.csv', encoding="utf-8")
authorForUrl = '小川洋子'
titleForUrl = '密やかな結晶'
url = ''
bookImgUrl = ''
random_n = 1
description = ''

image = Image.open('header.png')
st.image(image)

user_age = st.slider('How old are you?', 16, 90, 33)



def showbook():
    showbooks_df = main_df[main_df['authorPublishedDateAge'] == user_age]
    random_range = len(showbooks_df) - 1
    random_n = random.randrange(0,random_range,1)
    print(random_range)
    print(random_n)
    authorForUrl = showbooks_df.iat[random_n, 1]
    titleForUrl = showbooks_df.iat[random_n, 0]
    base_url = 'https://www.googleapis.com/books/v1/volumes?q=in'
    urlaut = 'inauthor:' + authorForUrl
    urltit = 'title:' + titleForUrl
    urlmax = 'maxResults=1'
    printtype = 'printType=books'
    url_list = [urltit, urlaut, urlmax, printtype]
    url = base_url + '&'.join(url_list)
    res = requests.get(url).json()  # 情報の取得,json変換
    items = res['items']
    description = items[0]['volumeInfo'].get('description')
    bookImgUrl = items[0]['volumeInfo']['imageLinks'].get('thumbnail')

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('タイトル : ')
        st.title('『' + showbooks_df.iat[random_n, 0] + '』')
        st.markdown('著者 :')
        st.header(showbooks_df.iat[random_n, 1])
        st.markdown('(本出版当時、' + str(user_age) + '才)')
    with col2:

        st.image(bookImgUrl, use_column_width=True)
    st.markdown(description)
    st.text('※著者年齢はだいたいです、本が出版された年から誕生年を引いています')


def url_gen():
    base_url = 'https://www.googleapis.com/books/v1/volumes?q=in'
    urlaut = 'inauthor:' + authorForUrl
    urltit = 'title:' + titleForUrl
    urlmax = 'maxResults=1'
    printtype = 'printType=books'

    url_list = [urltit, urlaut,urlmax, printtype]
    url = base_url + '&'.join(url_list)
    return url


def fetch_info():
    res = requests.get(url).json()  # 情報の取得,json変換
    items = res['items']
    description = items[0]['volumeInfo'].get('description')
    bookImgUrl = items[0]['volumeInfo']['imageLinks'].get('thumbnail')
    return description, bookImgUrl


recommend = st.button('占う')
if recommend:
    showbook()
else:
    st.write('Waiting...')