# lcan
lcan (Lichess Tournament Animation), python visualization tool for lichess tournaments.  
Supported by [Berserk](https://github.com/lichess-org/berserk) (Python client for the lichess API)  
It is named as the reverse of "Naci" and is intended to honor M. Naci Dokumacı for his dedicated contributions to the chess community.  
"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" ***Mustafa Naci Dokumacı***
## Usage
### API
Get a Personal API access token. **Edit profile** > **API access tokens**  
Copy the token. Paste into ```session = berserk.TokenSession("Token")```
### Tournament
Copy the link of the tournament. Paste into ```client.tournaments.stream_results("Link",sheet=True)```
