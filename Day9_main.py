import streamlit as st
import Day9_bikes
import Day10_navernews

# 사이드 바 화면
st.sidebar.title('사이드 바') # 쓸모가 없어 보이는데?
user_id=st.sidebar.text_input('아이디',value='') # value: 초기 값, max_chars: 최대 글자 수
user_pw=st.sidebar.text_input('비밀번호',value='',type='password')
# type=password - 비번이 별표로 표시되어 입력되게끔

if user_pw=='1234': # 회원 가입 기능도 만들고 싶은데...
    st.sidebar.header('나의 포트폴리오')
    select_data=['메뉴를 선택하세요.','따릉이 분석','실시간 금융 뉴스']
    menu=st.sidebar.selectbox('',select_data,index=0) # index=0: 아무것도 선택되지 않게끔

    if menu=='따릉이 분석':
        st.write('따릉이 분석')
        Day9_bikes.Bike_Main()
    elif menu=='실시간 금융 뉴스':
        st.write('실시간 금융 뉴스')
        df=Day10_navernews.Data_Create()
        st.dataframe(df)
        Day10_navernews.Text_Visualization(df)
    else:
        st.title('환영합니다.')

# 실행: 터미널 켜고 "streamlit run 9일차_main.py" 입력 후 엔터
# 최초 엔터에는 이메일 입력하라고 뜨는데 그냥 엔터 때리기
# 터미널 닫기 금지. 닫으면 다시 실행해야