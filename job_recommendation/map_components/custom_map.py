import math
import pandas as pd
import plotly.express as px
import streamlit as st
import json
import os

class CustomMap:

    def __init__(self) -> None:
         self.current_path = "job_recommendation"
    map_states = {
        'FT Kuala Lumpur': {'name': 'KUALA LUMPUR', 'center_point': (3.1390, 101.6869)},
        'FT Labuan': {'name': 'LABUAN', 'center_point': (5.2831, 115.2308)},
        'FT Putrajaya': {'name': 'PUTRAJAYA', 'center_point': (2.9264, 101.6964)},
        'Johor': {'name': 'JOHOR', 'center_point': (1.4854, 103.7618)},
        'Kedah': {'name': 'KEDAH', 'center_point': (6.1184, 100.3685)},
        'Kelantan': {'name': 'KELANTAN', 'center_point': (6.1254, 102.2386)},
        'Melaka': {'name': 'MELAKA', 'center_point': (2.1896, 102.2501)},
        'Negeri Sembilan': {'name': 'NEGERI SEMBILAN', 'center_point': (2.7258, 101.9424)},
        'Pahang': {'name': 'PAHANG', 'center_point': (3.8126, 103.3256)},
        'Perak': {'name': 'PERAK', 'center_point': (4.5921, 101.0901)},
        'Perlis': {'name': 'PERLIS', 'center_point': (6.4449, 100.2048)},
        'Penang': {'name': 'PENANG', 'center_point': (5.4141, 100.3288)},
        'Sabah': {'name': 'SABAH', 'center_point': (5.9788, 116.0753)},
        'Sarawak': {'name': 'SARAWAK', 'center_point': (1.5535, 110.3593)},
        'Selangor': {'name': 'SELANGOR', 'center_point': (3.0738, 101.5183)},
        'Terengganu': {'name': 'TRENGGANU', 'center_point': (5.3117, 103.1324)},
    }

    faculty_industry_map = {
        "MANAGEMENT": [
            "Banking/Financial Services",
            "Consulting (Business & Management)",
            "Human Resources Management/Consulting",
            "Insurance",
            "Retail/Merchandise",
            "General & Wholesale Trading",
            "Property/Real Estate",
            "Others"
        ],
        "IT": [
            "Computer/Information Technology (Software)",
            "Computer/Information Technology (Hardware)",
            "Telecommunication",
            "Consulting (IT, Science, Engineering & Technical)",
            "E-commerce",
            "Cybersecurity"
        ],
        "ENGINEERING": [
            "Construction/Building/Engineering",
            "Electrical & Electronics",
            "Heavy Industrial/Machinery/Equipment",
            "Automobile/Automotive Ancillary/Vehicle",
            "Aerospace/Aviation/Airline",
            "Energy and Utilities"
        ],
        "LAW": [
            "Law/Legal Services",
            "Government/Defence",
            "Intellectual Property",
            "Compliance and Regulatory roles"
        ],
        "FCM": [
            "Advertising/Marketing/Promotion/PR",
            "Arts/Design/Fashion",
            "Entertainment/Media",
            "Digital Media",
            "Graphic Design and Illustration"
        ],
        "FAC": [
            "Advertising/Marketing/Promotion/PR",
            "Consulting (Business & Management)",
            "Education",
            "Journalism",
            "Public Relations",
            "Corporate Communications"
        ],
        "FCA": [
            "Entertainment/Media",
            "Advertising/Marketing/Promotion/PR",
            "Film and Television Production",
            "Arts/Design/Fashion",
            "Digital Cinematography"
        ]
    }

    def _jss_industry_map(self, key):
        f = open(self.current_path +
                 '/map_components/jss_industry_map.json')
        data = json.load(f)
        return data[key]

    def _get_js_com_info(self):
        return pd.read_csv("job_recommendation/data/company_info_with_lat_lon.csv")

    def _get_haversine(self, lat1, lon1, lat2, lon2):

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        r = 6371
        distance = r * c
        return distance

    def _get_com_nearby(self, lat, lon, filter_tag=[], radius=50):
        data = self._get_js_com_info()
        if len(filter_tag) != 0:
            data = data[data['industry'].isin(filter_tag)]
            # data = data.filter(data[''])
        show_map_point_list = []
        for index, row in data.iterrows():
            distance = self._get_haversine(
                lat, lon, row['map_latitude'], row['map_longitude'])
            if distance <= radius:
                show_point = {
                    "lat": row['map_latitude'],
                    "lon": row['map_longitude'],
                    "company name": row['company_name'],
                    "address": row['address'],
                    "ratings": f"{row['average_company_rating']}/5({row['reviews_count']})",
                    "industry": row['industry'],
                    # **({'url': row['website_url']} if self.is_valid_url(row['website_url']) else {'url': 'no_data'})
                }
                show_map_point_list.append(show_point)
        return pd.DataFrame(show_map_point_list)

    def display_map(self, dataframe, center_lat=None, center_lon=None, lat_alias='lat', lon_alias='lon', color_discrete_sequence=['RED'], hover_title='', hover_data=[], width=None, height=None, zoom=None, opacity=None):
        current_loc_df = pd.DataFrame(
            [{'lat': center_lat, 'lon': center_lon,'company name':'selected location','ratings':'*','industry': 'selected location'}])
        new_df = pd.concat([dataframe, current_loc_df])

        # if len(new_df == 1):
        #     fig = px.scatter_mapbox(new_df, lat=lat_alias, lon=lon_alias, color_discrete_sequence=color_discrete_sequence+[
        #                             "GREEN"], width=width, height=height, opacity=opacity)
        # else:
        fig = px.scatter_mapbox(new_df, lat=lat_alias, lon=lon_alias, color_discrete_sequence=color_discrete_sequence+["GREEN"],
                                    hover_name=hover_title, hover_data=hover_data, width=width, height=height, opacity=opacity,custom_data=[])

        fig.update_layout(mapbox_style="open-street-map")

        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(
            autosize=False,
            hovermode='closest',
            mapbox=dict(
                bearing=0,
                center=dict(
                    lat=center_lat,
                    lon=center_lon
                ),
                pitch=0,
                zoom=zoom
            ),
        )
        if (len(new_df) != 1):
            fig.update_traces(
                hovertemplate='<b>%{hovertext}</b><br>Ratings: %{customdata[0]}<br>Industry type: %{customdata[1]}')
        return fig

    def get_state_and_map_data_with_jss(self, user_state, filter_jss="", height=330, width=200, zoom=None, opacity=None):
        '''
        It will show the company information on the map
        Parameters
        ----------
        user_state : string
            Name of the states in Malaysia.
        filter_jss : string
            The name of predicted job sector.

        Returns
        -------
        None
            It will show a map.
        '''
        if user_state in self.map_states:
            state_name = self.map_states[user_state]['name']
            state_center_point = self.map_states[user_state]['center_point']
            radius = 50
            if state_name == "KUALA LUMPUR" or state_name == 'PUTRAJAYA':
                radius = 20
            filtered_industry = []
            if filter_jss != "":
                filtered_industry = self._jss_industry_map(filter_jss)
            st_map = self._get_com_nearby(
                lat=state_center_point[0], lon=state_center_point[1], radius=radius, filter_tag=filtered_industry)
            return self.display_map(st_map, lat_alias='lat', lon_alias='lon',
                                     hover_title='company name', width=width, height=height, zoom=zoom, center_lat=state_center_point[0], center_lon=state_center_point[1], hover_data=['ratings', 'industry'], opacity=opacity)
        else:
            st.write('Please enter the correct state')

    def get_permanent_address_map_data_jss(self, lat, lon, radius=25, filter_jss="", height=350, width=200, zoom=None, opacity=None):
        filter_tag = self._jss_industry_map(filter_jss)
        st_map = self._get_com_nearby(
            lat=lat, lon=lon, radius=radius, filter_tag=filter_tag)
        # print(st_map)

        mp = self.display_map(st_map, center_lat=lat, center_lon=lon, color_discrete_sequence=[
            'BLUE'], hover_title='company name', width=width, height=height, zoom=zoom, opacity=opacity, hover_data=['ratings', 'industry'])
        return mp
