import streamlit as st
from streamlit.components.v1 import html
from streamlit_javascript import st_javascript

import base64

class CustomNav:
    def __init__(self):
        st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">""", unsafe_allow_html = True)

    def _load_img(self, brand_img):
        file_ = open(brand_img, "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        return data_url
    
    def _create_options(self, options):
        res = ""

        for key, opt in options.items():
            p_class = "nav-link"

            if key == st_javascript("""localStorage.getItem("page")""", key = key): p_class += " active-page"
    
            res += f"""<li class="nav-item" id="{key}"><p class="{p_class}">{opt}</p></li>"""

        return res
    
    def nav(self, brand_img, brand_name, options, default = 0):
        default =list(options.keys())[default]

        st.markdown(f"""<style>{open("nav_components/style.css").read()}</style>""", unsafe_allow_html = True)
                
        html(f"""<script>
             if (localStorage.getItem("page") == null)
                localStorage.setItem("page", "{default}"
                <script>""", height = 0)

        img_url = self._load_img(brand_img)

        st.markdown(f"""
            <nav class="navbar navbar-expand-lg">
                <div class="container-fluid">
                    <div class="navbar-brand">
                        <img src = "data:image/gif;base64,{img_url}" class="d-inline-block align-text-middle" width = "150px" height = "50px">
                        {brand_name}
                    </div>
                </div>
            </nav>  
            <div id="navbarText">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">{self._create_options(options)}</ul>
            </div>
        """, unsafe_allow_html = True)

        st.markdown("""<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>""", unsafe_allow_html = True)

        self._navbar_js(options)
        return self._get_page()
    
    def _navbar_js(self, options):
        js = ""

        for key, opt in options.items():
            js += f"""parent.document.getElementById("{key}").onclick = function(ele){{localStorage.setItem("page", "{key}");parent.location.reload();}}\n"""

        html(f"<script>{js}</script>", height = 0)

    def _get_page(self):
        return st_javascript("""localStorage.getItem("page")""")