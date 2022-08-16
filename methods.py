from rich import print
from spotipy import Spotify


# catching errors
class InvalidSearchError(Exception):
    pass


async def exit_application() -> None:
    """
    exits the application
    """
    print("[bold deep_sky_blue2]Goodbye![/bold deep_sky_blue2]")
    return exit()


async def get_current_song(spotify: Spotify) -> str:
    """
    Returns the name of the current song.
    """
    if spotify.currently_playing() is None:
        """ If there is no song playing, return nothing is playing. """
        return "Nothing is playing"
    song_name = spotify.currently_playing()['item']['name']
    artist_name = spotify.currently_playing()['item']['artists'][0]['name']
    return f"{song_name} - {artist_name}"


async def play_previous_song(spotify: Spotify) -> Spotify:
    """
    returns the previous song
    """
    print(f"[bold deep_sky_blue2]Playing previous song![/bold deep_sky_blue2]")
    return spotify.previous_track()


async def get_album_uri(spotify: Spotify, name: str) -> str:
    """
    returns the uri of the album with the given name
    """
    results = spotify.search(q=name, type="album")
    if len(results["albums"]["items"]) == 0:
        raise InvalidSearchError(f"No albums found with name: {name}")
    return results["albums"]["items"][0]["uri"]


async def get_track_uri(spotify: Spotify, name: str) -> str:
    """
    returns the uri of the track with the given name
    """
    results = spotify.search(q=name, type="track")
    if len(results["tracks"]["items"]) == 0:
        raise InvalidSearchError(f"No tracks found with name: {name}")
    return results["tracks"]["items"][0]["uri"]


async def get_artist_uri(spotify: Spotify, name: str) -> str:
    """
    returns the uri of the artist with the given name
    """
    results = spotify.search(q=name, type="artist")
    if len(results["artists"]["items"]) == 0:
        raise InvalidSearchError(f"No artists found with name: {name}")
    return results["artists"]["items"][0]["uri"]


async def play_album(spotify: Spotify, uri: str) -> Spotify:
    """
    plays the album with the given uri
    """
    return spotify.start_playback(context_uri=uri)


async def play_track(spotify: Spotify, uri: str) -> Spotify:
    """
    plays the track with the given uri
    """
    return spotify.start_playback(uris=[uri])


async def play_artist(spotify: Spotify, uri: str) -> Spotify:
    """
    plays the artist with the given uri
    """
    return spotify.start_playback(context_uri=uri)


async def play_playlist(spotify: Spotify, playlist_id: str) -> Spotify:
    """
    plays the playlist with the given id
    """
    return spotify.start_playback(context_uri=f"spotify:playlist:{playlist_id}")


async def next_track(spotify: Spotify) -> Spotify:
    """
    skips the current track
    """
    print(f"[bold deep_sky_blue2]Skipped![/bold deep_sky_blue2]")
    return spotify.next_track()


async def pause_track(spotify: Spotify) -> Spotify:
    """
    Puases the current song playing.
    """
    try:
        if spotify.current_user_playing_track()['is_playing'] is True:
            """ If the song is playing pause it."""
            print(f"[bold deep_sky_blue2]Paused![/bold deep_sky_blue2]")
            return spotify.pause_playback()
        else:
            """ Otherwise, inform the user that no song is currently playing."""
            print(f"[italic red]No song is currently playing.[/italic red]")
    except Exception as pause_tracK_exception:
        print(f"Error"+ str(pause_tracK_exception))


async def resume_track(spotify: Spotify) -> Spotify:
    """
    Resumes the paused song.
    """
    try:
        if spotify.current_user_playing_track()['is_playing'] is False:
            """ If the song is paused, resume it."""
            print(f"[bold deep_sky_blue2]Resumed![/bold deep_sky_blue2]")
            return spotify.start_playback()
        else:
            """ Otherwise, inform the user that song is currently playing."""
            print(f"[italic red]Song is already playing.[/italic red]")
    except Exception as resume_track_exception:
        print(f"Error"+ str(resume_track_exception))


async def change_volume(spotify: Spotify, volume: int) -> Spotify:
    """
    changes the volume to the given value between 1 and 100
    """
    if volume < 0 or volume > 100:
        """ Removed the raise exception to allow the user to continue using the application. """
        print(f"[italic red]Volume must be between 1 and 100.[/italic red]")
    else:
        return spotify.volume(volume)


async def repeat_track(spotify: Spotify) -> Spotify:
    """
    repeats the current track
    """
    try:
        print(f"[bold deep_sky_blue2]Track on repeat![/bold deep_sky_blue2]")
        return spotify.repeat("track")
    except Exception as repeat_track_exception:
        print(f"Error"+ str(repeat_track_exception))


async def shuffle(spotify: Spotify, state: str) -> Spotify:
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


async def get_user_followed_artists(spotify: Spotify) -> list:
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


async def get_user_saved_tracks(spotify: Spotify) -> list:
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


async def get_user_playlists(spotify: Spotify) -> tuple[list, list]:
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
