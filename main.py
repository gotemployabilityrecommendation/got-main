import pandas as pd

import streamlit as st

st.set_page_config(layout = "wide", )

from io import StringIO
from streamlit_javascript import st_javascript
from streamlit.components.v1 import html
from datetime import datetime

from nav_components import *
import pre_uni
import in_uni
import job_recommendation

from read_data import get_data
import json

if "page_reloaded" not in st.session_state:
    st.session_state["page_reloaded"] = False

sidebar_bg = "#386799"

st.markdown(f"""<style>
            div[class^="block-container"] {{padding-top: 0px; transform: translateY(-20px);}}
            div.block-container{{padding-left: 30px; padding-right: 30px}}
            div[data-testid="stSidebarContent"]{{background-color:{sidebar_bg}; color: white;}}
            div[data-testid="stFileUploader"] section{{background-color: {sidebar_bg}; color: white; border: 2px solid white; border-style: dotted}}
            div[data-testid="stFileUploaderDropzoneInstructions"]{{color:{sidebar_bg} white !important}}
            div[data-testid="stSidebarContent"] small {{color: white}}
            div[data-testid="stSidebarContent"] div {{color: white;}}
            div[data-testid="stFileUploader"] button {{background-color: {sidebar_bg}; border: 2px solid white;}}
            footer {{visibility: hidden;}}
            .stPlotlyChart {{
                border-radius: 3px;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.20), 0 6px 20px 0 rgba(0, 0, 0, 0.30);
            }}
            </style>""", unsafe_allow_html = True)

navbar = CustomNav()

options = {"pre_uni": "Pre-University", 
           "in_uni": "In-University", 
           "job_recommendation": "Job Recommendation"}

page = navbar.nav("logo.png", "Graduate on Time and Employability Analytics", options)

file = st.sidebar.file_uploader("Choose a file", type = "pdf", accept_multiple_files = False)

if file is not None:
    file = get_data(file)

    # for key, val in file.items():
    #     html(f"""<script>localStorage.setItem("student-data-{key}", "{val}")</script>""", height = 0)

    html(f"""<script>localStorage.setItem("student-data-dict-js", "{file}")</script>""", height = 0)

    html(f"<script>localStorage.setItem('has_data', true); parent.document.getElementById('{page}').click()</script>", height = 0)

elif st_javascript("""localStorage.getItem("has_data")""") == "true":
    try:
        file_input = st_javascript("""localStorage.getItem('student-data-dict-js')""")
        if file_input != 0:
            file_input = eval(file_input)

            file = {}
            orig_file = {}

            for key, val in file_input.items():

                orig_file[key] = val
                try: 
                    if "." in val: val = float(val)
                    else: val = int(val)

                except:
                    pass

                file[key] = [val]

        data = pd.DataFrame(file)
        
        if page == "in_uni":
            nan_values = []

            for col in ["Campus", "Faculty domain", "Faculty description", "Program description"]:
                if col not in data.columns:
                    nan_values.append(col)

            if len(nan_values):
                st.info(f"Please input your {', '.join(nan_values)}.")
            else: 
                if "MUET" in data.columns:
                    data["MUET"] = data["MUET"].replace("", "irrelavant")

                trim_cols = [int(col[1:2]) for col in data.columns if "gpa" in col and data[col].unique()[0] != ""]
                nxt_trim = sorted(trim_cols)
                
                if len(nxt_trim): nxt_trim = nxt_trim[-1] + 1
                else: nxt_trim = 1
                
                in_uni.page.show(data, n_trim = 6, nxt_trim = nxt_trim)

        elif page == "pre_uni":
            pre_uni.page.show(data)

        elif page == "job_recommendation":
            nan_values = []

            for col in ["Campus", "Faculty domain", "Faculty description", "Program description"]:
                if col not in data.columns:
                    nan_values.append(col)

            if len(nan_values):
                st.info(f"Please input your {', '.join(nan_values)}.")
            else: 
                job_recommendation.page.show(orig_file)
          
    except Exception as e:
        st.write(e)

else:
    st.info("Please upload a PDF")

img_url = CustomNav()._load_img("tm_logo.png")
st.markdown(f"""<div class = "row p-0" style = "margin-top: -90px">
    <div class = "col-md-8"></div>
    <div class = "col-md-4">
       <img src = "data:image/gif;base64,{img_url}" width = "200px" height = "200px" style="margin-left: 340px;">
    </div>
</div>""", unsafe_allow_html = True)