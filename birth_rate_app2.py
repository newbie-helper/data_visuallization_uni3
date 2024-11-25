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


### 경기도 데이터 전처리
gdf_Gyeonggi = gpd.read_file('data/경기도지도.json')
gdf_Gyeonggi['행정구'] = df_Gyeonggi['SGG_NM'].str.replace('경기도 ','')
gdf_Gyeonggi['행정구'] = (df_Gyeonggi['행정구']
                      .str.replace('수원시 ','')
                      .str.replace('성남시 ','')
                      .str.replace('안양시 ','')
                      .str.replace('안산시 ','')
                      .str.replace('고양시 ','')
                      .str.replace('용인시 ','')
                      .str.replace(' 원미구','')
                      .str.replace(' 소사구','')
                      .str.replace(' 오정구',''))

### 인천 지도 데이터 전처리
gdf_incheon = gpd.read_file('data/인천지도.json')
gdf_incheon['행정구'] = gdf_incheon['SGG_NM'].str.replace('인천광역시 ','')
gdf_incheon['행정구'] = gdf_incheon['행정구'].str.replace('중구','인천-중구')
gdf_incheon['행정구'] = gdf_incheon['행정구'].str.replace(r'^동구$','인천-동구') # ^동구$ (^: 문자열의 시작. | 동구: 정확히 "동구".|$: 문자열의 끝.)
gdf_incheon['행정구'] = gdf_incheon['행정구'].str.replace('서구','인천-서구')

### 강원도 지도 데이터 전처리
gdf_Gangwon = gpd.read_file('data/강원도지도.json')
gdf_Gangwon['행정구'] = gdf_Gangwon['SGG_NM'].str.replace('강원특별자치도 ','')


### 충북 지도 데이터전처리
gdf_chungbuk = gpd.read_file('data/충북지도.json')
gdf_chungbuk['행정구'] = (gdf_chungbuk['SGG_NM']
                       .str.replace('충청북도 ','')
                       .str.replace(' 상당구','')
                       .str.replace(' 서원구','')
                       .str.replace(' 흥덕구','')
                       .str.replace(' 청원구',''))

### 충남 지도 데이터 전처리
gdf_chungnam = gpd.read_file('data/충남지도.json')
gdf_chungnam['행정구'] = (gdf_chungnam['SGG_NM']
                       .str.replace('충청남도 ','')
                       .str.replace('천안시 동남구|천안시 서북구', '천안시',regex=True)
                      )

### 대전 지도 데이터 전처리
gdf_Daejeon = gpd.read_file('data/대전지도.json')
gdf_Daejeon['행정구'] = (gdf_Daejeon['SGG_NM']
                      .str.replace('대전광역시 ','')
                      .str.replace('동구','대전-동구')
                     .str.replace('중구','대전-중구')
                     .str.replace('서구','대전-서구'))


### 세종 지도 데이터 전처리
gdf_sejong = gpd.read_file('data/세종지도.json')
gdf_sejong['행정구'] =gdf_sejong['SGG_NM']

### 전북 지도 데이터 전처리
gdf_Jeonbuk = gpd.read_file('data/전북지도.json')
gdf_Jeonbuk['행정구'] = (gdf_Jeonbuk['SGG_NM']
                      .str.replace('전북특별자치도 ','')
                      .str.replace('전주시 완산구|전주시 덕진구','전주시',regex=True)) 

### 전남 지도 데이터 전처리
gdf_Jeonnam = gpd.read_file('data/전남지도.json')
gdf_Jeonnam['행정구'] = gdf_Jeonnam['SGG_NM'].str.replace('전라남도 ','')


### 광주 지도 데이터 전처리
gdf_Gwangju = gpd.read_file('data/광주지도.json')
gdf_Gwangju['행정구'] = (gdf_Gwangju['SGG_NM']
                      .str.replace('광주광역시 ','')
                      .str.replace('동구','광주-동구')
                      .str.replace('서구','광주-서구')
                      .str.replace('남구','광주-남구')
                      .str.replace('북구','광주-북구'))

### 경북 지도 데이터 전처리
gdf_Gyeongsangbuk = gpd.read_file('data/경북지도.json')
gdf_Gyeongsangbuk['행정구'] = (gdf_Gyeongsangbuk['SGG_NM']
                            .str.replace('경상북도 ','')
                            .str.replace('포항시 남구','포항-남구')
                            .str.replace('포항시 북구','포항-북구'))


### 대구 지도 데이터 전처리
gdf_daegu = gpd.read_file('data/대구지도.json')
gdf_daegu['행정구'] = (gdf_daegu['SGG_NM']
                    .str.replace('대구광역시 ','')
                    .str.replace('중구','대구-중구')
                    .str.replace('동구','대구-동구')
                    .str.replace(r'^서구$','대구-서구',regex=True)
                    .str.replace('남구','대구-남구')
                    .str.replace('북구','대구-북구'))

### 경남 지도 데이터 전처리
gdf_Gyeongnam = gpd.read_file('data/경남지도.json')
gdf_Gyeongnam['행정구'] = (gdf_Gyeongnam['SGG_NM']
                        .str.replace('경상남도 ','')
                        .str.replace('창원시 ',''))

### 울산 지도 데이터 전처리
gdf_Ulsan = gpd.read_file('data/울산지도.json')
gdf_Ulsan['행정구'] = (gdf_Ulsan['SGG_NM'].str.replace('울산광역시 ','')
                    .str.replace('중구','울산-중구')
                    .str.replace('남구','울산-남구')
                    .str.replace('동구','울산-동구')
                    .str.replace('북구','울산-북구'))

### 부산 지도 데이터 전처리
gdf_busan = gpd.read_file('data/부산지도.json')
gdf_busan['행정구'] = (gdf_busan['SGG_NM']
                    .str.replace('부산광역시 ','')
                    .str.replace('중구','부산-중구')
                    .str.replace('강서','부산-강서'))











# Streamlit 앱 제목
st.title("시군구 기준 합계출산율 Choropleth 지도")

# 지도 중심 설정
center = [36.7335, 127.16609]
title = "전국 출산율 지도"

# GeoJSON 파일 통합
geojson_combined = {
    "type": "FeatureCollection",
    "features": (
        gdf_seoul_gu.__geo_interface__["features"] +
        gdf_Gyeonggi.__geo_interface__["features"] +
        gdf_incheon.__geo_interface__["features"] +
        gdf_Gangwon.__geo_interface__["features"] +
        gdf_chungbuk.__geo_interface__["features"]+
        gdf_chungnam.__geo_interface__["features"]+
        gdf_Daejeon.__geo_interface__["features"]+
        gdf_sejong.__geo_interface__["features"]+
        gdf_Jeonbuk.__geo_interface__["features"]+
        gdf_Jeonnam.__geo_interface__["features"]+
        gdf_Gwangju.__geo_interface__["features"]+
        gdf_Gyeongsangbuk.__geo_interface__["features"]+
        gdf_daegu.__geo_interface__["features"]+
        gdf_Gyeongnam.__geo_interface__["features"]+
        gdf_Ulsan.__geo_interface__["features"]+
        gdf_busan.__geo_interface__["features"]
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
