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
