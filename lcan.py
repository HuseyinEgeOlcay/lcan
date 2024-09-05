import pandas as pd
import berserk
from datetime import timedelta

class game:
    """Make a request for a resource in a paticular format.
    
    :param white: white player
    :param black: black player
    :param time: when the last move is done
    :param wp: white's point in the game
    :param wpt: white's total point after the game
    :param bp: black's point in the game
    :param bpt: black's total point after the game
    """
    def __init__(self, white, black, time, wp=None, wpt=None, bp=None, bpt=None):
        self.white = white
        self.black = black
        self.time = time
        self.wp = wp
        self.bp = bp
        self.wpt = 0
        self.bpt = 0
    
    def __lt__(self, other):
        return self.time < other.time

class player:
    """Make a request for a resource in a paticular format.
    
    :param name: username of the player
    :param sheet: score sheet
    :param point: total point
    :param counter: counter for matcing score sheet and match time
    :param team: team of the player
    :param point_list: dictionary which has points as key and value as match time
    """
    def __init__(self, name, sheet, team=None):
        self.name = name
        self.sheet = sheet
        self.point = 0
        self.counter = -1
        self.team = team
        self.point_list = {}

#Lichess API token(Optional for faster data stream)        
token="" 
session = berserk.TokenSession(token)
client = berserk.Client(session=session)

# Get tournament info, games and player's score sheet
tournamnet_results = client.tournaments.stream_results("88D8Ewzn", sheet=True)
tournament_games = client.tournaments.export_arena_games("88D8Ewzn")
tournament=client.tournaments.get_tournament("88D8Ewzn")

# Check if it's a team tournament
if "teamBattle" in tournament:
    print("This is a team tournament")
    players = [player(i["username"], i["sheet"], i["team"]) for i in tournamnet_results]
else:
    print("This is an individual tournament")
    players = [player(i["username"], i["sheet"]) for i in tournamnet_results]

games = [game(i["players"]["white"]["user"]["name"], i["players"]["black"]["user"]["name"], i["lastMoveAt"]) for i in tournament_games]

# Sort the games based on time
games.sort()

# Initialize an empty DataFrame with columns: name, point, time
df = pd.DataFrame(columns=["name", "point", "time"])

# Process each game
for i in games:
    for j in players:
        if i.white == j.name:
            wp = j.sheet["scores"][j.counter]
            i.wp = wp
            j.point += int(wp)
            i.wpt += j.point
            j.point_list[i.wpt] = i.time
            j.counter -= 1
            # Append the new row to the DataFrame
            df = pd.concat([df, pd.DataFrame({"name": [j.name], "point": [i.wpt], "time": [i.time]})], ignore_index=True)
        
        if i.black == j.name:
            bp = j.sheet["scores"][j.counter]
            i.bp = bp
            j.point += int(bp)
            i.bpt += j.point
            j.point_list[i.bpt] = i.time
            j.counter -= 1
            # Append the new row to the DataFrame
            df = pd.concat([df, pd.DataFrame({"name": [j.name], "point": [i.bpt], "time": [i.time]})], ignore_index=True)
            
# Extracting start time and duration from the tournament 
start_time = tournament["startsAt"]
duration_minutes = tournament["minutes"]

# Set your desired interval in seconds (e.g., 60 for 1 minute, 30 for 30 seconds, 120 for 2 minutes)
interval_seconds = 60  

# Generate time intervals based on the specified interval
time_intervals = [start_time + timedelta(seconds=i * interval_seconds) for i in range((duration_minutes * 60) // interval_seconds + 1)]

df_points = pd.DataFrame(0, index=[p.name for p in players], columns=time_intervals)

# Iterate over each player
for player_obj in players:
    player_name = player_obj.name
    point_list = player_obj.point_list

    # Iterate through each time interval
    for time in time_intervals:
        
        # Find the closest time in the player's point_list that is less than or equal to the current interval
        closest_time = None
        for pt_time in sorted(point_list.values()):
            if pt_time <= time:
                closest_time = pt_time
            else:
                break
        
        # If a valid closest time is found, set the corresponding point in the DataFrame
        if closest_time is not None:
            df_points.at[player_name, time] = list(point_list.keys())[list(point_list.values()).index(closest_time)]
        else:
            df_points.at[player_name, time] = 0

# Check if it's a team tournament
if "teamBattle" in tournament:
    # Identify unique teams
    teams = list(set(player_obj.team for player_obj in players if player_obj.team is not None))
    
    # Initialize a DataFrame for teams, similar to the player-time DataFrame
    team_df = pd.DataFrame(0, index=teams, columns=df_points.columns)
    
    # Populate the Team DataFrame considering only the top 10 players by total points
    for team in teams:
        # Get player objects in this team
        team_players = [player_obj for player_obj in players if player_obj.team == team]
        
        # Sort players by their total points (sum of all points)
        sorted_players = sorted(team_players, key=lambda x: sum(x.point_list.keys()), reverse=True)
        
        # Select top 10 players (Lichess only sum up top 10 players in the team)
        top_10_players = sorted_players[:10]
        
        # Get the names of the top 10 players
        top_10_player_names = [player_obj.name for player_obj in top_10_players]
        
        # Sum the points for each time interval (column) for the top 10 players in the current team
        team_points = df_points.loc[top_10_player_names].sum(axis=0)
        
        # Assign the summed points to the team_df for this team
        team_df.loc[team] = team_points
    

# Change time format and strat from 00:00:00
df_points.columns = [(col - start_time).total_seconds() for col in df_points.columns]
df_points.columns = [str(timedelta(seconds=sec)) for sec in df_points.columns]

# Save the DataFrame as a CSV file 
df_points.to_csv('player_points.csv', index=True)
# Optionally, you can specify the path where you want to save the file
# df_points.to_csv('path/to/your/directory/player_points.csv', index=True)
print("DataFrame saved as 'player_points.csv'.")

if "teamBattle" in tournament:
    team_df.columns = df_points.columns  # Apply the same elapsed time formatting
    team_df.to_csv('team_points.csv', index=True)
    # Optionally, you can specify the path where you want to save the file
    # df_points.to_csv('path/to/your/directory/team_points.csv', index=True)
    print("Team DataFrame saved as 'team_points.csv'.")

