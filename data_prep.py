import requests
import json
import time
import pandas as pd
import numpy as np

#PRECLEANING (Transforming the json api calls into a dataframe and csv)
def get_games_data(page=1, per_page=100, total_pages=None):
    """
    This function makes the API request and transforms the json into a pandas DataFrame and csv
    
    Parameters:
    page - starting page number (default = 1)
    per_page - number of results to return per page (default = 100). API defaults to 25, but we want more results per_page so we make fewer requests
    total_pages - number of pages requested
    """
    # Specify url and parameters
    url = 'https://www.balldontlie.io/api/v1/games'
    parameters = {'per_page': per_page, 'page': page, 'postseason': True}
   # Make request with url and parameters and return results as json
    resp = requests.get(url, params=parameters).json()
   # total_pages = user-specified argument or the 'total_pages' value in the meta, whichever is less and NOT None
   # So if a user does NOT specify total_pages, function will use the 'total_pages' value in the meta data
    total_pages = min(x for x in [resp['meta']['total_pages'], total_pages] if x is not None)-page+1
   # Initialize data frame
    games_data = pd.DataFrame()
   # Looping through all our pages
    for page_num in range(page, total_pages+1):
       # Make request using url and parameters and return results as json
        parameters = {'page': page_num, 'per_page': per_page, 'postseason': True}
        resp = requests.get(url, params=parameters).json()
       # Create dataframe from json key, 'data'
        data = pd.DataFrame.from_records(resp['data'])
       # Format date column to datetype
       # Original values had timezone values included, so we remove those with dt.tz_localize(None)
        data['date'] = pd.to_datetime(data['date'], yearfirst=True, errors='coerce').dt.tz_localize(None)
       # Creating columns out of the dictionary-type columns
       # Iterating through columns
        for col in data.columns:
            # Since each value in col is same type, we can use the type of cell data[col][0] to test type for the entire column
            if type(data[col][0]) == dict:
               # For each key in our dictionary value
                for k in data[col][0].keys():
                   # Create a column named [column name]_[key value]
                   # Ex. 'home_team' has a key called 'full_name'
                   # So a column called 'home_team_full_name' will be created
                    data[col+"_"+k] = data[col].apply(lambda x: x[k])
       # Concat initial dataframe with dataframe from each iterations
        games_data = pd.concat([games_data, data])
       # Delay next request
        time.sleep(.8)

    games_data.to_csv('games_data.csv', index=False)
    
    return games_data


# DATA CLEANING FUNCTION ONE (first hypothesis test)
def make_east_west_df(data):
    """
    This function filters the original DataFrames to only display games of an East conference team playing against a West conference team. The resulting DataFrame is used for a hypothesis test comparing the scores of the two difference conferences.
    """    
   # Filter to only include games where East team plays West team
    data = data.loc[((data['home_team_conference']=="East")
                     & (data['visitor_team_conference']=="West"))
                   | ((data['home_team_conference']=="West")
                      & (data['visitor_team_conference']=="East"))].copy()
   # Creating East columns
    data['east_team'] = np.where(data['home_team_conference']=="East",
                                 data['home_team_full_name'],
                                 data['visitor_team_full_name'])
    data['east_score'] = np.where(data['home_team_conference']=="East",
                                  data['home_team_score'],
                                  data['visitor_team_score'])
   # Creating West columns
    data['west_team'] = np.where(data['home_team_conference']=="West",
                                 data['home_team_full_name'],
                                 data['visitor_team_full_name'])
    data['west_score'] = np.where(data['home_team_conference']=="West",
                                  data['home_team_score'],
                                  data['visitor_team_score'])
   # Create a column with difference in scores
    data['east_minus_west'] = data['east_score'] - data['west_score']
   # Only include certain columns
    data = data[['id', 'east_team', 'east_score',
                 'west_team', 'west_score', 'east_minus_west']]
    
    return data

# DATA CLEANING FUNCTION TWO (second hypothesis test)
def make_home_df(dataframe, conference=None, n=None):
    """
    This function filters the original DataFrames to only display home game scores. The resulting DataFrame is used for a hypothesis test comparing the score differences of games for the home teams to analyze which teams perform the best in their home courts.

    Parameters:
    dataframe = original DataFrame name
    conference = "East" or "West"
    n = number of teams to display (teams are ordered by their mean of score differences, descending)
    """
    data=dataframe.copy()
    # Calculate difference between home team score and visitor team score
    data['home_score_diff'] = data['home_team_score'] - data['visitor_team_score']
    # If conference is specified, filter data to only include teams in the conference
    if conference is not None:
        data = data.loc[data['home_team_conference'] == conference]
    # If n is specified, obtain the top n teams with highest means and filter original dataframe to only include those teams
    if n is not None:
        # Get means of each team
        top_n = pd.DataFrame(data.groupby('home_team_full_name')['home_score_diff'].mean())
        top_n.reset_index(inplace=True)
        # Sort by means, descending
        top_n.sort_values(by='home_score_diff', ascending=False, inplace=True)
        # Obtain top n teams
        top_n_teams = top_n['home_team_full_name'][:n]
        # Filter data to only include teams in top_n_teams
        data = data.loc[data['home_team_full_name'].isin(top_n_teams)]
    # Return team name and score difference columns
    data = data[['home_team_full_name', 'home_score_diff']]
    
    return data