import random
import json
import pandas as pd
import requests
import streamlit as st
from PIL import Image

main_df = pd.read_csv('main_df.csv', encoding="utf-8")
authorForUrl = ''
titleForUrl = ''
url = ''
bookImgUrl = ''
description = ''

image = Image.open('header.png')
st.image(image)

user_age = st.slider('How old are you?', 16, 90, 36)



def showbook():
    showbooks_df = main_df[main_df['authorPublishedDateAge'] == user_age]
    st.write(user_age)
    random_range = len(showbooks_df) - 1
    random_n = random.randrange(0,random_range,1)
    st.write(random_range)
    st.write(random_n)
    authorForUrl = showbooks_df.iat[random_n, 1]
    titleForUrl = showbooks_df.iat[random_n, 0]
    base_url = 'https://www.googleapis.com/books/v1/volumes?q=in'
    urlaut = 'inauthor:' + authorForUrl
    urltit = 'title:' + titleForUrl
    urlmax = 'maxResults=1'
    printtype = 'printType=books'
    url_list = [urltit, urlaut, urlmax, printtype]
    url = base_url + '&'.join(url_list)
    st.write(url)
    res = requests.get(url).json()  # 情報の取得,json変換
    st.write(res)
    items = res['items']
    st.write(items)
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