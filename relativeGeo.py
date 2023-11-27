from google.cloud import bigquery
import pandas as pd
import folium
import streamlit as st
from streamlit_folium import folium_static


def relativeGeo(dfPortPolygons: pd.DataFrame, dfvesselInformation: pd.DataFrame, dfShipTypes: pd.DataFrame):
    
    #SIDEBAR
    vesselType = st.sidebar.selectbox("Select the category:",
                                options=dfShipTypes['shipType'].sort_values().unique(),  
                                index=None)

    #CONTENT
    col1, col2 = st.columns([5,1])
    with col1:
        st.subheader("Relative GeoLocation")
        st.caption("Relative geolocation for ships is a crucial aspect of maritime navigation and safety. It involves determining the position of a ship relative to other nearby ships, landmasses, or navigational markers. This concept is essential in congested waterways or during complex maneuvers, such as docking or navigating through narrow channels. Relative geolocation helps in collision avoidance, maintaining safe distances, and executing coordinated movements in fleets or convoys. Advanced technologies like AIS (Automatic Identification System), radar, and GPS are often employed to obtain precise relative positions, enhancing maritime situational awareness and operational efficiency.")
        st.divider()
    with col2:
        st.image(r"images\satelite.jpg")
    
    #FILTERED CONTENT
    if vesselType != None:
        qvesselInformation = """SELECT *
                            FROM   (SELECT Cast(md.timestamp AS date) AS timestamp,
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
                                    WHERE  md.latitude IS NOT NULL
                                        AND md.longitude IS NOT NULL
                                        and st.shipType = '""" + vesselType + """')
                            LIMIT  1000; """
        
        dfvesselInformation = pd.read_gbq(project_id="maritime-analytics",query=qvesselInformation)

        if not dfvesselInformation.empty:
            
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

            def process_polygon_string(polygon_str):
                    coords_str = polygon_str.replace('POLYGON ((', '').replace('))', '').split(', ')
                    return [[float(coord.split()[1]), float(coord.split()[0])] for coord in coords_str]

            def create_map(dfPortPolygons: pd.DataFrame, dfvesselInformation: pd.DataFrame):
                    
                    dfvesselInformation['polygon'] = dfvesselInformation.apply(lambda x: f"POLYGON (({x['longitude']} {x['latitude']}))", axis=1)
                    st.subheader("Vessels and ports correlation")
                    st.caption("Analyzing such information help understand traffic paterns per industry and ports activities")
                    m = folium.Map(location=[0, 0], zoom_start=3, tiles='CartoDB dark_matter')

                    for _, row in dfPortPolygons.iterrows():
                        tooltip_port = row['name']
                        folium.vector_layers.Polygon(locations=row['multi_polygon_coords'][0],
                                                    fill_color='steelblue',
                                                    color='white', 
                                                    weight=4,
                                                    tooltip=tooltip_port).add_to(m)

                    # Plot AIS Message Polygons
                    for _, row in dfvesselInformation.iterrows():
                        mmsi = "MMSI: " + str(row['mmsi'])
                        country = " | Country: " + str(row['flag_short_code'])
                        aisClass = "| AIS Class:" + str(row['ais_class'])
                        speed = "| Speed: " + str(row['speed'])
                        LAT = "LAT: " + str(row['latitude'])
                        LON = "LON: " + str(row['longitude'])
                        tooltip_vessel = mmsi + country + aisClass + speed
                        coordinates = process_polygon_string(row['polygon'])
                        folium.vector_layers.Polygon(locations=coordinates,
                                                    color='red',
                                                    weight=6,
                                                    tooltip=tooltip_vessel).add_to(m)


                    folium_static(m, width=2000, height=800)

            dfPortPolygons['coordinates'] = dfPortPolygons['polygon'].apply(process_polygon_string)
            dfPortPolygons['multi_polygon_coords'] = dfPortPolygons['coordinates'].apply(lambda x: [x])

            create_map(dfPortPolygons, dfvesselInformation)

            def parse_polygon_string(polygon_str):
                    coords_str = polygon_str.replace('POLYGON ((', '').replace('))', '').split(', ')
                    return [[float(coord.split()[1]), float(coord.split()[0])] for coord in coords_str]
            
            st.subheader("Surrounding per vessel")
            st.caption("By vizualizing the surrounding areas near the vessels and ports you can more efficient avoid accidents, provide assistence and calculate ETA based on the vessel speed.")

            m = folium.Map(location=[0, 0], zoom_start=2, tiles='CartoDB dark_matter')

            for _, row in dfvesselInformation.iterrows():
                    LAT=dfvesselInformation['latitude'][_]
                    LON=dfvesselInformation['longitude'][_]
                    folium.Map(location=[LAT, LON], zoom_start=2)
                    folium.Circle(
                    radius=100 * 1000,  # radius in meters
                    location=[LAT, LON],
                    color="red",
                    fill=True,
                    fill_opacity=0.1
                ).add_to(m)
            for _, row in dfvesselInformation.iterrows():
                mmsi = "MMSI: " + str(row['mmsi'])
                country = " | Country: " + str(row['flag_short_code'])
                aisClass = "| AIS Class:" + str(row['ais_class'])
                speed = "| Speed: " + str(row['speed'])
                LAT = "LAT: " + str(row['latitude'])
                LON = "LON: " + str(row['longitude'])
                tooltip_vessel = mmsi + country + aisClass + speed
                coordinates = parse_polygon_string(row['polygon'])
                folium.vector_layers.Polygon(locations=coordinates,
                                            fill_color='white',
                                            color='white',
                                            weight=4,
                                            tooltip=tooltip_vessel
                                            ).add_to(m)

            folium_static(m, width=2000, height=800)
           
        else:
            st.write("No information found for the Vessel type informed")
    else:
        st.write("Use the filters to create and display the dashboard")        
         
        #to study haversine formula  
        """
            R = 6371  # Earth radius in kilometers
            a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            R * c
            distance = round(haversine((36.84082166666667, 76.28162), (36.391345, 75.727675)))
        """