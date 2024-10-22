import streamlit as st

st.header(':blue[사용자입력]')

st.write('#### :orange[_텍스트 입력_]')

text = st.text_input('여기에 텍스트입력')
st.write(f'입력된 텍스트:{text}')

text= st.text_input('여기에 텍스트입력2')
st.write(f'입력된 텍스트:{text}')


#숫자 입력은 입력된 값을 변환

st.write('#### :orange[숫자 입력]')
number = st.number_input('여기에 숫자를 입력하세요')
st.write(f'입력된 숫자:{number}')

#날짜 입력은 입력된 값을 반환
st.write('#### :orange[날짜 입력]')
date = st.date_input('날짜를 선택하세요')
st.write(f'선택된 날짜: {date}')

#시간 입력은 입력된 값을 반환
st.write('#### :orange[시간입력]')
time = st.time_input('시간을 선택하세요', help='weee',step =600)
st.write(f'선택된 시간:{time}')

# 파일 업로드는 업로드된 파일을 반환
st.write('#### :orange[파일업로드]')
file = st.file_uploader('파일을 업로드하세요')
if file:
  st.write(f'업로드된 파일: {file}')

#체크박스, 라디오 버튼, 셀렉트 박스, 멀티 셀렉트 박스 ================
st.header(' :blue[체크박스, 라디오 버튼, 셀렉트 박스, 멀티 셀렉트 박스]')

#체크박스는 True/False 값을 반환
st.write('#### :orange[체크박스]')
check = st.checkbox('여기를 체크하세요')
if check:
  st.write('#### :orange[체크 박스]')
