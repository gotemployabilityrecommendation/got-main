import streamlit as st
import math
import pandas as pd
import pydeck as pdk
import plotly.express as px
import re


class PoiBasedMap:
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

    def get_state_and_map_data(self, user_state, filter_faculty=""):
        '''
        It will show the company information on the map
        Parameters
        ----------
        user_state : string
            Name of the states in Malaysia.
        filter_faculty : string
            The name of predicted Faculty Domain.
            
        Returns
        -------
        None
            It will show a map.
        '''
        filter_faculty = filter_faculty.upper()
        if user_state in self.map_states:
            state_name = self.map_states[user_state]['name']
            state_center_point = self.map_states[user_state]['center_point']
            radius = 50
            if state_name == "KUALA LUMPUR" or state_name == 'PUTRAJAYA':
                radius = 20
            filtered_industry = []
            if filter_faculty != "":
                filtered_industry = self.faculty_industry_map[filter_faculty]
            st_map = self.get_com_nearby(
                lat=state_center_point[0], lon=state_center_point[1], radius=radius, filter_tag=filtered_industry)
            # mp = self.display_map(st_map)
            self.display_map(st_map, lat_alias='lat', lon_alias='lon', hover_title='company name', 
                                    width=400, height=400, zoom=10, center_lat=state_center_point[0], 
                                    center_lon=state_center_point[1], hover_data=['ratings', 'industry'])
            # mp.show()
            # st.map(st_map, size=2)
        else:
            st.write('Please enter the correct state')

    def get_permanent_address_map_data(self, lat, lon, radius=25, filter_faculty=""):
        '''
            It will show the company information on the map
            Parameters
            ----------
            lat : float
                Latitude.
            lon : float
                Longitude.
            radius: int
                radius in KM to show the surrounded company  
            filter_faculty: string
                   The name of predicted Faculty Domain.
            Returns
            -------
            None
                It will show a map.
        '''
        filter_faculty = filter_faculty.upper()
        filtered_industry = []
        if filter_faculty != "":
            filtered_industry = self.faculty_industry_map[filter_faculty]
        
        st_map = self.get_com_nearby(
            lat=lat, lon=lon, radius=radius,filter_tag=filtered_industry)
        self.display_map(st_map)
        # return self.display_map(st_map, lat_alias='lat', lon_alias='lon', hover_title='company name', 
        #                         width=400, height=400, zoom=10, center_lat=state_center_point[0], 
        #                         center_lon=state_center_point[1], hover_data=['ratings', 'industry'])

    def get_haversine(self, lat1, lon1, lat2, lon2):

        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * \
            math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        r = 6371
        distance = r * c
        return distance

    def get_js_com_info(self):
        return pd.read_csv("./job_recommendation/data/company_info_with_lat_lon.csv")

    def get_com_nearby(self, lat, lon, filter_tag=[], radius=50):
        data = self.get_js_com_info()
        if len(filter_tag) != 0:
            data = data[data['industry'].isin(filter_tag)]
            # data = data.filter(data[''])
        show_map_point_list = []
        for index, row in data.iterrows():
            distance = self.get_haversine(
                lat, lon, row['map_latitude'], row['map_longitude'])
            if distance <= radius:
                show_point = {
                    "lat": row['map_latitude'],
                    "lon": row['map_longitude'],
                    "company name": row['company_name'],
                    "address": row['address'],
                    "ratings": row['average_company_rating'],
                    **({'url': row['website_url']} if self.is_valid_url(row['website_url']) else {})
                }
                show_map_point_list.append(show_point)
        return pd.DataFrame(show_map_point_list)

    def show_map(self, dataframe):
        layer = pdk.Layer(
            "ScatterplotLayer",
            dataframe,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
            # Tooltip text including URL
            tooltip={"text": "{details}\n{ratings}\nURL: {url}"}
        )
        avg_lat = dataframe["lat"].mean()
        avg_lon = dataframe["lon"].mean()
        # Set the view
        view_state = pdk.ViewState(
            latitude=avg_lat, longitude=avg_lon, zoom=11)

        # Render the deck.gl map
        r = pdk.Deck(layers=[layer], initial_view_state=view_state)
        st.pydeck_chart(r)

    def display_map(self, dataframe, center_lat=None, center_lon=None, lat_alias='lat', lon_alias='lon', color_discrete_sequence=['RED'], hover_title='', hover_data=[], width=None, height=None, zoom=None):    
        if len(dataframe):
            fig = px.scatter_mapbox(dataframe, lat='lat', lon='lon', color_discrete_sequence=[
                                    "fuchsia"], hover_name='company name', hover_data=['company name', 'address', 'ratings', 'url'])
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
            fig.update_layout(width = 350, height = 440)
            # fig.show()
            st.plotly_chart(fig, use_container_width = True)
        else:
            st.info("No Company Found")
    
    def is_valid_url(self, url):
        try:
            if url == '' or url is None or url == 'no_data':
                return False
            pattern = re.compile(
                r'^(https?://)?(www\.)?([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)+.*)$')
            return bool(pattern.match(url))
        except:
            # print(url)
            return False
