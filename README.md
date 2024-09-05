# lcan
lcan (Lichess Tournament Animation), python visualization tool for lichess tournaments.  
Supported by [Berserk](https://github.com/lichess-org/berserk) (Python client for the lichess API)  
It is named as the reverse of "Naci" and is intended to honor M. Naci Dokumacı for his dedicated contributions to the chess community.  
## Usage
### Berserk
Requires Python 3.8+   
Download and install the latest release:
```pip3 install berserk"```
If you have berserk-downstream installed, make sure to uninstall it first!   
**Change the stream_result() fuction!** (It will be changed in the next berserk version)    
```__init__.py - berserk``` >``` __init__.py - client``` > ```tournaments.py```   
Paste ```tournaments.py``` in this repository 
### API (Optional)
API token can be used for faster data stream
Get a Personal API access token. **Edit profile** > **API access tokens**  
Copy the token. Paste into ```token="Paste the Token"```   
If you do not have a token just leave as ```token=""``` 
### Tournament
Copy the link of the tournament. Paste into ```client.tournaments.stream_results("Paste the Link",sheet=True)```
### CSV File
Players' points over time is saved as "player_points.csv". If the tournament is a team tournament "team_points.csv" saved as well   
[Flourish](https://app.flourish.studio) can be used. Choose bar chart race and upload the csv file
