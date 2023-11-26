import streamlit as st

def Home():
    col1, col2 = st.columns([12,1])
    with col1:
        st.header("Luiz Francisco dos Santos")
        st.caption("CSM, CSPO, Agile driven and Data Enthusiast")
        st.divider()
        st.write("Hello everyone, I would like to briefly introduce myself...")
        st.write("My name Luiz and quite experienced in agile software development best practices, I am deeply committed to driving efficiency and innovation within our industry harnessing empirical processes to develop real and impactful solutions that enhance visibility, predictability, and overall quality to build a better future. I take pride in creating a collaborative environment where me and my colleagues can thrive.")
        st.write("I am eager to connect and explore how my expertise can align with your goals and contribute to mutual success.")
    st.divider()
    with col2:
        st.image(r"images\luiz.jpg")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        skills = """
        + Agile Software Development
        + Process Leadership
        + Continuous Improvement
        + Creative Problem-Solving
        + Critical Thinking
        + Operational Efficiency
        + Project and Product Management
        + Data-Driven Decision Making
                """
        st.subheader("Core Skills:")
        st.markdown(skills)
    with col2:
        languages = """
        + English
        + Portuguese
        + Italian
                """
        st.subheader("We can communicate in:")
        st.markdown(languages)
    with col3:
        industries = """
        + Banking and Financial Services
        + Construction
        + Consumer Goods
        + Information Technology (IT)
        + Media and Entertainment
        + Retail (e-Commerce)
                """
        st.subheader("Industries I've worked on:")
        st.markdown(industries)
    with col4:
        hobbies = """
        + Travelling
        + To play RPG and Video Games
        + Photography
        + Watching animes
        + Techno music
                """
        st.subheader("Things I like to do:")
        st.markdown(hobbies)       
    st.divider()
    st.write("Technologies and Frameworks:")
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14, col15 = st.columns(15)
    with col1:
        st.image(r"images\seal-csm.png")
    with col2:
        st.image(r"images\jira.png")
    with col3:
        st.image(r"images\confluence.png")
    with col4:
        st.image(r"images\github.png")
    with col5:
        st.image(r"images\figma.png")
    with col6:
        st.image(r"images\seal-cspo.png")
    with col7:
        st.image(r"images\mysql.png")
    with col8:
        st.image(r"images\python.png")
    with col9:
        st.image(r"images\camunda.png")
    with col10:
        st.image(r"images\miro.png")
    with col11:
        st.image(r"images\streamlit.png")
    with col12:
        st.image(r"images\powerbi.png")
    with col13:
        st.image(r"images\plotly.png")
    with col14:
        st.image(r"images\fastAPI.png")
    with col15:
        st.image(r"images\pandas.png")