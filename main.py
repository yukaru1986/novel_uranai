import random
import json
import pandas as pd
import requests
import streamlit as st
from PIL import Image

APP_ID = 1054605449854620144
req_url = 'https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404'

main_df = pd.read_csv('main_df.csv', encoding="utf-8")
authorForUrl = ''
titleForUrl = ''
url = ''
bookImgUrl = ''
description = ''

image = Image.open('header.jpg')
st.image(image)
user_name = st.text_input("お名前は？ニックネームでも。","それがし なにがし")
user_age = st.slider('何才でしょうか?', 7, 77, 36)
st.divider()


def showbook():
    uranai_age = user_age // 7 * 3 + 17
    showbooks_df = main_df[(main_df['authorPublishedDateAge'] >= uranai_age - 5) & (main_df['authorPublishedDateAge'] <= uranai_age + 5)]
    random_range = len(showbooks_df) - 1
    random_n = random.randrange(0,random_range,1)
    authorForUrl = showbooks_df.iat[random_n, 1]
    titleForUrl = showbooks_df.iat[random_n, 0]
    params = {
        'format': 'json',
        'title': titleForUrl,
        'author': authorForUrl,
        'hits': 1,
        'applicationId': APP_ID
    }
    res = requests.get(req_url, params).json() # 情報の取得,json変換
    try:
        description = res['Items'][0]['Item'].get('itemCaption')
        bookImgUrl = res['Items'][0]['Item'].get('largeImageUrl')
    except Exception:
        pass

    st.markdown("幸運の小説。それは、読者に深い共感と感動をもたらし、人生を変える可能性さえあるもの。この小説が"+ user_name + "さんにとって幸運の小説であるかもしれません。あなたの人生にとって特別な意味を持ち、読むたびにその価値を再確認できるような小説との出会いを願っております…")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown('タイトル : ')
        st.title('『' + showbooks_df.iat[random_n, 0] + '』')
        st.markdown('出版時期:'+showbooks_df.iat[random_n, 2][:7])
        st.markdown('著者 :')
        st.header(showbooks_df.iat[random_n, 1])
        st.markdown('(本出版当時、' + str(int(showbooks_df.iat[random_n, 4])) + '才くらい)')

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
st.divider()
