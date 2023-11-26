import pandas as pd
import folium
from streamlit_folium import folium_static
import streamlit as st
import datetime
import plotly.express as px

def Messages(dfvesselInformation: pd.DataFrame, dfShipTypes: pd.DataFrame, dfPortPolygons: pd.DataFrame):
    #SIDEBAR
    vesselType = st.sidebar.selectbox("Select the category:",
                                options=dfShipTypes['shipType'].sort_values().unique(),  
                                index=None)

    #CONTENT
    col1, col2 = st.columns([10,1])
    with col1:
        st.subheader("Vessels dashboard")
        st.caption("Vessels in the maritime industry refer to various types of watercraft used for different purposes at sea. These range from large cargo ships and oil tankers, which play a crucial role in global trade and energy transportation, to passenger ships like cruise liners and ferries. There are also specialized vessels such as fishing boats, tugboats, and research ships. Each type of vessel is uniquely designed for its specific function, whether it's transporting goods across oceans, carrying passengers, aiding in navigational tasks, or conducting maritime research and exploration. Vessels are the backbone of the maritime industry, facilitating a significant portion of international commerce and mobility.")
        st.divider()
    with col2:
        st.image(r"images\vessel.jpg")
    
    #FILTERED CONTENT
    if vesselType != None:
        qvesselInformation = """SELECT *
                            FROM   (SELECT Cast(md.timestamp AS date) AS timestamp,
                                        Cast(md.timestamp AS time) AS timestamp2,
                                        md.ais_class,
                                        st.mmsi,
                                        md.collection_type,
                                        md.latitude,
                                        md.longitude,
                                        md.flag_short_code,
                                        md.speed,
                                        md.message_type,
                                        st.shiptype
                                    FROM   test_data.ais_messages AS md
                                        LEFT JOIN test_data.ship_types AS st
                                                ON md.mmsi = st.mmsi
                                    WHERE  st.shipType = '""" + vesselType + """')
                            LIMIT  1000; """
        
        dfvesselInformation = pd.read_gbq(project_id="maritime-analytics",query=qvesselInformation)

        if not dfvesselInformation.empty:

            """calendar = st.sidebar.date_input("Date specification", datetime.date(2023, 9, 20))
            calendar = calendar.f"{year}-{month:02d}-{day:02d}"
            dfvesselInformation = dfvesselInformation"""

            dfvesselInformation['speed'].fillna(0, inplace=True)
            speedMin = dfvesselInformation['speed'].min().round()
            speedMax = dfvesselInformation['speed'].max().round()
            speedavg = dfvesselInformation['speed'].mean().round()

            st.subheader("Vessel Speed")
            speed1, speed2, speed3 = st.columns(3)
            with speed1:
                st.metric("Min.",speedMin,delta=speedMin-speedavg)
            with speed2:
                st.metric("Avg.",speedavg)
            with speed3:
                st.metric("Max.",speedMax,delta=speedMax-speedavg)

            st.divider()

            ais1, message1 = st.columns(2)
            with ais1:
                dfCollectionTypeCount = dfvesselInformation.groupby('collection_type').size().reset_index(name='collection_typeCount').sort_values(by='collection_typeCount')
                average_count = dfCollectionTypeCount['collection_typeCount'].mean()
                aisChart = px.bar(dfCollectionTypeCount, x='collection_type', y='collection_typeCount', title='COMMUNICATION PER DATA SOURCE', color='collection_type')
                aisChart.add_hline(y=average_count,
                    annotation_text="Average",
                    line_color="red",
                    annotation_position="top right")
                st.plotly_chart(aisChart, use_container_width=True)
                st.caption("Inspecting technologies used per industry can give foresight on finding paterns and trends for investiments.")
            with message1:
                dfMessagesDic = pd.read_csv("messageTypes.csv")
                dfMessageSummary = dfvesselInformation.groupby('message_type').size().reset_index(name='message_typeCount').sort_values(by='message_typeCount')
                average_count = dfMessageSummary['message_typeCount'].mean()
                dfMessageSummary = pd.merge(dfMessageSummary,dfMessagesDic, on="message_type", how="left")
                dfMessageSummary.fillna("UNKNOWN", inplace=True)
                messageChart = px.bar(dfMessageSummary, x='message', y='message_typeCount', title='SUMMARY OF MESSAGE TYPES', color='message')
                messageChart.add_hline(y=average_count, annotation_text="Average", line_color="red", annotation_position="top right")
                st.plotly_chart(messageChart, use_container_width=True)
                st.caption("Finding paterns regarding message types can also help understand and capture outliers and take actions faster potentially reducing the operational cost")
            
            st.divider()
            flag1, region1 = st.columns(2)
            with flag1:
                dfCountryDic = pd.read_csv("countryDic.csv")
                dfCountry = dfvesselInformation.groupby('flag_short_code').size().reset_index(name='flag_short_code_typeCount').sort_values(by='flag_short_code_typeCount')
                average_count = dfCountry['flag_short_code_typeCount'].mean()
                dfCountry = pd.merge(dfCountry,dfCountryDic, on="flag_short_code", how="left")
                dfCountry.fillna("UNKNOWN", inplace=True)
                countryChart = px.bar(dfCountry, x='Country', y='flag_short_code_typeCount', title='Vessels per country', color='flag_short_code')
                countryChart.add_hline(y=average_count, annotation_text="Average", line_color="red", annotation_position="top right")
                st.plotly_chart(countryChart, use_container_width=True)
                st.caption("Understanding the volume of messages per country can help plan ahead regarding the countries demand per industry type")

            with region1:
                dftimeframe = dfvesselInformation.groupby('timestamp').size().reset_index(name='timestamp_Count').sort_values(by='timestamp_Count')
                dateChart = px.line(dftimeframe, x='timestamp', y='timestamp_Count', title='Vol. of messages overtime')
                st.plotly_chart(dateChart, use_container_width=True)
                st.caption("Its important also analysing the volume over time to see if they are in the expected range tending to increase or otherwise, actions plans are cheaper when early put in place")
        st.divider()
        st.write('Future improvements could be:')
        st.caption('= Filter per dat to manage better the volume of data')
        st.caption('- Charts covering messages per Region and Rate of turn for example')