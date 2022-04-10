import streamlit as st
from hydralit import HydraHeadApp
from db import db_conn as oracle_db
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('default')
#import plotly
from io import BytesIO

# states = []
# modified_states = []
# #global where
# where = "WHERE state_name IN ("

class Home(HydraHeadApp):
    #where = "WHERE state_name = "

    def run(self):
        # global where
        # print(where)
        where = "WHERE state_name IN ("
        states = []
        modified_states = []
        # Example code to get data from database using cursor and connection object
        #state = st.text_input("Enter State: ")
        #states = []
        st.sidebar.header('State', anchor=None)
        state = st.sidebar.selectbox(
            "Select State",
            ('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
             'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho',
             'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
             'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
             'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
             'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
             'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
             'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
             'West Virginia', 'Wisconsin', 'Wyoming')
        )
        if state not in states:
            states.append(state)

        for val in states:
            mod = "\'" + val + "\'"
            if mod not in modified_states:
                modified_states.append(mod)

        print(states)
        print(modified_states)

        for index, val in enumerate(modified_states):
            if len(modified_states) > 1:
                where = where[:len(where) - 2]
                print(where)
                where += ", "
            where += modified_states[index] + ", "
            if index == len(modified_states) - 1:
                where = where[:len(where) - 2] + ")"


        #print(where)
        query = f"""WITH cte_funding AS(
                SELECT sname AS state_name, year, funding
                FROM "J.POULOS".state_fund),

                cte_accidents AS (
                SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                FROM "J.POULOS".accident
                GROUP BY state_name, EXTRACT(year FROM start_time))

                SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                {where}
                ORDER BY year"""

        #{where}
        #print(query)

        df_oracle2 = pd.read_sql(query, con=oracle_db.connection)
        st.write(df_oracle2)

        fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
        ax1.set_title('Funding')
        ax1.set_ylabel('Dollar Amount')

        ax2.set_title('Amount of Accidents', fontsize=12)
        ax2.set_xlabel('Year', fontsize=12)
        ax2.set_ylabel('Accidents')
        ax2.plot(df_oracle2['YEAR'], df_oracle2['ACCIDENTS'])
        ax1.plot(df_oracle2['YEAR'], df_oracle2['FUNDING'])
        plt.subplots_adjust(bottom=0.000000000000000000001)

        for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                    ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                    ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
            tick.set_fontsize(6)
        ax2.set_xticks(df_oracle2['YEAR'])
        ax1.set_xticks(df_oracle2['YEAR'])
        st.pyplot(fig=plt)

        if "load_state" not in st.session_state:
            st.session_state.load_state = False

        if st.button("Compare this state with another?") or st.session_state.load_state:
            st.session_state.load_state = True
            st.write('Why? One state should be good enough for you')
            state = st.sidebar.selectbox(
                "Select State",
                ('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
                 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho',
                 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
                 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
                 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
                 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                 'West Virginia', 'Wisconsin', 'Wyoming'), key=len(modified_states)
            )
            if state not in states:
                states.append(state)

            for val in states:
                mod = "\'" + val + "\'"
                if mod not in modified_states:
                    modified_states.append(mod)

            print(states)
            print(modified_states)

            for index, val in enumerate(modified_states):
                if len(modified_states) == 1:
                    break
                if len(modified_states) > 1:
                    where = where[:len(where) - 1]
                    #print(where)
                    #where += ", "
                where += modified_states[index] + ", "
                if index == len(modified_states) - 1:
                    where = where[:len(where) - 2] + ")"

            # print(where)
            query = f"""WITH cte_funding AS(
                    SELECT sname AS state_name, year, funding
                    FROM "J.POULOS".state_fund),

                    cte_accidents AS (
                    SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                    FROM "J.POULOS".accident
                    GROUP BY state_name, EXTRACT(year FROM start_time))

                    SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                    {where}
                    ORDER BY year"""

            #for debugging purposes. A previous sate shows up but that doesn't screw up the sql code.
            # ie if state1 was Alabama and state2 is arkansas you'll get ('Alabama', 'Alabama', 'Arkansas')
            # Too tired to fix. But really, it doesn't matter.
            #print(query)
            #print(where)

            #print(df_oracle2)
            #wtf? Why aren't isn't the previ
            df_oracle3 = pd.read_sql(query, con=oracle_db.connection)

            # Wtf? The dataframe printed completely ignores the previous state/funding values that were selected.
            # I don't see how thats possible when the query that prints has the 2 different states?!?
            st.write(df_oracle3)
            print(df_oracle3)
            for col in df_oracle3:
                print(col)

            for val in df_oracle3['STATE_NAME']:
                print(val)
            #frames = [df_oracle2, df_oracle3]
            #result = pd.concat(frames)
            #st.write(result)

            # df_oracle2['Key'] = 'trail1'
            # df_oracle3['Key'] = 'trail2'

            #fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
            ax1.set_title('Funding')
            ax1.set_ylabel('Dollar Amount')

            ax2.set_title('Amount of Accidents', fontsize=12)
            ax2.set_xlabel('Year', fontsize=12)
            ax2.set_ylabel('Accidents')
            # ax2.plot(df_oracle2['YEAR'], df_oracle3['YEAR'], df_oracle2['ACCIDENTS'], df_oracle3['ACCIDENTS'])
            # ax1.plot(df_oracle2['FUNDING'], df_oracle3['FUNDING'])

            for frame in [df_oracle2, df_oracle3]:
                ax1.plot(frame['YEAR'], frame['FUNDING'])
                ax2.plot(frame['YEAR'], frame['ACCIDENTS'])

            # df = pd.concat([df_oracle2, df_oracle3], keys=['trail1', 'trail2'])
            # dfgroup = df.groupby(['YEAR', 'Key'])
            # plt = dfgroup.sum().unstack('Key').plot()

            #plt.subplots_adjust(bottom=0.000000000000000000001)
            plt.tight_layout()

            for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                          ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                         ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                tick.set_fontsize(6)
            ax2.set_xticks(df_oracle2['YEAR'])
            ax1.set_xticks(df_oracle2['YEAR'])
            print(states)

            st.pyplot(fig=plt)

            if "another_state" not in st.session_state:
                st.session_state.another_state = False

            if st.button("Compare previous two with another state?") or st.session_state.another_state:
                st.session_state.another_state = True
                st.write('Why? Hot shot over here comparing 3 states smh')
                state = st.sidebar.selectbox(
                    "Select State",
                    ('Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
                     'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Idaho',
                     'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
                     'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi',
                     'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey',
                     'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma',
                     'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                     'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington',
                     'West Virginia', 'Wisconsin', 'Wyoming'), key=len(modified_states)
                )
                if state not in states:
                    states.append(state)

                for val in states:
                    mod = "\'" + val + "\'"
                    if mod not in modified_states:
                        modified_states.append(mod)

                print(states)
                print(modified_states)

                for index, val in enumerate(modified_states):
                    if len(modified_states) == 1:
                        break
                    if len(modified_states) > 1:
                        where = where[:len(where) - 1]
                        # print(where)
                        # where += ", "
                    where += modified_states[index] + ", "
                    if index == len(modified_states) - 1:
                        where = where[:len(where) - 2] + ")"

                # print(where)
                query = f"""WITH cte_funding AS(
                        SELECT sname AS state_name, year, funding
                        FROM "J.POULOS".state_fund),

                        cte_accidents AS (
                        SELECT COUNT(id) AS accidents, EXTRACT(year FROM start_time) AS year, state_name
                        FROM "J.POULOS".accident
                        GROUP BY state_name, EXTRACT(year FROM start_time))

                        SELECT * FROM cte_funding NATURAL JOIN cte_accidents
                        {where}
                        ORDER BY year"""

                # for debugging purposes. A previous sate shows up but that doesn't screw up the sql code.
                # ie if state1 was Alabama and state2 is arkansas you'll get ('Alabama', 'Alabama', 'Arkansas')
                # Too tired to fix. But really, it doesn't matter.
                # print(query)
                print(where)

                # print(df_oracle2)
                # wtf? Why aren't isn't the previ
                df_oracle4 = pd.read_sql(query, con=oracle_db.connection)
                df_oracle4 = df_oracle4[df_oracle4['STATE_NAME'] == states[len(states)-1]]

                # Wtf? The dataframe printed completely ignores the previous state/funding values that were selected.
                # I don't see how thats possible when the query that prints has the 2 different states?!?
                st.write(df_oracle4)
                print(df_oracle4)
                for col in df_oracle4:
                    print(col)

                for val in df_oracle4['STATE_NAME']:
                    print(val)
                # frames = [df_oracle2, df_oracle3]
                # result = pd.concat(frames)
                # st.write(result)

                # df_oracle2['Key'] = 'trail1'
                # df_oracle3['Key'] = 'trail2'

                # fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
                ax1.set_title('Funding')
                ax1.set_ylabel('Dollar Amount')

                ax2.set_title('Amount of Accidents', fontsize=12)
                ax2.set_xlabel('Year', fontsize=12)
                ax2.set_ylabel('Accidents')
                # ax2.plot(df_oracle2['YEAR'], df_oracle3['YEAR'], df_oracle2['ACCIDENTS'], df_oracle3['ACCIDENTS'])
                # ax1.plot(df_oracle2['FUNDING'], df_oracle3['FUNDING'])

                for frame in [df_oracle2, df_oracle3, df_oracle4]:
                    ax1.plot(frame['YEAR'], frame['FUNDING'])
                    ax2.plot(frame['YEAR'], frame['ACCIDENTS'])

                # df = pd.concat([df_oracle2, df_oracle3], keys=['trail1', 'trail2'])
                # dfgroup = df.groupby(['YEAR', 'Key'])
                # plt = dfgroup.sum().unstack('Key').plot()

                # plt.subplots_adjust(bottom=0.000000000000000000001)
                plt.tight_layout()

                for tick in ([ax1.title, ax1.xaxis.label, ax1.yaxis.label, ax2.title,
                              ax2.xaxis.label, ax2.yaxis.label] + ax1.get_xticklabels() +
                             ax2.get_xticklabels() + ax1.get_yticklabels() + ax2.get_yticklabels()):
                    tick.set_fontsize(6)
                ax2.set_xticks(df_oracle2['YEAR'])
                ax1.set_xticks(df_oracle2['YEAR'])
                print(states)
                #plt.legend(ax1.get_legend_handle_labels(), ax2.get_legend_handle_labels())

                st.pyplot(fig=plt)