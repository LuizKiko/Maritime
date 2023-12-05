from google.cloud import bigquery
import pandas as pd
from relativeGeo import relativeGeo
import os
from google.cloud.bigquery.client import Client
import streamlit as st
import json
from google.oauth2.service_account import Credentials

# Reconstruct credentials JSON from Streamlit secrets
credentials_info = st.secrets['bigquery_credentials']

# Load credentials from the JSON string
credentials = Credentials.from_service_account_info(dict(credentials_info))

# Use credentials directly with BigQuery client
from google.cloud import bigquery
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


qShipTypes = "select st.shipType, count(st.shipType) FROM  `test_data.ship_types` AS st group by st.shipType;"
qPortPolygons = "SELECT * FROM `maritime-analytics.test_data.port_polygons`;"

qAisMessages = """SELECT *
                            FROM   (SELECT Cast(md.timestamp AS date),
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
                                        AND md.longitude IS NOT NULL)
                            LIMIT  1000; """

dfShipTypes = pd.read_gbq(credentials=credentials, project_id=credentials.project_id, query=qShipTypes)
dfPortPolygons = pd.read_gbq(credentials=credentials, project_id=credentials.project_id, query=qPortPolygons)
dfAisMessages = pd.read_gbq(credentials=credentials, project_id=credentials.project_id, query=qAisMessages)
