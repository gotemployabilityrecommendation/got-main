import streamlit as st
import geocoder
from job_recommendation.map_components.custom_map import CustomMap
from job_recommendation.jss_prediction_components.prediction import Prediction

class Recommendation():
    def __init__(self):
        st.markdown("""<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.11.8/dist/umd/popper.min.js" integrity="sha384-I7E8VVD/ismYTF4hNIPjVp/Zjvgyol6VFvRkX/vR+Vc4jQkC+hVqc2pM8ODewa9r" crossorigin="anonymous"></script>""", unsafe_allow_html=True)
        st.markdown("""<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>""", unsafe_allow_html=True)
        st.markdown("""<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">""", unsafe_allow_html=True)

    def _inject_css(self):
        st.markdown(
            f"""<style>{open("job_recommendation/recommendation_components/style.css").read()}</style>""", unsafe_allow_html=True)

    def _load_html(self, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()

    def _get_states(self):
        states = {
            'FT Kuala Lumpur': 'FT Kuala Lumpur',
            'FT Labuan': 'FT Labuan',
            'FT Putrajaya': 'FT Putrajaya',
            'Johor': 'Johor',
            'Kedah': 'Kedah',
            'Kelantan': 'Kelantan',
            'Melaka': 'Melaka',
            'Negeri Sembilan': 'Negeri Sembilan',
            'Pahang': 'Pahang',
            'Perak': 'Perak',
            'Perlis': 'Perlis',
            'Penang': 'Penang',
            'Sabah': 'Sabah',
            'Sarawak': 'Sarawak',
            'Selangor': 'Selangor',
            'Terengganu': 'Terengganu'
        }
        return states

    def _make_state_options(self, states):
        options_str = '<ul class="dropdown-menu">'
        for key, val in states.items():
            options_str += '<li><a class="dropdown-item" href="'+key+'">'+val+'</a></li>'
        options_str += '</ul>'

        dropdown_str = '<div class="dropdown"><button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">States</button>'+options_str+'</div>'
        return dropdown_str

    def _format_html(self, js, jss, percentage,faculty_domain):
        html = self._load_html('job_recommendation/recommendation_components/index.html')
        states = self._get_states()
        state_option = self._make_state_options(states)
        formated_html = html.format(
            percentage=percentage, js=js, jss=jss, state_options=str(state_option),faculty_domain=faculty_domain)
        # print(formated_html)
        return formated_html

    def _get_current_location(self):
        return 2.9277769,101.6393255
        # g = geocoder.ip('me')
        # if g.latlng:
        #     latitude, longitude = g.latlng
        #     return latitude, longitude
        # else:
        #     return None, None

    def _show_page(self,js,jss,percentage,faculty_domain):
        map_obj = CustomMap()

        self._inject_css()
        formated_html = self._format_html(js,jss, percentage,faculty_domain)
        st.markdown(formated_html, unsafe_allow_html=True)

        states = self._get_states()
        # col1, col_m, col2 = st.columns([.4, .2, .4])
        # col1, col2 = st.columns([.5, .3])
        left, right = st.columns([.5, .5])
        curr_lat, curr_lon = self._get_current_location()
        left.markdown(
            """<div style="color:black; font-size:24px; font-weight:900">Companies in</div>""", unsafe_allow_html=True)

        state = right.selectbox(
            label="State", options=states, label_visibility='collapsed')

        col1, col2 = st.columns([.5, .5])

        map1 = map_obj.get_state_and_map_data_with_jss(
            state, filter_jss=jss, zoom=10)
        st.plotly_chart(map1, use_container_width=True)

        st.markdown(
            f"""<div style="color:black; font-size:24px; font-weight:900">Companies Near MMU, Cyberjaya </div>""", unsafe_allow_html=True)
        # col1, col_m, col2 = st.columns([.4, .2, .4])

        map2 = map_obj.get_permanent_address_map_data_jss(
            lat=curr_lat, lon=curr_lon, filter_jss=jss, zoom=11,opacity=0.8)
        st.plotly_chart(map2, use_container_width=True)

    def recommend(self,data):
        pred = Prediction()
        js,jss,percentage,faculty_domain = pred.predict(data)
        self._show_page(js,jss,percentage,faculty_domain)
