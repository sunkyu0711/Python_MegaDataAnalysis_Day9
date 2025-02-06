import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import folium
from folium.plugins import MarkerCluster
import seaborn as sns
import matplotlib.pyplot as plt

@st.cache_data

def DataPreprocessing():
    bikes_temp={}

    for i in range(1,4):
        bikes_temp[i]=pd.read_csv(f'C:/Users/sunky/OneDrive/바탕 화면/Programming/Python_MegaDataAnalysis_Day9/bike/files/서울특별시 공공자전거 대여이력 정보_240{i}.csv',encoding='cp949') # 서울 열린데이터광장에서 검색색

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
    bike_shop=pd.read_csv('C:/Users/sunky/OneDrive/바탕 화면/Programming/Python_MegaDataAnalysis_Day9/bike/files/공공자전거 대여소 정보.csv',encoding='cp949')
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

def Time_Analysis(bikes):
    plt.rc('font',family='Malgun Gothic')

    hourly_ride=bikes.groupby('대여시간대',as_index=False)[['자전거번호']].count().rename(columns={'자전거번호':'이용건수'})
    weekday_ride=bikes.groupby('대여요일',as_index=False)[['자전거번호']].count().rename(columns={'자전거번호':'이용건수'})

    fig,axes=plt.subplots(2,1,figsize=(7,14))

    sns.barplot(data=hourly_ride,x='대여시간대',y='이용건수',ax=axes[0])
    axes[0].set_title('2024년 1분기 시간대별 서울특별시 자전거 대여 현황')

    sns.barplot(data=weekday_ride,x='대여요일',y='이용건수',ax=axes[1])
    axes[1].set_title('2024년 1분기 요일별 서울특별시 자전거 대여 현황')

    st.pyplot(fig) # streamlit이라서... plt.show()는 없애기

# 여기는 10일 차
def Bike_Main():
    tab1,tab2,tab3=st.tabs(["데이터 보기","인기 대여소 TOP 50","2024년 1분기 분석"])

    with tab1:
        data=DataPreprocessing()
        st.dataframe(data.head(20))
    with tab2:
        Top50(data)
    with tab3:
        Time_Analysis(data)

if __name__=='__main__':
    Bike_Main()
    