from rich import print
from spotipy import Spotify


# catching errors
class InvalidSearchError(Exception):
    pass


def get_album_uri(spotify: Spotify, name: str) -> str:
    """
    returns the uri of the album with the given name
    """
    results = spotify.search(q=name, type="album")
    if len(results["albums"]["items"]) == 0:
        raise InvalidSearchError(f"No albums found with name: {name}")
    return results["albums"]["items"][0]["uri"]


def get_track_uri(spotify: Spotify, name: str):
    """
    returns the uri of the track with the given name
    """
    results = spotify.search(q=name, type="track")
    if len(results["tracks"]["items"]) == 0:
        raise InvalidSearchError(f"No tracks found with name: {name}")
    return results["tracks"]["items"][0]["uri"]


def get_artist_uri(spotify: Spotify, name: str):
    """
    returns the uri of the artist with the given name
    """
    results = spotify.search(q=name, type="artist")
    if len(results["artists"]["items"]) == 0:
        raise InvalidSearchError(f"No artists found with name: {name}")
    return results["artists"]["items"][0]["uri"]


def play_album(spotify: Spotify, uri: str) -> Spotify:
    """
    plays the album with the given uri
    """
    return spotify.start_playback(context_uri=uri)


def play_track(spotify: Spotify, uri: str) -> Spotify:
    """
    plays the track with the given uri
    """
    return spotify.start_playback(uris=[uri])


def play_artist(spotify: Spotify, uri: str) -> Spotify:
    """
    plays the artist with the given uri
    """
    return spotify.start_playback(context_uri=uri)


def play_playlist(spotify: Spotify, playlist_id: str) -> Spotify:
    """
    plays the playlist with the given id
    """
    return spotify.start_playback(context_uri=f"spotify:playlist:{playlist_id}")


def skip_track(spotify: Spotify) -> Spotify:
    """
    skips the current track
    """
    return spotify.next_track()


def previous_track(spotify: Spotify) -> Spotify:
    """
    plays the previous track
    """
    return spotify.previous_track()


def pause_track(spotify: Spotify) -> Spotify:
    """
    pauses the current track
    """
    return spotify.pause_playback()


def resume_track(spotify: Spotify) -> Spotify:
    """
    resumes the current track
    """
    return spotify.start_playback()


def change_volume(spotify: Spotify, volume: int) -> Spotify:
    """
    changes the volume to the given value between 1 and 100
    """
    if volume < 0 or volume > 100:
        raise ValueError("Volume must be between 0 and 100")
    else:
        return spotify.volume(volume)


def repeat_track(spotify: Spotify) -> Spotify:
    """
    repeats the current track
    """
    return spotify.repeat("track")


def shuffle(spotify: Spotify, state: str):
    """
    shuffles the playlist
    """
    if state == "on":
        print(f"[bold deep_sky_blue2]Shuffle is[/bold deep_sky_blue2] [italic spring_green3]ON[/italic spring_green3]")
        return spotify.shuffle(True)
    elif state == "off":
        print(f"[bold deep_sky_blue2]Shuffle is[/bold deep_sky_blue2] [italic spring_green3]OFF[/italic spring_green3]")
        return spotify.shuffle(False)
    else:
        raise ValueError("State must be either on or off")


def get_user_followed_artists(spotify: Spotify) -> list:
    """
    returns a list of the users followed artists
    """
    all_artists = []
    results = spotify.current_user_followed_artists(limit=20)
    for i in range(results["artists"]["total"]):
        for j in range(len(results["artists"]["items"])):
            all_artists.append(results["artists"]["items"][j]["name"])
        if results["artists"]["cursors"]["after"] is None:
            break
        else:
            after = results["artists"]["cursors"]["after"]
        results = spotify.current_user_followed_artists(limit=20, after=after)

    return all_artists


def get_user_saved_tracks(spotify: Spotify) -> list:
    """
    returns a list of the users saved tracks
    """
    tracks = []
    offset = 0
    results = spotify.current_user_saved_tracks(limit=50, offset=offset)
    while len(results["items"]) != 0:
        for i in range(len(results["items"])):
            tracks.append(results["items"][i]["track"]["name"])
        offset += 50
        results = spotify.current_user_saved_tracks(limit=50, offset=offset)

    return tracks


def get_user_playlists(spotify: Spotify) -> tuple[list, list]:
    """
    returns a list of the users playlists
    """
    playlists = []
    playlist_ids = []
    offset = 0
    results = spotify.current_user_playlists(limit=50, offset=offset)
    while len(results["items"]) != 0:
        for i in range(len(results["items"])):
            playlists.append(results["items"][i]["name"])
            playlist_ids.append(results["items"][i]["id"])
        offset += 50
        results = spotify.current_user_playlists(limit=50, offset=offset)

    return playlists, playlist_ids
