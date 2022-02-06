from rich import print
from spotipy import Spotify


# catching errors
class InvalidSearchError(Exception):
    pass

def get_album_uri(spotify: Spotify, name: str):
    '''
    returns the uri of the album with the given name
    '''
    results = spotify.search(q=name, type="album")
    if len(results["albums"]["items"]) == 0:
        raise InvalidSearchError(f"No albums found with name: {name}")
    return results["albums"]["items"][0]["uri"]
    
def get_track_uri(spotify: Spotify, name: str):
    '''
    returns the uri of the track with the given name
    '''
    results = spotify.search(q=name, type="track")
    if len(results["tracks"]["items"]) == 0:
        raise InvalidSearchError(f"No tracks found with name: {name}")
    return results["tracks"]["items"][0]["uri"]

def get_artist_uri(spotify: Spotify, name: str):
    '''
    returns the uri of the artist with the given name
    '''
    results = spotify.search(q=name, type="artist")
    if len(results["artists"]["items"]) == 0:
        raise InvalidSearchError(f"No artists found with name: {name}")
    return results["artists"]["items"][0]["uri"]

def play_album(spotify: Spotify, uri: str):
    '''
    plays the album with the given uri
    '''
    spotify.start_playback(context_uri=uri)

def play_track(spotify: Spotify, uri: str):
    '''
    plays the track with the given uri
    '''
    spotify.start_playback(uris=[uri])

def play_artist(spotify: Spotify, uri: str):
    '''
    plays the artist with the given uri
    '''
    spotify.start_playback(context_uri=uri)

def skip_track(spotify: Spotify):
    '''
    skips the current track
    '''
    spotify.next_track()

def previous_track(spotify: Spotify):
    '''
    plays the previous track
    '''
    spotify.previous_track()

def pause_track(spotify: Spotify):
    '''
    pauses the current track
    '''
    spotify.pause_playback()

def resume_track(spotify: Spotify):
    '''
    resumes the current track
    '''
    spotify.start_playback()    

def change_volume(spotify: Spotify, volume: int):
    '''
    changes the volume to the given value between 1 and 100
    '''
    if volume < 0 or volume > 100:
        raise ValueError("Volume must be between 0 and 100")
    else:    
        spotify.volume(volume)

def repeat_track(spotify: Spotify):
    '''
    repeats the current track
    '''
    spotify.repeat("track")

def shuffle(spotify: Spotify, state: str):
    '''
    shuffles the playlist
    '''
    if state == "on":
        spotify.shuffle(True)
        print("[bold deep_sky_blue2]Shuffle is[/bold deep_sky_blue2] [italic spring_green3]ON[/italic spring_green3]")
    
    elif state == "off":
        spotify.shuffle(False)
        print("[bold deep_sky_blue2]Shuffle is[/bold deep_sky_blue2] [italic spring_green3]OFF[/italic spring_green3]")
    
    else:
        raise ValueError("State must be either on or off")
    
def get_user_followed_artists(spotify: Spotify):
    '''
    returns a list of the users followed artists
    '''
    all_artists = []
    results = spotify.current_user_followed_artists(limit=20)
    for i in range(results["artists"]["total"]):
        for j in range(len(results["artists"]["items"])):
            all_artists.append(results["artists"]["items"][j]["name"])
        if results["artists"]["cursors"]["after"] == None:
            break
        else:
            after = results["artists"]["cursors"]["after"]
        results = spotify.current_user_followed_artists(limit=20, after=after)

    return all_artists