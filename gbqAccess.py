from google.cloud import bigquery
import pandas as pd
from relativeGeo import relativeGeo

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

dfShipTypes = pd.read_gbq(project_id="maritime-analytics",query=qShipTypes)
dfPortPolygons = pd.read_gbq(project_id="maritime-analytics",query=qPortPolygons)
dfAisMessages = pd.read_gbq(project_id="maritime-analytics",query=qAisMessages)