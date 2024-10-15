import streamlit as st
st.header('🤖 텍스트 출력')
st.write('') #빈 줄 삽입

st.write('# 마크다운 H1: st.write()')
st.write('### 마크다운 H3: st.write()')
st.write('')

st.title('제목 : st.title()')
st.header('헤더 : st.header()')
st.subheader('서브헤더: st.subheader')
st.text('본문 테그트: st.text()')
st.write('')

st.markdown('## 마크다운 : st.markdown()')
st.markdown('''
            1.ordered item
                - unordered item
                - unordered item
            2. odered item
            3. ordered item
            ''')
st.divider() # 구분선

# 사이드바 추가!--------------------------
st.header('---- 사이드바')
st.sidebar.write('## 사이드바 텍스트')
st.sidebar.checkbox('체크박스1')
st.sidebar.checkbox('체크박스2')
st.sidebar.radio('라디오 버튼', ['radio 1', 'radio 2', 'radio 3'])
st.sidebar.selectbox('셀렉트 박스', ['select 1', 'select 2', 'select 3'])

