# lcan
lcan (Lichess Tournament Animation), python visualization tool for lichess tournaments.  
Supported by [Berserk](https://github.com/lichess-org/berserk) (Python client for the lichess API)  
It is named as the reverse of "Naci" and is intended to honor M. Naci Dokumacı for his dedicated contributions to the chess community.  
## Usage
### API (Optional)
Get a Personal API access token. **Edit profile** > **API access tokens**  
Copy the token. Paste into ```token="Paste the Token"```
### Tournament
Copy the link of the tournament. Paste into ```client.tournaments.stream_results("Paste the Link",sheet=True)```
### CSV File
Players' points over time is saved as "player_points.csv". If the tournament is a team tournament "team_points.csv" saved as well   
[Flourish](https://app.flourish.studio) can be used. Choose bar chart race and upload the csv file
