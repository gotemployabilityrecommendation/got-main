import streamlit as st
import pandas as pd
import numpy as np
from natsort import natsorted
import random
import statistics

from pre_uni.common import *
from pre_uni.map_shower import *

from model import ProbaModel

def show(data):
    state_selector = ['FT Kuala Lumpur', 'FT Labuan', 'FT Putrajaya', 'Johor', 'Kedah', 
                    'Kelantan', 'Melaka', 'Negeri Sembilan', 'Pahang', 'Perak', 
                    'Perlis', 'Penang', 'Sabah', 'Sarawak', 'Selangor', 'Terengganu']

    # domain_selector = ['ENGINEERING', 'FAC', 'FCA', 'FCM', 'IT', 'LAW', 'MANAGEMENT']
    faculty_domain_selector = ['ENGINEERING', 'APPLIED COMMUNICATION', 'CINEMATIC ART', 'IT', 'LAW', 'MANAGEMENT']
    domain_selector = ['ENGINEERING', 'FAC', 'FCA', 'IT', 'LAW', 'MANAGEMENT']
    # FAC: Applied Communication
    # FCA: Cinematic Art
    # FCM: Creative Multimedia

    left, right = st.columns((3, 2))

    with left:
        l1, l2 = st.columns((1,1))
        state = dropdown("State", state_selector, l1)
        domain = dropdown("Faculty Domain", faculty_domain_selector, l2)

        if domain == "APPLIED COMMUNICATION":
            domain = domain.replace("APPLIED COMMUNICATION", "FAC")
        elif domain == "CINEMATIC ART":
            domain = domain.replace("CINEMATIC ART", "FCA")

        getPoi = PoiBasedMap()

        getPoi.get_state_and_map_data(state, filter_faculty=domain)

    comb = pd.read_csv("pre_uni/combination.csv")
    data['Campus'] = ""
    data['Faculty domain'] = ""
    data['Program description'] = ""
    data['Faculty description'] = ""
    if data.iloc[0]['MUET'] == '':
        data["MUET"] = data["MUET"].replace('', 0)

    got_res = []
    emp_res = []
    for d in domain_selector:
        comb_c = comb[comb.Faculty_domain == d]
        got_lst = []
        emp_lst = []

        for i in range(len(comb_c)):
            data_c = data.copy()
            prev_domain = data_c["Faculty domain"].values[0]
            prev_c = data_c["Campus"].values[0]
            prev_pd = data_c["Program description"].values[0]
            prev_fd = data_c["Faculty description"].values[0]

            nxt_c = comb_c['Campus'].iloc[i]
            nxt_pd = comb_c['Program_Description'].iloc[i]
            nxt_fd = comb_c['Faculty_Description'].iloc[i]

            data_c["Faculty domain"] = data_c["Faculty domain"].replace(prev_domain, d)
            data_c["Campus"] = data_c["Campus"].replace(prev_c, nxt_c)
            data_c["Program description"] = data_c["Program description"].replace(prev_pd, nxt_pd)
            data_c["Faculty description"] = data_c["Faculty description"].replace(prev_fd, nxt_fd)

            model = ProbaModel(phases = ["before"])
            _, proba = model.predict(data_c)
            
            got = proba["got"]["before"][:, 1]
            emp = proba["employed"]["before"][:, 1]

            got = got.item()
            emp = emp.item()

            got_lst.append(got)
            emp_lst.append(emp)
        
        got_m = statistics.median(got_lst)
        emp_m = statistics.median(emp_lst)

        got_res.append(got_m)
        emp_res.append(emp_m)

    # cat = [col for col in data.columns if 'Cat' in col]
    # cat = natsorted(cat)
    # cat_val = []
    # for c in cat:
    #     cat_val.append(data[c].iloc[0])

    temp_state = data.iloc[0]['Permanent address state'].lower()
    temp_district = data.iloc[0]['Permanent address district'].lower()
    searching_location = f"{temp_district}, {temp_state}"
    testing_poi = pd.read_csv("pre_uni/Testing_POI_Data_Streamlit.csv")
    poi_df = testing_poi[testing_poi.Location == searching_location]
    cat_val = poi_df.drop(columns=['Location', 'State', 'District'])
    # cat_val = poi_df.values.tolist()[0]
    # st.write(cat_val)
    # cat_val = []
    # for i in range(10):
    #     cat_val.append(random.randint(0, 15))
    success_df = similarity(domain_selector, cat_val, temp_state)

    with right:
        radar(faculty_domain_selector, got_res, emp_res, st)
        bar(success_df, temp_state.upper(), st)

    # markdown("""<style>
    #             div.block-container{padding-top:1rem;z-index: 1}
    #             header[data-testid="stHeader"]{z-index: 0}
    #         </style>""")

    shadow()

