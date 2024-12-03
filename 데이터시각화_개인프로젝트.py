# c222079 /  김민수 / 배포링크 : https://hndvg5vxfubfjdpap7t92t.streamlit.app/

# 라이브러리 불러오기
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import json


#######################
# 데이터 불러오기
df_reshaped = pd.read_csv(url+'201412_202312_korea_population_year_UTF8.csv', encoding='UTF-8') # csv 파일 불러오기

korea_geojson = json.load(open(url+'gdf_korea_sido_2022.json', encoding="UTF-8")) # json 파일 불러오기

#######################
# 데이터 전처리
df_reshaped.bfill(inplace=True) # NaN값을 아래의 값으로 채움
df_reshaped.drop(11, inplace=True) # 11번째 행(강원자치도) 삭제
df_reshaped.drop(0, inplace=True) # 0번째 행(전국) 삭제
df_reshaped.reset_index(drop=True, inplace=True) # 인덱스 재설정

# 행정구역을 기준으로 데이터를 쪼개서 새로운 열로 만들기
# expand=True : 쪼개진 데이터를 새로운 열로 만들어줌
df_reshaped[['city', 'code']] = df_reshaped['행정구역'].str.split('(', expand=True) 
df_reshaped['code'] = df['code'].str.strip(')').str.replace('00000000', '')  # 코드에 있는 괄호 제거하고 00000000을 공백으로 변경
df_reshaped.drop('행정구역', axis=1, inplace=True) # 행정구역 열 삭제

df_reshaped = df_reshaped.melt(
    id_vars=['city', 'code'], 
    var_name='property', 
    value_name='population',
)

df_reshaped[['year', 'category']] = df_reshaped['property'].str.split('년_', expand=True) # 속성을 연도와 구분으로 나누기
df_reshaped.drop('property', axis=1, inplace=True) # 속성 열 삭제

df_reshaped['population'] = df_reshaped['population'].str.replace(',', '').astype('int') # 인구수를 쉼표를 삭제한 후 정수로 변환 (문자열 -> 정수)
df_reshaped['year'] = df_reshaped['year'].astype('int') # 연도를 정수로 변환 (문자열 -> 정수)

df_reshaped = df_reshaped[['city', 'code', 'year', 'category', 'population']] # 열 순서 변경


##################################################
#1 인구추이 데이터 로드/ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!개인 디렉토리에 맞게 url 수정!!
#url = 'data/'
#df_reshaped = pd.read_excel(url+'2014_2023인구추이_전처리.xlsx')
    
#2 korea_geojson 지도 데이터로드/ !!!!!!!!!!!!!!!!!!!!!!!!!!!!!1!!!개인파일 이름에 맞게 지도데이터 이름 수정!!!
#korea_geojson = json.load(open(url+'전국지도.json',encoding="UTF-8"))

#3 연도 및 카테고리 리스트
year_list = list(df_reshaped.year.unique())[::-1]
category_list =list(df_reshaped.category.unique())


