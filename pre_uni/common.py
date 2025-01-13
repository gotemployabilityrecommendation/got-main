import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from io import StringIO

def markdown(html, container = st):
    container.markdown(html, unsafe_allow_html = True)

def dropdown(title, selector, container = st):
    selected = container.selectbox(title, selector)
    return selected

def radar(cat, got, emp, container = st):
    categories = cat

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r = got,
        theta=categories,
        fill='toself',
        name='GOT',
        fillcolor='rgba(255,0,0,0.5)',
        # marker='rgba(255,0,0,0.5)',
        # fillcolor='red',
        marker=dict(color='red')
    ))
    fig.add_trace(go.Scatterpolar(
        r = emp,
        theta=categories,
        fill='toself',
        name='Employability',
        fillcolor='rgba(0,0,255,0.5)',
        # fillcolor='blue',
        marker=dict(color='blue')
    ))

    fig.update_layout(
    polar=dict(
        radialaxis=dict(
        visible=True,
        range=[0, 1]
        )),
    showlegend=True
    )
    # fig.update_layout(title="Probability of GOT and Employability for each Faculty Domain")
    fig.update_layout(title = "Which Domain Seems Like the Right Fit for Me?")
    fig.update_layout(width = 500, height = 380)
    container.plotly_chart(fig, use_container_width = True)

def similarity_score(a, b):
    if a+b == 0:
        score = 0
    else:
        score = (1 - abs(a - b) / (a + b))
    return score

def similarity(domain, cat_val, temp_state):
    data = pd.read_csv("pre_uni/POI_Data_Streamlit.csv")
    data = data[data.Faculty_Domain != 'FCM']

    data['State'] = data['State'].str.lower()
    data = data[data.State == temp_state]
    
    cat_list = ['Attorneys and Law Offices', 'Engineering', 'Arts and Crafts', 'Management', 'Online Advertising',
    'Public Relations', 'Web Design and Development', 'Human Resources', 'Media', 'Art Dealers and Galleries']
    avg_list = []
    for index, row in data.iterrows():
        sum_similarity = 0
        # for idx, r in cat_val.iterrows():
        for i in range(len(cat_list)):
            # score = similarity_score(row[cat_list[i]], r[cat_list[i]])
            score = similarity_score(row[cat_list[i]], cat_val.iloc[0][cat_list[i]])
            sum_similarity += score
        avg_similarity = sum_similarity / 10
        avg_list.append(avg_similarity)
    data['Average_Similarity'] = avg_list
    
    df_list = []
    for i in range(len(domain)):
        df = data.loc[data['Faculty_Domain'] == domain[i]]
        # if len(df) >= 10:
        #     top_10 = df.sort_values(by = ['Average_Similarity'], ascending = False).head(10)
        # else:
        #     top_10 = df.sort_values(by = ['Average_Similarity'], ascending = False)
        df_list.append(df)

    success = []
    for i in range(len(df_list)):
        if len(df_list[i]) > 0:
            count = 0
            for index, row in df_list[i].iterrows():
                if row['GOT'] == 'Yes':
                    count += 1
            success.append(count / len(df_list[i]) * 100)
        else:
            success.append(0)
    
    success_df = pd.DataFrame({
        'Faculty_Domain': domain,
        'Success_GOT': success
    })

    return success_df

def bar(success_df, temp_state, container = st):
    success_df = success_df.sort_values(by=['Success_GOT'], ascending=False)
    fig = px.bar(y = success_df['Faculty_Domain'], x = success_df['Success_GOT'])
    t = f"How Likely Am I to Graduate on Time? ({temp_state})"
    fig.update_layout(
    # title="Percentage of Success GOT for the Top 10 Similarity Score Based on POI",
    # title = "How Likely Am I to Graduate on Time?",
    title = t,
    xaxis_title="Success GOT (%)",
    yaxis_title="Faculty Domain",
    )
    fig.update_layout(width = 500, height = 280)
    fig.update_layout(yaxis=dict(autorange="reversed"))
    fig.update_traces(
        hovertemplate="<br>".join([
            "GOT: %{x}%",
            "Faculty Domain: %{y}",
        ])
    )
    container.plotly_chart(fig, use_container_width = True)
    
def shadow():
    st.markdown(
        f"""
        <style>
        .stPlotlyChart {{
        border-radius: 3px;
        box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.20), 0 6px 20px 0 rgba(0, 0, 0, 0.30);
        }}
        </style>
        """, unsafe_allow_html=True
    )
    