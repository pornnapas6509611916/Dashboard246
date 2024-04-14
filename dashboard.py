# -*- coding: utf-8 -*-
"""Dashboard.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1HywERjiYqxQw4Nvqt2hVauo4z_z0kfLW
"""

import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="🪸Dashboard",
    page_icon="🪸",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

# import google form  data by csv
url_form = 'https://drive.google.com/file/d/1h_df5XgkOOcO__7f5fq7gSjqtsFXFJ8v/view?usp=drive_link' #csv link
file_id_form = url_form.split('/')[-2]
dwn_url_form = 'https://drive.google.com/uc?id=' + file_id_form
df = pd.read_csv(dwn_url_form)

df = df.rename(columns={' [ด้านการเดินทางและความปลอดภัย]': 'ด้านการเดินทางและความปลอดภัย',
                         ' [ด้านการศึกษา]': 'ด้านการศึกษา',
                         ' [ด้านสุขภาพ]': 'ด้านสุขภาพ',
                         ' [ด้านสิ่งแวดล้อม]': 'ด้านสิ่งแวดล้อม'})



counts_5 = []
counts_4 = []
counts_3 = []
counts_2 = []
counts_1 = []

for category_column in ['ด้านการเดินทางและความปลอดภัย', 'ด้านการศึกษา', 'ด้านสุขภาพ', 'ด้านสิ่งแวดล้อม']:
    counts_5.append(df[category_column].value_counts().get(5, 0))
    counts_4.append(df[category_column].value_counts().get(4, 0))
    counts_3.append(df[category_column].value_counts().get(3, 0))
    counts_2.append(df[category_column].value_counts().get(2, 0))
    counts_1.append(df[category_column].value_counts().get(1, 0))

mean = df[['ด้านการเดินทางและความปลอดภัย', 'ด้านการศึกษา', 'ด้านสุขภาพ', 'ด้านสิ่งแวดล้อม']].mean().round(2)
mean_data = {
    'Categories': ['ด้านการเดินทางและความปลอดภัย', 'ด้านการศึกษา', 'ด้านสุขภาพ', 'ด้านสิ่งแวดล้อม'],
    'Mean': mean
}
df_mean = pd.DataFrame(mean_data)

data = {
    'Categories': ['การเดินทางและความปลอดภัย', 'การศึกษา', 'สุขภาพ', 'สิ่งแวดล้อม'],
    'Satisfaction_5': counts_5,
    'Satisfaction_4': counts_4,
    'Satisfaction_3': counts_3,
    'Satisfaction_2': counts_2,
    'Satisfaction_1': counts_1
}


# สร้าง DataFrame
df = pd.DataFrame(data)

# ใช้ pd.melt() เพื่อรวมคอลัมน์ 'Rank 1', 'Rank 2', และ 'Rank 3' เป็นคอลัมน์ 'population'
df_reshaped = pd.melt(df, id_vars=['Categories'], value_vars=['Satisfaction_5','Satisfaction_4','Satisfaction_3','Satisfaction_2','Satisfaction_1'], var_name='Satisfaction', value_name='population')

# แสดง DataFrame ที่ได้
print(df_reshaped)

with st.sidebar:
    st.title('Categories')

    Categories = list(df_reshaped.Categories.unique())[::-1]

    selected_Categories = st.selectbox('Select a Categories', Categories, index=len(Categories)-1)
    df_selected_Categories = df_reshaped[df_reshaped.Categories == selected_Categories]
    df_selected_Categories_sorted = df_selected_Categories.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    print(df_selected_Categories)

