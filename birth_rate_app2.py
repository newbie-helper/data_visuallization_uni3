import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# 출생율 데이터 전처리
import pandas as pd # pandas 라이브러리 불러오기
df_birth_rate = pd.read_excel('data/행정구역별출산율.xlsx',header=1)
df_birth_rate.columns = ['행정구','출산율'] # 컬럼명 변경
# 출생율 데이터 공백제거
df_birth_rate['행정구'] = df_birth_rate['행정구'].str.replace('\u3000', '', regex=False)

### 서울지도 데이터 전처리
import geopandas as gpd 
# geopandas 라이브러리 불러오기
# geopandas의 read_file 함수로 데이터 불러오기
gdf_seoul_gu = gpd.read_file('data/서울지도.json')
gdf_seoul_gu['행정구'] = gdf_seoul_gu['SGG_NM'].str.replace('서울특별시 ','') 

# Streamlit 앱 제목
st.title("시군구 기준 합계출산율 Choropleth 지도")

# 지도 중심 설정
center = [36.7335, 127.16609]
title = "전국 출산율 지도"

# GeoJSON 파일 통합
geojson_combined = {
    "type": "FeatureCollection",
    "features": (
        gdf_seoul_gu.__geo_interface__["features"] 
    )
}

# Folium 지도 생성
korea_map = folium.Map(location=center, zoom_start=7, tiles="cartodbpositron")

folium.Choropleth(
    geo_data=geojson_combined,
    data=df_birth_rate,
    columns=("행정구", "출산율"),
    key_on="feature.properties.행정구",
    fill_color="BuPu",
    fill_opacity=0.7,
    line_opacity=0.5,
    legend_name="합계출산율"
).add_to(korea_map)

# Streamlit을 통해 Folium 지도 렌더링
st_folium(korea_map, width=800, height=600)

# 설명 추가
st.markdown("""
### 지도 설명
- 이 지도는 전국 시군구의 합계출산율을 색상으로 시각화한 Choropleth 지도입니다.
- 시군구별 출산율은 데이터 기반으로 색상이 다르게 표시됩니다.
- 데이터를 바탕으로 지역별 출산율 비교가 가능합니다.
""")
