from itertools import count
import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import numpy as np
import pandas as pd
from PIL import Image
import pydeck as pdk
import datetime
import altair as alt


class Home(HydraHeadApp):

    def run(self):
        
        l1 = Image.open('images/logo.png')
        l2 = Image.open('images/logo2.png')
        st.image(l1)

        """
        This section is for the elements in the sidebar
        """
        st.sidebar.image(l2, width = 250)

        # Date selection
        day = 'Accidents by Day'
        st.sidebar.header(day, anchor = None)
        add_calendar = st.sidebar.date_input(
            "Date:", datetime.date(2019, 4, 1)
        )

        # Year slider
        st.sidebar.header('Accidents by Year', anchor = None)
        add_slider = st.sidebar.slider(
            'Select the range of years',
            2016, 2021, (2016, 2017)
        )
        
        # Weather options
        st.sidebar.header('Select Weather Conditions', anchor = None)
        w_clear = st.sidebar.checkbox('Clear')
        w_rain = st.sidebar.checkbox('Rain')
        w_snow = st.sidebar.checkbox('Snow')
        w_tornado = st.sidebar.checkbox('Tornado')

        # Temperature options
        st.sidebar.header('Select Temperature', anchor = None)
        temp1 = st.sidebar.checkbox('00 - 34 °F')
        temp2 = st.sidebar.checkbox('35 - 69 °F')
        temp3 = st.sidebar.checkbox('70 - 100 °F')

        # Time selection
        st.sidebar.header('Select Time', anchor = None)
        st.sidebar.time_input('Select Time', datetime.time(8, 45))

        # Text box
        st.sidebar.header('Traffic Pro', anchor = None)
        txt = st.sidebar.text_area('About', 
            "TrafficPro is a traffic accident data visualization tool designed for"
            "professionals in many fields from public safety to civil engineering."
            "TrafficPro allows users to analyze trends about traffic accidents"
            "occurring in the United States from 2016-2019."
    
            "TrafficPro integrates this accident data along with state demographic"
            "data to allow users to visualize trends in areas of interest.",
            height = 300
        )

        """
        This section is for the main page elements
        """
        # Data frame and map
        df = pd.DataFrame(
            np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
            columns=['lat', 'lon']
        )

        st.pydeck_chart(pdk.Deck(
            map_style = 'mapbox://styles/mapbox/light-v9',
            initial_view_state = pdk.ViewState(
                latitude = 37.0,
                longitude = -98.0,
                zoom = 3,
                pitch = 10,
            ),
            layers = [
                pdk.Layer(
                    'ScatterplotLayer',
                    data = df,
                    get_position = '[lon, lat]',
                    get_color = '[200, 30, 0, 160]',
                    get_radius = 75,
                ),
            ],
        ))

        # Data frame and bar graph
        df_graph = pd.DataFrame({
            'State': ['Florida', 'Michigan', 'Texas', 'Arizona', 'Nevada', 
                    'NY', 'Georgia', 'Maryland', 'California', 'New Mexico'],
            'Accident Totals': [450000, 250000, 105345, 500450, 320032, 
                                75345, 350450, 320032, 145345, 600450]
        })
        chart_data = alt.Chart(df_graph).mark_bar().encode(
            x = 'State', 
            y = 'Accident Totals',
            color = 'Origin:N'
        ).properties(height = 500, title = "Bar Graph").configure_range(
            category={'scheme': 'yelloworangered'}
        )
        st.altair_chart(chart_data, use_container_width = True)