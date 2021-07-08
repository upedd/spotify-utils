# Spotify utils
Various python scripts for spotify automation 
## Setup
### 1. Requirements
- Spotify account
- Python 3 with pip installed 
- Git installed
### 2. Create spotify application
1. Go to [Spotify Developers Dashboard](https://developer.spotify.com/dashboard) and login to your spotify account.
2. Create new application or use existing one.
3. Add `http://localhost:8080` (or any URL you want) as a redirect URI.
### 3. Download and install dependencies 
```bash
git clone https://github.com/upedd/spotify-utils
pip install -r requirements.txt
```
### 4. Set environment variables 
- `SPOTIPY_CLIENT_ID` - client id of your spotify application
- `SPOTIPY_CLIENT_SECRET`- client secret of your spotify application
- `SPOTIPY_REDIRECT_URI` - redirect URI of your spotify application
## Usage
### Artist Playlist (artist_playlist.py)
Creates playlist with tracks from given artist albums.
```
usage: artist_playlist.py [-h] [-i ID] [-v {public,private}] [-a] [-m]
                          [-r REGION] [-d]
                          playlist_name

positional arguments:
  playlist_name         name of generated playlist

optional arguments:
  -h, --help            show this help message and exit
  -i ID, --id ID        artist id
  -v {public,private}, --visibility {public,private}
                        playlist visibility (default: private)
  -a, --appearances     include appearances in other artists albums
  -m, --mentioned       include only tracks that given artist is mentioned as
                        track artist
  -r REGION, --region REGION
                        include only tracks that are playable in this region
                        (f.e. "PL")
  -d, --deduplicate     remove duplicates based on title
```
##### Example:
```
$ python artist_playlist.py test -i 1Xyo4u8uXC1ZmMpatF05PJ -a -m -r PL
=== Spotify playlist creation helper by uped (https://github.com/upedd) ===
Fetched 361 albums...
Fetched 2450 tracks...
Got 591 tracks in which given artist is mentioned in track artists...
Got 320 tracks which are playable in given region (PL)...
Created playlist "test" https://open.spotify.com/playlist/1L6NRrtxxPFOUqypVygSg6...
Added all tracks to playlist...
Execution completed in 6.02 seconds.
```
#### Interactive mode
If `--id` argument is missing script will run in interactive mode which helps you with specifying options and allows you to search for an artist.
##### Example of interactive mode:
```
$ python artist_playlist.py test
=== Spotify playlist creation helper by uped (https://github.com/upedd) ===
Running in interactive mode! You can skip this by specifying "--id" argument
Do you have an artist id? (y/N): n
Enter an artist name: weekend
1. The Weeknd (https://open.spotify.com/artist/1Xyo4u8uXC1ZmMpatF05PJ)
2. Weekend (https://open.spotify.com/artist/4jPwc1E9EXPQbryc1YKbjl)
[...]
Enter a index of artist you want to select: 1
Artist ID: 1Xyo4u8uXC1ZmMpatF05PJ
Do you want to make your playlist public? (y/N): n
Include appearances in other artists albums? (y/N): y
Include only tracks that given artist is mentioned as track artist? (y/N): y
Include only tracks that are playable in specified region? (y/N): y
Enter that region (f.e "PL"): PL
Remove duplicates based on title? (y/N): n
Fetched 361 albums...
Fetched 2450 tracks...
Got 591 tracks in which given artist is mentioned in track artists...
Got 320 tracks which are playable in given region (PL)...
Created playlist "test" https://open.spotify.com/playlist/{id}...
Added all tracks to playlist...
Execution completed in 4.8 seconds.
```
## Authors
- [uped](https://www.github.com/upedd)
## License
[MIT](https://choosealicense.com/licenses/mit/)