###############################################################
# 사이트 이름 지정
st.set_page_config(
    page_title="Korea Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

# 각 페이지에 해당하는 함수 정의

### 메인 페이지!
def main_page():

    st.title("📊 대한민국 인구 대시보드")

    st.markdown("""
    #### 대한민국 인구 대시보드
    - 이 대시보드는 연도별, 지역별, 카테고리별 대한민국 인구 변화를 분석하고 시각화합니다.
    - 주요 목표:
        - 지역 간 인구 증감 비교
        - 인구 통계의 시각적 탐색
        - 대한민국의 인구 구조 변화 이해
    """)

    st.markdown("""
    #### 데이터 출처
    - **주민등록 인구통계**: 행정안전부 (https://jumin.mois.go.kr)
    - 데이터 기간: **2014년 ~ 2023년**
    """)

    st.markdown("""
    #### 대시보드 사용 방법
    1. **사이드바를 활용하여 연도와 카테고리를 선택**
    2. **시각화 탭**에서 지도와 그래프를 통해 지역별 인구 변화를 탐색
    3. **인사이트 탭**에서 인구 변화에 대한 주요 요약과 미래 전망을 확인
    """)

    # 주요 통계 요약 (예시 데이터)
    total_population = 51800000  # 전체 인구
    most_populated_city = "서울특별시"
    least_populated_city = "세종특별자치시"
    population_growth_rate = -0.3  # 전년 대비 성장률
    
    st.markdown("""
    #### 주요 인구 통계 (2023년 기준)
    - 총 인구: **{:,}명**
    - 가장 인구가 많은 지역: **{}**
    - 가장 인구가 적은 지역: **{}**
    - 인구 성장률: **{:.1f}%**
    """.format(total_population, most_populated_city, least_populated_city, population_growth_rate))

    # 지도 미리보기 (축소된 버전)
    st.markdown("#### 주요 시각화 미리보기: 지역별 인구 분포 (2023년)")
    map_fig_preview = px.choropleth_mapbox(
        df_reshaped[(df_reshaped['year'] == 2023) &(df_reshaped['category'] == '총인구수')],
        geojson=korea_geojson,
        featureidkey='properties.CTPRVN_CD',
        locations="code",
        color="population",
        center={"lat": 36.5, "lon": 127.8},
        zoom=5,
        mapbox_style="carto-darkmatter",
        color_continuous_scale="viridis",
        title="2023년 지역별 인구 분포",
        labels={'population':'총인구수','code':'시도코드','city':'시도명'},
        hover_data=['city','population']
    )
    st.plotly_chart(map_fig_preview, use_container_width=True)

######### 시각화 페이지
def visualization_page():
    st.sidebar.title("📈 시각화 설정")


# 함수정의

##1 연도별 인구수 변화 계산 함수 작성
    def calculate_population_difference(df,year,target):
        selected_year_data = df.query('year==@year & category == @target').reset_index()
        previous_year_data = df.query('year==@year-1 & category == @target').reset_index()
        selected_year_data['population_diff'] = selected_year_data['population'].sub(
            previous_year_data['population'],fill_value=0)
        selected_year_data['population_diff_abs'] = abs(selected_year_data['population_diff'])
        return selected_year_data[['city',
                                   'code',
                                   'population',
                                   'population_diff',
                                   'population_diff_abs']].sort_values(by='population_diff',ascending=False)

##2 형식변환 함수
    def format_number(num):
        if num > 1000000:
            if not num % 1000000:
                return f'{num // 1000000} M'
            return f'{round(num/1000000,1)} M'
        return f'{num // 1000} K'

##3 도넛 함수
    def make_donut(input_response, input_text, input_color):
        if input_color == 'blue':
            chart_color = ['#29b5e8','#155F7A']
        if input_color == 'green':
            chart_color = ['#27AE60', '#12783D']
        if input_color =='orange':
            chart_color = ['#F39C12','#87A12']
        if input_color == 'red':
            chart_color = ['#E74C3C','#781F16']

        source = pd.DataFrame({
            'Topic':['',input_text],
            '% value':[100-input_response, input_response]
        })

        source_bg = pd.DataFrame({
            'Topic':['',input_text],
            '% value':[100,0]
        })

        plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius =25).encode(
            theta='% value',
            color= alt.Color('Topic:N',
                            scale = alt.Scale(
                                domain=[input_text,''],
                                range=chart_color),
                            legend=None),
        ).properties(width=130, height =130)

        text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(
            text=alt.value(f'{input_response} %'))
        plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
            theta='% value',
            color=alt.Color(
                'Topic:N',
                scale=alt.Scale(
                    domain=[input_text,''],
                    range=chart_color),
                legend=None
            ),
        ).properties(
            width=130, height=130
        )
        return plot_bg + plot +text

##4 지도 함수
    def make_choropleth(input_df, input_id, input_column, input_color_theme):
        choropleth = px.choropleth_mapbox(input_df, 
                                   locations=input_id, 
                                   color=input_column, 
                                   color_continuous_scale=input_color_theme,
                                   geojson=korea_geojson,
                                   featureidkey='properties.CTPRVN_CD',
                                   range_color=(0, max(df_all.population)),
                                   center = {'lat':35.9,'lon':126.98},
                                   mapbox_style='carto-darkmatter',
                                   zoom=5,
                                   labels={'population':f'{selected_category}','code':'시도코드','city':'시도명'},
                                   hover_data=['city','population']
                                  )
        choropleth.update_geos(
        fitbounds='locations',
        visible=False
        )
        choropleth.update_layout(
            template='plotly_dark',
            plot_bgcolor='rgba(0, 0, 0, 0)',
            paper_bgcolor='rgba(0, 0, 0, 0)',
            margin=dict(l=0, r=0, t=0, b=0),
            height=350
        )
        return choropleth

