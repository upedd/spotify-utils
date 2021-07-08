# https://stackoverflow.com/a/1751478
def chunks(items, n):
    n = max(1, n)
    return (items[i:i + n] for i in range(0, len(items), n))


def get_id(item):
    return item["id"]


various_artist_id = "0LyfQWJT6nXafLPZqxe9Of"


def not_from_various_artists(album):
    for artist in album["artists"]:
        if artist["id"] == various_artist_id:
            return False
    return True


def artist_in_track_artists(artist_id, track):
    for artist in track["artists"]:
        if artist["id"] == artist_id:
            return True
    return False


def track_available_in_region(region, track):
    for market in track["available_markets"]:
        if market == region:
            return True
    return False


def prompt_yes_or_no(question):
    answer = input(question)
    if answer.lower() == "yes" or answer.lower() == "y":
        return True
    return False
