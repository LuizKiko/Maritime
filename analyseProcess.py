import streamlit as st

def Analyse():
    col1, col2 = st.columns([12,1])
    with col1:
        st.header("Analyse process")
        st.caption("How the work has been developed")
        st.divider()
    with col2:
        st.image(r"images/analyse.jpg")
    col1, col2, col3 = st.columns(3)
    with col1:
        inputs = """
        ### Inputs:
        + Spire Maritime Analytics - Homework
            + This exercise aims to assess your ability to perform data analysis, identify patterns, and visualize insights using the provided datasets
        + Access to the test database        
                """
        st.markdown(inputs)
    with col2:
        steps = """
        ### Work steps
        1. Database access test
        2. Documentation inspection: https://documentation.spire.com/
        3. Research on maritime industry
        4. GBQ analysis
        5. Environment set for Python development
        6. Development
        7. Review
        8. Versioning
        9. Documentation
        10. Deployment
                """
        st.markdown(steps)
    with col3:
        tech = """
        ### Technology used:
        + Google Big Query
        + Python
        + Pandas
        + Streamlit
        + Plotly and Foluim
                """
        st.markdown(tech)      
    st.divider()
    description = """
        Short summary of the findings to be brought to the panel:

        This report presents a detailed analysis of maritime data, leveraging capabilities of Google BigQuery for data processing and Python with Plotly and Folium for dashboard development. The primary focus was to extract as much insights querying the tables: ship_types, port_polygons, and ais_messages.
        Analysis: 
        1. ship_types table provided insights into the vessel categories. I could get the metrics of min. avg. and max. amount of vessels using it as category. This analysis offered a deeper understanding of vessel distribution and operational profiles when crossed with other tables.
        2. port_polygons: Utilizing the port_polygons table, I could plot a map with all port locations, facilitating a geographical overview of maritime traffic hubs. This section highlighted wich continent/region/countries explore more the maritime industry and identified some characteristics in port activities.
        3. ais_messages: The ais_messages table was pivotal in analyzing vessel communication data. Patterns in maritime communication were examined, revealing paterns and anti-paterns for each vessel category. This analysis was instrumental in understanding maritime logistics and can be a key point to leverage more a sustainable future decreasing fuel consumption.

        Conclusion:

        It was a very interesting data analysis, which to be honest brought me more questions than answers at the moment, but what are the questions for if not fuel that moves us further in our evolution. 
        Thanks Spire for the oportunity, I am looking forward to meet you at the panel to present more in dept my finds.
 """
    st.markdown(description)