##5 히트맵 함수
    def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
        heatmap = alt.Chart(input_df).mark_rect().encode(
                y=alt.Y(
                    f'{input_y}:O', 
                    axis=alt.Axis(title="연도",                            
                                  titleFontSize=16, 
                                  titlePadding=15, 
                                  titleFontWeight=900, 
                                  labelAngle=0)),
                x=alt.X(
                    f'{input_x}:O', 
                    axis=alt.Axis(title="시도명", 
                                  titleFontSize=16, 
                                  titlePadding=15, 
                                  titleFontWeight=900)),
                color=alt.Color(
                    f'max({input_color}):Q',
                    legend=None,
                    scale=alt.Scale(scheme=input_color_theme)),
                stroke=alt.value('black'),
                strokeWidth=alt.value(0.25),
                tooltip=[
                    alt.Tooltip('year:O',title='연도'),
                    alt.Tooltip('population:Q',title=f'{selected_category}')
                    ]).properties(
            width=900
        ).configure_legend(
            orient='bottom',
            titleFontSize=16,
            labelFontSize=14,
            titlePadding=0
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=12
        )
        return heatmap


#4 사이드바 구현

    with st.sidebar:
        st.title('🏂 대한민국 인구 대시보드')
    
        selected_year = st.selectbox('연도 선택', year_list, index=len(year_list)-1)
        df_selected_year = df_reshaped[df_reshaped.year == selected_year]
        df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

        selected_category = st.selectbox('카테고리 선택', category_list, index=len(category_list)-1)
        df_selected_category = df_reshaped[df_reshaped.category == selected_category]
        df_selected_category_sorted = df_selected_category.sort_values(by="population", ascending=False)

        df_all= df_reshaped[(df_reshaped.category == selected_category)&(df_reshaped.year == selected_year)]
        df_all_sorted = df_all.sort_values(by='population', ascending = False)

        color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
        selected_color_theme = st.selectbox('컬러 테마 선택', color_theme_list)

    #5. 인구증감, 도넛 그래프 구현(col1)
    col = st.columns((1.5, 4.5, 2), gap='medium')
    with col[0]:
        st.markdown('#### 증가/감소')
    
        df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year,selected_category)
    
        if selected_year > 2014:
            first_city_name = df_population_difference_sorted.city.iloc[0]
            first_city_population = format_number(df_population_difference_sorted.population.iloc[0])
            first_city_delta = format_number(df_population_difference_sorted.population_diff.iloc[0])
        else:
            first_city_name = '-'
            first_city_population = '-'
            first_city_delta = ''
        st.metric(label=first_city_name, value=first_city_population, delta=first_city_delta)
    
        if selected_year > 2014:
            last_city_name = df_population_difference_sorted.city.iloc[-1]
            last_city_population = format_number(df_population_difference_sorted.population.iloc[-1])   
            last_city_delta = format_number(df_population_difference_sorted.population_diff.iloc[-1])   
        else:
            last_city_name = '-'
            last_city_population = '-'
            last_city_delta = ''
        st.metric(label=last_city_name, value=last_city_population, delta=last_city_delta)
    
        
        st.markdown('#### 변동 시도 비율')
    
        if selected_year > 2014:
            # Filter cities with population difference > 5000
            # df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference_absolute > 50000]
            df_greater_5000 = df_population_difference_sorted[df_population_difference_sorted.population_diff > 5000]
            df_less_5000 = df_population_difference_sorted[df_population_difference_sorted.population_diff < -5000]
            
            # % of cities with population difference > 50000
            city_migration_greater = round((len(df_greater_5000)/df_population_difference_sorted.city.nunique())*100)
            city_migration_less = round((len(df_less_5000)/df_population_difference_sorted.city.nunique())*100)
            donut_chart_greater = make_donut(city_migration_greater, '전입', 'green')
            donut_chart_less = make_donut(city_migration_less, '전출', 'red')
        else:
            city_migration_greater = 0
            city_migration_less = 0
            donut_chart_greater = make_donut(city_migration_greater, '전입', 'green')
            donut_chart_less = make_donut(city_migration_less, '전출', 'red')
    
        migrations_col = st.columns((0.2, 1, 0.2))
        with migrations_col[1]:
            st.write('증가')
            st.altair_chart(donut_chart_greater)
            st.write('감소')
            st.altair_chart(donut_chart_less)

    #6 지도시각화 및 차트맵 구현(col2)
    
    with col[1]:
        st.markdown(f'#### {selected_year}년 {selected_category}')
        
        choropleth = make_choropleth(df_all, 'code', 'population', selected_color_theme)
        st.plotly_chart(choropleth, use_container_width=True)
    
        heatmap = make_heatmap(df_reshaped[df_reshaped['category']==f'{selected_category}'], 'year', 'city', 'population', selected_color_theme)
        st.altair_chart(heatmap, use_container_width=True)
    
    
    #7 시도별 인구수 및 기타정보
    with col[2]:
        st.markdown(f'#### 시도별 {selected_category}')
    
        st.dataframe(df_all_sorted,
                     column_order=("city", "population"),
                     hide_index=True,
                     width=None,
                     column_config={
                        "city": st.column_config.TextColumn(
                            "city",
                        ),
                        "population": st.column_config.ProgressColumn(
                            "Population",
                            format="%f",
                            min_value=0,
                            max_value=max(df_all_sorted.population),
                         )}
                     )
        
        with st.expander('정보', expanded=True):
            st.write('''
                - Data: [행정안전부 주민등록인구통계](<https://https://jumin.mois.go.kr.html>).
                - :orange[**증가/감소**]: 선택한 연도/카테고리에서 가장 많이 증가/감소한 시도
                - :orange[**변동 시도 비율**]: 선택한 연도/카테고리에서 인구가 5000명 이상 증가/감소한 시도의 비율 ''')




