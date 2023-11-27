import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static
import plotly.express as px

def PortsMap(dfPortPolygons: pd.DataFrame):
    col1, col2 = st.columns([10,1])
    with col1:
        st.subheader("Ports dashboard")
        st.caption("Designed to display various key metrics and geographical information about ports worldwide...")
        st.divider()
    with col2:
        st.image(r"images/port.jpg")

    def process_polygon_string(polygon_str):
        coords_str = polygon_str.replace('POLYGON ((', '').replace('))', '').split(', ')
        return [[float(coord.split()[1]), float(coord.split()[0])] for coord in coords_str]

    category = st.sidebar.selectbox("Select the category:", options=['continent', 'region', 'country'], index=None)
    selectedViewType = None
    if category != None:
        dfGrouped = dfPortPolygons.groupby(category).size().reset_index(name=category + 'Count')
        
        st.subheader("Ports location and information")
        metricTitles = dfGrouped[category].tolist()
        metricValues = dfGrouped[category + 'Count'].tolist()
        metricAvg = dfGrouped[category + 'Count'].mean().round()
        selectedAmount = len(metricTitles)
        columns = st.columns(selectedAmount)

        selectedViewType = st.sidebar.selectbox("Drilldown by:", options=metricTitles, index=0)

        dfFiltered = dfPortPolygons[dfPortPolygons[category] == selectedViewType]
        dfFiltered['coordinates'] = dfFiltered['polygon'].apply(process_polygon_string)
        dfFiltered['multi_polygon_coords'] = dfFiltered['coordinates'].apply(lambda x: [x])
        
        m = folium.Map(location=[0, 0], zoom_start=3, tiles='CartoDB dark_matter')
        for _, row in dfFiltered.iterrows():
            locode = "Locode: " + str(row['locode'])
            name = " | Port: " + str(row['name'])
            tooltip = locode + name
            folium.vector_layers.Polygon(locations=row['multi_polygon_coords'][0],
                                            fill_color='white',
                                            color='white', 
                                            weight=4,
                                            tooltip=tooltip).add_to(m)
        folium_static(m, width=2000, height=700)
        st.caption("Insights on comparing operations, can evolve into more in dept comparisson adding efficiency time based on vessels waiting time for example")
        st.divider()
        st.subheader("Count of ports and its delta comparing the reference with its category average")
        for i in range(selectedAmount):
            if i % 5 == 0:
                columns = st.columns(5)
            with columns[i % 5]:  
                st.metric(metricTitles[i], metricValues[i], metricValues[i] - metricAvg)