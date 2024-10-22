import streamlit as st

st.header(':blue[사용자입력]')

st.write('#### :orange[_텍스트 입력_]')

text = st.text_input('여기에 텍스트입력')
st.write(f'입력된 텍스트:(text)')

text= st.text_input('여기에 텍스트입력2')
st.write(f'입력된 텍스트:(text)')
