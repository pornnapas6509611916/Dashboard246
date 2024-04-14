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

# Create a function to generate the gauge chart for a category
def make_gauge(category, average):
    color_scale = alt.Scale(

        domain=[1, 1.8, 2.6, 3.4, 4.2, 5],
        range=["red", "orange", "yellow", "lightgreen", "green"]
    )

    gauge_chart = alt.Chart(pd.DataFrame({'Category': [category], 'Average': [average]})).mark_bar().encode(
        x=alt.X('Average:Q', axis=None),
        color=alt.Color('Average:Q', scale=color_scale, legend=None)
    ).properties(
        title=category,
        width=200,
        height=100
    )

    return gauge_chart

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

with col[2]:
    st.markdown('#### Mean Satisfaction')
    gauge_chart = make_gauge('Satisfaction', average)  # Use the function make_gauge correctly
    st.altair_chart(gauge_chart)  # Use the correct variable name for the gauge chart

# Create DataFrame
data = pd.DataFrame({'categories': categories, 'averages': averages})

# Define color scale for gauge
color_scale = alt.Scale(
    domain=[1, 2, 3, 4, 5],
    range=['red', 'orange', 'yellow', 'lightgreen', 'green']
)

# Create Gauge Chart using Altair
gauge_chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('categories', title=None),
    y=alt.Y('averages', title=None, scale=alt.Scale(domain=(0, 5))),
    color=alt.Color('averages:Q', scale=color_scale, legend=None),
    tooltip=['categories', 'averages']
).properties(
    width=200,
    height=200
)

# Display the Gauge Chart
st.altair_chart(gauge_chart, use_container_width=True)

for i, category in enumerate(categories):
    data = pd.DataFrame({'category': [category], 'average': [averages[i]]})

    # Define color domain for the gauge
    color_domain = [1, 1.8, 2.6, 3.4, 4.2, 5]
    color_range = ['red', 'orange', 'yellow', 'lightgreen', 'green']

    chart = alt.Chart(data).mark_bar(size=100).encode(
        x='average:Q',
        color=alt.Color('average:Q', scale=alt.Scale(domain=color_domain, range=color_range)),
        tooltip=['average:Q']
    ).properties(
        width=200,
        height=150
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        ticks=False,
        labels=False
    )

    st.write(chart)

def gauge_chart(category, value, min_value, max_value, label):
    # Set up the figure and axis
    fig, ax = plt.subplots()

    # Draw the gauge
    theta = np.linspace(0.5 * np.pi, -0.5 * np.pi, 100)
    r = np.linspace(min_value, max_value, 100)
    x = r * np.sin(theta)
    y = r * np.cos(theta)
    ax.plot(x, y, color='gray', linewidth=2)

    # Draw the pointer
    angle = (0.5 - ((value - min_value) / (max_value - min_value))) * np.pi
    ax.plot([0, 0.9 * np.sin(angle)], [0, 0.9 * np.cos(angle)], color='red', linewidth=4)

    # Add the category label
    ax.text(0, -1.2, category, horizontalalignment='center', fontsize=14)

    # Add the value label
    ax.text(0, 1.2, label.format(value), horizontalalignment='center', fontsize=14)

    # Hide the axes
    ax.axis('off')

    # Show the plot
    plt.show()

# Example usage
category = 'Speed'
value = 75
min_value = 0
max_value = 100
label = 'Current speed: {} km/h'
gauge_chart(category, value, min_value, max_value, label)