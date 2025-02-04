import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.plugins import MarkerCluster

@st.cache_data

def DataPreprocessing():
    bikes_temp={}

    for i in range(1,4):
        bikes_temp[i]=pd.read_csv(f'files\서울특별시 공공자전거 대여이력 정보_240{i}.csv',encoding='cp949')

    bikes=pd.concat(bikes_temp,ignore_index=True)

    bikes['대여일']=pd.to_datetime(bikes['대여일시'])
    bikes['대여월']=bikes['대여일'].dt.month
    bikes['대여일자']=bikes['대여일'].dt.day
    bikes['대여시간대']=bikes['대여일'].dt.hour

    weekdays={0:'월',
              1:'화',
              2:'수',
              3:'목',
              4:'금',
              5:'토',
              6:'일'}
    bikes['대여요일']=bikes['대여일'].dt.weekday.map(weekdays)

    bikes['대여요일 주말구분']=bikes['대여일'].dt.weekday.map(lambda x: '평일' if x<5 else '주말')

    return bikes

def Top50(bikes):
    bikes_weekend=bikes.groupby(['대여 대여소번호','대여 대여소명','대여요일 주말구분'])['자전거번호'].count().unstack()
    weekend50=bikes_weekend.sort_values('주말',ascending=False).head(50).reset_index()
    bike_shop=pd.read_csv('files\공공자전거 대여소 정보.csv',encoding='cp949')
    weekend50_total=pd.merge(weekend50,bike_shop,left_on='대여 대여소번호',right_on='대여소번호')

    map=folium.Map(location=[weekend50_total['위도'].mean(),weekend50_total['경도'].mean()],
               zoom_start=12,width=1000,height=700)
    
    marker_c=MarkerCluster().add_to(map)

    for i in weekend50_total.index:
        sub_lat=weekend50_total.loc[i,'위도']
        sub_lon=weekend50_total.loc[i,'경도']
        sub_name=weekend50_total.loc[i,'대여 대여소명']

        shop=[sub_lat,sub_lon]

        folium.Marker(location=shop,popup=sub_name,icon=folium.Icon(color='red',icon='star')).add_to(marker_c)
    
    components.html(map._repr_html_(),width=1000,height=700) # 위치를 가운데로 맞추고 싶은데?

if __name__=='__main__':
    data=DataPreprocessing()
    st.dataframe(data.head(20))
    Top50(data)
    