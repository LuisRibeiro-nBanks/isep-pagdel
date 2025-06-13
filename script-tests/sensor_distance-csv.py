import pandas as pd
import numpy as np
from scipy.spatial import cKDTree
from connect_db import TestDBConnector

EARTH_RADIUS_KM = 6371

def find_traffic_sensors_within_radius(loc_df, radius_km=1.0):
    
    
    air_df = loc_df[loc_df['sensor_type'] == 'AIR QUALITY'].copy()
    traffic_df = loc_df[loc_df['sensor_type'] == 'ROAD TRAFFIC'].copy()

    # Convert lat/lon to radians
    air_coords = np.radians(air_df[['latitude', 'longitude']].values)
    traffic_coords = np.radians(traffic_df[['latitude', 'longitude']].values)

    # Build a KDTree from traffic sensor coordinates
    traffic_tree = cKDTree(traffic_coords)

    # Convert radius to radians
    radius_rad = radius_km / EARTH_RADIUS_KM

    # Query for all traffic sensors within radius for each air sensor
    results = traffic_tree.query_ball_point(air_coords, r=radius_rad)

    # Build result list
    data = []
    for i, traffic_indices in enumerate(results):
        air_sensor = air_df.iloc[i]
        for idx in traffic_indices:
            traffic_sensor = traffic_df.iloc[idx]
            lat1, lon1 = air_sensor['latitude'], air_sensor['longitude']
            lat2, lon2 = traffic_sensor['latitude'], traffic_sensor['longitude']
            distance = haversine_distance(lat1, lon1, lat2, lon2)
            data.append({
                "air_sensor": air_sensor['name'],
                "traffic_sensor": traffic_sensor['name'],
                "distance_km": distance
            })

    return pd.DataFrame(data)






def haversine_distance(lat1, lon1, lat2, lon2):
    R = EARTH_RADIUS_KM
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    return R * 2 * np.arcsin(np.sqrt(a))






#my_db = TestDBConnector(r'..\database\Data\test')
#my_connector = my_db.getConnector()
#my_cursor = my_db.getCursor()

#query = """SELECT * FROM Location"""
path = r'..\datasets\results\Result.csv'
locations_DF = pd.read_csv(path)

distance_DF = find_traffic_sensors_within_radius(locations_DF)
distance_DF.rename(columns={"LOCAL": "name", 
                            "LATITUDE": "latitude", 
                            "LONGITUDE": "longitude", 
                            "Type": "sensor_type"}, inplace=True)
print(distance_DF)
distance_DF.to_csv(r'..\datasets\results\Result-Distance.csv')
