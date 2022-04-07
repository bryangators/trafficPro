import streamlit as st
from hydralit import HydraHeadApp
import matplotlib.pyplot as plt
from io import BytesIO


class State(HydraHeadApp):

    def run(self):
        st.title("State")
        # this is where code for page will be

        cat = ["bored", "happy", "bored", "bored", "happy", "bored"]
        dog = ["happy", "happy", "happy", "happy", "bored", "bored"]
        activity = ["combing", "drinking", "feeding", "napping", "playing", "washing"]

        # width = st.sidebar.slider("plot width", 0.1, 25., 3.)
        # #width = st.sidebar.slider("year", 2016, 2020, key='interval')
        # print(width)
        #
        # height = st.sidebar.slider("plot height", 0.1, 25., 1.)
        #
        # fig, ax = plt.subplots(figsize=(width, height))
        # ax.plot(activity, dog, label="dog")
        # ax.plot(activity, cat, label="cat")
        # ax.legend()
        #
        # buf = BytesIO()
        # fig.savefig(buf, format="png")
        # st.image(buf)

        age = st.slider('Choose a year', 2016, 2020)
        st.write('You chose', age)