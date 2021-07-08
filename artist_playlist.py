import argparse
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from util import not_from_various_artists, get_id, chunks, artist_in_track_artists, track_available_in_region, \
    prompt_yes_or_no

scope = "user-library-read playlist-modify-private playlist-modify-public"


def get_all_artist_albums(artist_id, include_appearances):
    album_type = "album,single"
    if include_appearances:
        album_type += ",appears_on"

    last_albums = sp.artist_albums(artist_id=artist_id, limit=50, album_type=album_type)
    artist_albums = []
    while last_albums is not None:
        artist_albums.extend(last_albums["items"])
        next_results = sp.next(last_albums)
        last_albums = next_results
    return artist_albums


def get_all_tracks_from_albums(albums_in):
    # We filter out various artist albums as they litter valid results
    filtered_albums = filter(not_from_various_artists, albums_in)
    album_ids = map(get_id, filtered_albums)
    # We need to split it into chunks of 20 as it's maximum number we can request at once
    album_ids_chunks = chunks(list(album_ids), 20)

    albums_tracks = []
    for album_id_chunk in album_ids_chunks:
        albums_response = sp.albums(album_id_chunk)
        for album in albums_response["albums"]:
            for track in album["tracks"]["items"]:
                albums_tracks.append(track)
    return albums_tracks


def add_tracks_to_playlist(playlist_in, tracks_in):
    playlist_id = playlist_in["id"]
    tracks_ids = map(get_id, tracks_in)
    # We need to split it into chunks of 100 as it's maximum number we can request at once
    tracks_ids_chunks = chunks(list(tracks_ids), 100)

    for track_id_chunk in tracks_ids_chunks:
        sp.playlist_add_items(playlist_id, track_id_chunk)


def create_playlist(name, visibility):
    return sp.user_playlist_create(user=sp.me()["id"], name=name, public=visibility == "public")


def deduplicate_tracks(tracks_in):
    track_names = set()
    tracks_out = []
    for track in tracks_in:
        if track["name"] not in track_names:
            track_names.add(track["name"])
            tracks_out.append(track)
    return tracks_out


def create_artist_playlist(playlist_name, artist_id, visibility, appearances, mentioned, region, deduplicate):
    start_time = time.perf_counter()

    albums = get_all_artist_albums(artist_id, appearances)
    print(f"Fetched {len(albums)} albums...")
    tracks = get_all_tracks_from_albums(albums)
    print(f"Fetched {len(tracks)} tracks...")
    if mentioned:
        tracks = list(
            filter(
                lambda track: artist_in_track_artists(artist_id, track),
                tracks
            )
        )
        print(f"Got {len(tracks)} tracks in which given artist is mentioned in track artists...")

    if region:
        tracks = list(
            filter(
                lambda track: track_available_in_region(region, track),
                tracks
            )
        )
        print(f"Got {len(tracks)} tracks which are playable in given region ({region})...")

    if deduplicate:
        tracks = deduplicate_tracks(tracks)
        print(f"Got {len(tracks)} tracks which are aren't duplicates...")
    playlist = create_playlist(playlist_name, visibility)
    print(f'Created playlist "{playlist["name"]}" {playlist["external_urls"]["spotify"]}...')
    add_tracks_to_playlist(playlist, tracks)
    print(f'Added all tracks to playlist...')
    print(f'Execution completed in {round(time.perf_counter() - start_time, 2)} seconds.')


def interactive_search_query():
    query = input("Enter an artist name: ")
    search_results = sp.search(query, type="artist")
    artists = search_results["artists"]["items"]
    for i, artist in enumerate(artists):
        print(f'{i + 1}. {artist["name"]} ({artist["external_urls"]["spotify"]})')
    artist_index = input("Enter a index of artist you want to select: ")
    return artists[int(artist_index) - 1]["id"]


def run_interactive(playlist_name):
    print("Running in interactive mode! You can skip this by specifying \"--id\" argument")
    # Artist id
    has_artist_id = input("Do you have an artist id? (y/N): ")
    if has_artist_id.lower() == "yes" or has_artist_id.lower() == "y":
        artist_id = input("Enter an artist id: ")
    else:
        artist_id = interactive_search_query()
    print(f"Artist ID: {artist_id}")
    # Visibility
    visibility = "private"
    if prompt_yes_or_no("Do you want to make your playlist public? (y/N): "):
        visibility = "public"
    # Appearances
    appearances = prompt_yes_or_no("Include appearances in other artists albums? (y/N): ")
    # Mentioned
    mentioned = prompt_yes_or_no("Include only tracks that given artist is mentioned as track artist? (y/N): ")
    # Region
    has_region = prompt_yes_or_no("Include only tracks that are playable in specified region? (y/N): ")
    region = None
    if has_region:
        region = input("Enter that region (f.e \"PL\"): ")
    # Deduplicate
    deduplicate = prompt_yes_or_no("Remove duplicates based on title? (y/N): ")

    create_artist_playlist(playlist_name, artist_id, visibility, appearances, mentioned, region, deduplicate)


if __name__ == '__main__':
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    parser = argparse.ArgumentParser()
    parser.add_argument("playlist_name", help="name of generated playlist")
    parser.add_argument("-i", "--id", help="artist id")
    parser.add_argument("-v", "--visibility",
                        help="playlist visibility (default: private)",
                        choices=["public", "private"],
                        default="private")
    parser.add_argument("-a", "--appearances",
                        help="include appearances in other artists albums",
                        action="store_true")
    parser.add_argument("-m", "--mentioned",
                        help="include only tracks that given artist is mentioned as track artist",
                        action="store_true")
    parser.add_argument("-r", "--region", help="include only tracks that are playable in this region (f.e. \"PL\")")
    parser.add_argument("-d", "--deduplicate",
                        help="remove duplicates based on title",
                        action="store_true")
    args = parser.parse_args()

    print("=== Spotify playlist creation helper by uped (https://github.com/upedd) ===")
    if args.id:
        create_artist_playlist(args.playlist_name, args.id, args.visibility, args.appearances, args.mentioned,
                               args.region, args.deduplicate)
    else:
        run_interactive(args.playlist_name)
