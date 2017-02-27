from scraper import Strava_scraper
from geopy.geocoders import Nominatim
import os, csv
import pandas as pd
import numpy as np
import re, stravalib


# my user client secrete and access token. Not using access token for some reason. Not sure why I don't need it.
client_id = int(os.environ["STRAVA_CLIENT_ID"])
client_secret = os.environ["STRAVA_CLIENT_SECRET"]
access_token = os.environ["STRAVA_ACCESS_TOKEN"]

geocoder = Nominatim()

def write_list_to_csv(my_list, filename):
    """
    This method will write a list of items to a csv filename
    Input: my_list as list, filename as string
    Output: none
    """
    my_file = open(filename, 'wb')
    wr = csv.writer(my_file)
    wr.writerow(my_list)

def get_state(geocoder, lat, lng):
    location = geocoder.reverse([lat, lng])
    try:
        state = location.raw['address']['state']
        return state
    except KeyError:
        return "State not available"

def remap_athlete_datatypes(df, drop_identifying=True):
    """
    This method is to convert objects to numeric values when found. This pandas method is deprecated so may need to perform column operations explicitly in future.
    Input: df as DataFrame
    Output: df as DataFrame
    """

    df['city'] = df['city'].apply(lambda x: re.sub(r'[^\x00-\x7f]',r'',x) if x else 'unspecified city', 1)

    if drop_identifying:
        df.drop(['firstname', 'lastname', 'profile', 'profile_medium'], 1, inplace=True)

    otherdatatypes = {'id':'int', 'resource_state':'int'}

    for k, v in otherdatatypes.iteritems():
        df[k] = df[k].astype(v)

    return df.drop_duplicates(subset='id')

def create_athlete_df(ath_list):
    """
    This method creates an athletes DataFrame from a list of raw athlete objects from the stravalib api library. It uses remap_athlete_datatypes to get data into format safe for csv conversion.
    Input: ath_list as list
    Output: ath_df as DataFrame
    """
    columns = ['id', 'resource_state', 'firstname', 'lastname', 'profile_medium', 'profile', 'city', 'state', 'country', 'sex', 'friend', 'follower', 'premium', 'created_at', 'updated_at']

    ath_feat_matrix = np.array([[getattr(athlete, atribute) for atribute in columns] for athlete in ath_list])
    ath_df = pd.DataFrame(ath_feat_matrix, columns=columns)
    ath_df = ath_df.drop_duplicates(subset='id')
    ath_df = remap_athlete_datatypes(ath_df)
    return ath_df

def remap_activity_datatypes(df):
    """
    This method is to convert objects to numeric values when found. This pandas method is deprecated so may need to perform column operations explicitly in future.
    Input: df as DataFrame
    Output: df as DataFrame
    """
    str_cols = ['name', 'type']

    for col in str_cols:
        df[col] = df[col].apply(lambda x: re.sub(r'[^\x00-\x7F]+',r'',x) if x else 'unspecified {}'.format(col), 1)

    time_delta_cols = ['moving_time', 'elapsed_time']

    for col in time_delta_cols:
        df[col] = df[col].apply(lambda x: x.total_seconds(), 1)

    otherdatatypes = {'id':'int', 'distance':'float', 'total_elevation_gain':'float', 'achievement_count':'int', 'kudos_count':'int', 'comment_count':'int', 'athlete_count':'int', 'photo_count':'int', 'total_photo_count':'int', 'trainer':'bool', 'commute':'bool', 'manual':'bool', 'private':'bool', 'flagged':'bool', 'average_speed':'float', 'max_speed':'float', 'average_watts':'float', 'max_watts':'float', 'weighted_average_watts':'float', 'kilojoules':'float', 'device_watts':'bool', 'has_heartrate':'bool', 'average_heartrate':'float', 'max_heartrate':'float', 'athlete_id': 'int'}

    for k, v in otherdatatypes.iteritems():
        df[k] = df[k].astype(v)

    return df

def create_activity_df(act_list):
    """
    This method creates an activities DataFrame from a list of raw activity objects from the stravalib api library. It uses remap_activity_datatypes to get data into format safe for csv conversion.
    Input: act_list as list
    Output: act_df as DataFrame
    """

    columns = ['id', 'resource_state', 'external_id', 'upload_id', 'athlete', 'name', 'distance', 'moving_time', 'elapsed_time', 'total_elevation_gain', 'type', 'start_date', 'start_date_local', 'timezone', 'start_latlng', 'end_latlng', 'achievement_count', 'kudos_count', 'comment_count', 'athlete_count', 'photo_count', 'total_photo_count', 'map', 'trainer', 'commute', 'manual', 'private', 'flagged', 'average_speed', 'max_speed', 'average_watts', 'max_watts', 'weighted_average_watts', 'kilojoules', 'device_watts', 'has_heartrate', 'average_heartrate', 'max_heartrate']

    act_feat_matrix = np.array([[getattr(activity, atribute) for atribute in columns] for activity in act_list])
    act_df = pd.DataFrame(act_feat_matrix, columns=columns)

    act_df = act_df.drop_duplicates(subset='id')
    # create new column athlete containing athlete id
    act_df['athlete_id'] = pd.Series([athlete.id for athlete in act_df.athlete.values])
    # create new column map_id
    act_df['map_id'] = pd.Series([map.id if type(map) == stravalib.model.Map else None for map in act_df.map.values])
    # create new column map_summary_polyline
    act_df['map_summary_polyline'] = pd.Series([strava_map.summary_polyline if type(strava_map) == stravalib.model.Map else None for strava_map in act_df.map.values])
    # create new columns for start latitude, longitude and end latitude, longitude for the stravalib Latlon attribute
    act_df['start_lat'] = pd.Series([start[0] if type(start) == stravalib.attributes.LatLon else float('nan') for start in act_df.start_latlng.values])
    act_df['start_lng'] = pd.Series([start[1] if type(start) == stravalib.attributes.LatLon else float('nan') for start in act_df.start_latlng.values])
    act_df['end_lat'] = pd.Series([end[0] if type(end) == stravalib.attributes.LatLon else float('nan') for end in act_df.end_latlng.values])
    act_df['end_lng'] = pd.Series([end[1] if type(end) == stravalib.attributes.LatLon else float('nan') for end in act_df.end_latlng.values])


    # act_df['start_latlng'] = act_df['start_latlng'].apply(lambda x: list(x) if x else None, 1)
    # act_df['end_latlng'] = act_df['end_latlng'].apply(lambda x: list(x) if x else None, 1)
    # act_df['map'] = act_df['map'].apply(lambda x: {'id': x.id, 'summary_polyline': x.summary_polyline, 'resource_state': x.resource_state}, 1)

    # drop rows where athlete id is nan
    act_df = act_df[act_df['athlete_id'].fillna(0.0) > 0]
    # drop rows where gps data is null
    act_df = act_df[act_df['start_lat'].fillna(0.0) > 0]

    act_df['state'] = pd.Series([get_state(geocoder, start_lat, start_lng) for start_lat, start_lng in zip(act_df.start_lat.values, act_df.start_lng.values)])
    # drop columns that we don't potentially need
    act_df.drop(['athlete', 'upload_id', 'resource_state', 'external_id', 'start_latlng', 'end_latlng', 'map'], 1, inplace=True)


    act_df = remap_activity_datatypes(act_df)
    return act_df

def pickle_the_df(df, filename):
    df.to_pickle(filename)



if __name__ == '__main__':
    # df.to_csv('path', header=True, index=False, encoding='utf-8') # utility function saves df to csv
    # my_scraper = Strava_scraper(client_secret, access_token)
    pass