# คำนวณค่าเฉลี่ยของความพึงพอใจในหมวดหมู่การศึกษาตามวิธีที่ระบุ
avg1 = ((df_reshaped[df_reshaped['Categories'] == 'การเดินทางและความปลอดภัย']['population'] * df_reshaped[df_reshaped['Categories'] == 'การเดินทางและความปลอดภัย']['Satisfaction'].str[-1].astype(int)).sum() / 102).round(2)
avg2 = ((df_reshaped[df_reshaped['Categories'] == 'การศึกษา']['population'] * df_reshaped[df_reshaped['Categories'] == 'การศึกษา']['Satisfaction'].str[-1].astype(int)).sum() / 102).round(2)
avg3 = ((df_reshaped[df_reshaped['Categories'] == 'สุขภาพ']['population'] * df_reshaped[df_reshaped['Categories'] == 'สุขภาพ']['Satisfaction'].str[-1].astype(int)).sum() / 102).round(2)
avg4 = ((df_reshaped[df_reshaped['Categories'] == 'สิ่งแวดล้อม']['population'] * df_reshaped[df_reshaped['Categories'] == 'สิ่งแวดล้อม']['Satisfaction'].str[-1].astype(int)).sum() / 102).round(2)

print(avg1, avg2, avg3, avg4)

average = [avg1, avg2, avg3, avg4]

import altair as alt

alt.themes.enable("dark")

def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
  heatmap = alt.Chart(input_df).mark_rect().encode(
          y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Satisfaction", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
          x=alt.X(f'{input_x}:O', axis=alt.Axis(title="Categories", titleFontSize=16, titlePadding=15, titleFontWeight=900, labelAngle=0)),
          color=alt.Color(f'max({input_color}):Q',
                          legend=alt.Legend(title=" "),
                          scale=alt.Scale(scheme=input_color_theme)),
          stroke=alt.value('black'),
          strokeWidth=alt.value(0.25),
          #tooltip=[
          #    alt.Tooltip('year:O', title='Year'),
          #    alt.Tooltip('population:Q', title='Population')
          #]
      ).properties(width=900
      #).configure_legend(orient='bottom', titleFontSize=16, labelFontSize=14, titlePadding=0
      #).configure_axisX(labelFontSize=14)
      ).configure_axis(
      labelFontSize=12,
      titleFontSize=12
      )

  return heatmap

def make_donut(input_df, input_population, input_Satisfaction):
    donut_chart = alt.Chart(input_df).mark_arc().encode(
        theta=f'{input_population}:Q',
        color=alt.Color(f'{input_Satisfaction}:N', scale=alt.Scale(scheme='category20')),
        tooltip=[f'{input_Satisfaction}', f'{input_population}']
    ).properties(
        width=200,
        height=200,
        title='Donut Chart'
    )

    return donut_chart

color_scale = alt.Scale(
    domain=[0, 1, 2, 3, 4, 5],
    range=['white', 'red', 'orange', 'yellow', 'lightgreen', 'green']
)

# Create Gauge Chart using Altair
gauge_chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('Categories', title=None),
    y=alt.Y('average', title=None, scale=alt.Scale(domain=(0, 5))),
    color=alt.Color('average:Q', scale=color_scale, legend=None),
    tooltip=['Categories', 'average']
).properties(
    width=200,
    height=200
)

# Add full value text
text = gauge_chart.mark_text(
    align='center',
    baseline='bottom',
    dx=0,
    dy=-5,  # ระยะห่างจากแท่งกราฟ
    color='black',
    fontSize=14,  # ขนาดตัวอักษร
).encode(
    text=alt.Text('average:Q', format='.1f')  # รูปแบบของตัวเลข (ทศนิยม 1 ตำแหน่ง)
)

# Add full value bar
full_value_bar = alt.Chart(pd.DataFrame({'value': [5]})).mark_bar(color='black').encode(
    y=alt.Y('value', title=None),
    opacity=alt.value(0.5),
)

gauge_chart = (gauge_chart + text + full_value_bar)

# Display the Gauge Chart
st.altair_chart(gauge_chart, use_container_width=True)

col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Satisfaction')
    donut_chart = make_donut(df_selected_Categories, 'population', 'Satisfaction')
    st.altair_chart(donut_chart)

with col[0]:
    st.markdown('#### Total Ranking')

    heatmap = make_heatmap(df_reshaped, 'Satisfaction', 'Categories', 'population', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)

with col[2]:
    st.markdown('#### Top States')

    st.dataframe(df_selected_Categories,
                 column_order=("Satisfaction", "population"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "Satisfaction": st.column_config.TextColumn(
                        "Satisfaction",
                    ),
                    "population": st.column_config.ProgressColumn(
                        "Population",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_Categories_sorted.population),
                     )}
                 )