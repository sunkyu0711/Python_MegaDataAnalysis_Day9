import pandas as pd
import requests
from bs4 import BeautifulSoup
import collections
from konlpy.tag import Okt
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt
import streamlit as st


def Req_Url(url): # 똑같은 코드가 두 개 적혀 있으므로로
    res=requests.get(url).text
    soup=BeautifulSoup(res)

    return soup

def Data_Create():
    url='https://news.naver.com/breakingnews/section/101/259'
    soup=Req_Url(url)
    temp=soup.select_one('ul.sa_list').select('li',limit=5)

    news_list=[]
    for li in temp:
        news_info={'title':li.select_one('strong.sa_text_strong').text,
                'date':li.select_one('div.sa_text_datetime.is_recent').text,
                'news_url':li.select_one('a')['href']}
        news_list.append(news_info)

    for news in news_list:
        news_url=news['news_url']
        soup=Req_Url(news_url)
        body=soup.select_one('article.go_trans._article_content') # 주의: select 함수를 이용할 때에는 공백을 없애야(.으로 메우면 됨)
        news_content=body.text.replace('\n','').strip()
        news['news_content']=news_content

    df=pd.DataFrame(news_list)

    return df

def Text_Visualization(df):
    df=Data_Create()
    s_words=STOPWORDS.union({'있다','이','것'})
    okt=Okt()
    clist=[]
    for word in df['news_content']:
        token=okt.pos(word)
        for word, tag in token:
            if tag in ['Noun','Adjective']:
                clist.append(word)
    counts=collections.Counter(clist)
    tag=counts.most_common(100)

    fpath='C:\Windows\Fonts\malgunbd.ttf'
    wc=WordCloud(font_path=fpath,background_color='white',stopwords=s_words) # 필요 없는 단어 없애기...
    cloud=wc.generate_from_frequencies(dict(tag))

    fig=plt.figure(figsize=(10,8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()
    
    st.pyplot(fig)

if __name__=='__main__':
    df=Data_Create()
    st.dataframe(df)
    Text_Visualization(df)