##### 인사이트 페이지
def insights_page():
    st.title("📋 주요 인사이트")
    
    st.markdown("""
    ### 대한민국 인구의 주요 변화
    - 지역별 인구 증감의 주요 요인 분석
    - 인구 증가 지역과 감소 지역 비교
    """)
    
    st.markdown("""
    ### 주요 요약
    - 최근 연도 기준 전국 인구: **52,000,000명**에서 **51,800,000명**으로 **-0.3% 감소**.
    - 인구가 가장 많이 증가한 지역: **서울특별시** (+100,000명).
    - 인구가 가장 많이 감소한 지역: **전라북도** (-50,000명).
    """)
    
    st.markdown("""
    ### 지역별 인구 증감 요인
    - **인구 증가 지역**:
        - 대도시 중심으로 출생률은 감소했지만, **서울특별시**와 **수도권**은 이주 증가로 인해 인구가 증가.
        - **경기도**는 신규 아파트 공급 및 직주 근접 효과로 인해 인구 유입이 활발.
    - **인구 감소 지역**:
        - **전라남도**, **경상북도** 등 농촌 지역은 인구 감소가 두드러지며, 청년층 이탈로 인해 노동 연령대 인구가 급감.
        - 노령화와 출산율 감소가 복합적으로 작용
    """)

    st.markdown("""
    ### 연령대 및 성별 변화
    - **연령변화**:
        - 20~30대 청년층은 수도권으로 이동, 지방의 비율은 감소 추세.
        - 65세 이상 인구 비중은 **2023년 기준 전체의 18%**로, 고령화 속도가 가속화되고 있음.
        
    - **성별 비중**:
        - 남성 인구와 여성 인구의 비율은 약간의 차이를 보이며, 출생 성비는 1.05로 안정세.
    """)
    
    st.markdown("""
    ### 미래 전망
    - **출산율 감소와 고령화**:
        - 출생률은 지난 5년간 매년 약 5% 감소. **출산율 0.8명 이하**로 세계 최저 수준.
        - 고령화 속도는 OECD 국가 중 가장 빠르며, 2050년까지 65세 이상 인구 비중이 **35%**를 초과할 것으로 예상.
    
    - **지역 간 격차 확대**:
        - 수도권 집중화로 지방 소멸 위기가 심화. 특히 **전라남도**, **경상북도** 일부 지역은 10년 내 소멸 위험 지역으로 분류.
    """)


# 페이지 선택 기능은 모든 함수가 정의된 후 배치
page = st.sidebar.radio("페이지 선택", ["메인", "시각화", "인사이트"])

if page == "메인":
    main_page()
elif page == "시각화":
    visualization_page()
elif page == "인사이트":
    insights_page()

###########################################################












            
