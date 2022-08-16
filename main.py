# imports
import spotipy
import os
import dotenv
import speech_recognition as sr
import orjson
import random
from spotipy.oauth2 import SpotifyOAuth
from rich import print
from methods import *
import asyncio
from src.initialize_speech import *


""" 
TODO(emoss): Fully implement asynchronized methods.
"""


# load environment variables
dotenv.load_dotenv()

# loading settings
with open('settings.json') as f:
    settings = orjson.loads(f.read())
presets = settings["presets"]
f.close()

# create spotify object with all scopes
scope = f"ugc-image-upload, user-read-playback-state, user-modify-playback-state, user-follow-modify, user-read-private, user-follow-read, user-library-modify, user-library-read, streaming, user-read-playback-position, app-remote-control, user-read-email, user-read-currently-playing, user-read-recently-played, playlist-modify-private, playlist-read-collaborative, playlist-read-private, user-top-read, playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"), redirect_uri="http://localhost:8888/callback"), requests_timeout=300)

# everyone likes ASCII art so why not
print(f'''[spring_green3]
:'######::'########:::'#######::'########:'####:'########:'##:::'##:
'##... ##: ##.... ##:'##.... ##:... ##..::. ##:: ##.....::. ##:'##::
 ##:::..:: ##:::: ##: ##:::: ##:::: ##::::: ##:: ##::::::::. ####:::
. ######:: ########:: ##:::: ##:::: ##::::: ##:: ######:::::. ##::::
:..... ##: ##.....::: ##:::: ##:::: ##::::: ##:: ##...::::::: ##::::
'##::: ##: ##:::::::: ##:::: ##:::: ##::::: ##:: ##:::::::::: ##::::
. ######:: ##::::::::. #######::::: ##::::'####: ##:::::::::: ##::::
:......:::..::::::::::.......::::::..:::::....::..:::::::::::..:::::
[/spring_green3]
[hot_pink2]Voice Control for Spotify[/hot_pink2]
''')

while True:
    '''
    infinite loop to listen for commands
    commands:
    - 'play {track name}'
    - 'album {album name}'
    - 'artist {artist name}'
    - 'skip track'
    - 'previous track'
    '''
    r = sr.Recognizer()
    command, audio = initialize_voice(recognizer=r)
    
    # recognize speech and using try-except to catch errors
    try:
        command = r.recognize_google(audio_data=audio).lower()
    except sr.UnknownValueError:
        print(f"[italic red]Could not understand.[/italic red]")
        continue
    
    print(f"[medium_purple3]{command}[/medium_purple3]")
    # splitting the command into separate words
    words = command.split()
    
    # checking if the speech recognizer recognized a command
    if len(words) < 1:
        print(f"[italic red]Could not understand.[/italic red]")
        continue
    elif len(words) == 1:
        for preset in presets:
            if words[0] == preset["preset"]:
                if preset["type"] == "track":
                    name = preset["name"]
                    uri = asyncio.run(get_track_uri(spotify=sp, name=name))
                    asyncio.run(play_track(spotify=sp, uri=uri))
                    print(f"[bold deep_sky_blue2]Playing track:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                    continue

                elif preset["type"] == "album":
                    name = preset["name"]
                    uri = asyncio.run(get_album_uri(spotify=sp, name=name))
                    asyncio.run(play_album(spotify=sp, uri=uri))
                    print(f"[bold deep_sky_blue2]Playing album:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                    continue
                
                elif preset["type"] == "artist":
                    name = preset["name"]
                    uri = asyncio.run(get_artist_uri(spotify=sp, name=name))
                    asyncio.run(play_artist(spotify=sp, uri=uri))
                    print(f"[bold deep_sky_blue2]Playing artist:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                    continue

                elif preset["type"] == "playlist":
                    playlists, playlist_ids = asyncio.run(get_user_playlists(spotify=sp))
                    name = preset["name"]
                    for i in range(len(playlists)):
                        if name.lower() == playlists[i].lower():
                            id = playlist_ids[i]
                            asyncio.run(play_playlist(spotify=sp, playlist_id=id))
                            print(f"[bold deep_sky_blue2]Playing playlist:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                    continue

        if words[0] == "next":
            asyncio.run(next_track(spotify=sp))
        elif words[0] == "pause":
            asyncio.run(pause_track(spotify=sp))
        elif words[0] == "resume":
            asyncio.run(resume_track(spotify=sp))
        elif words[0] == 'back':
            asyncio.run(play_previous_song(spotify=sp))
        elif words[0] == "quit":
            asyncio.run(exit_application())
            break
        elif words[0] == "repeat":
            asyncio.run(repeat_track(spotify=sp))
        else:
            print(f"[italic red]Command not recognized.[/italic red]")
            continue
    
    else:
        # here action is the command, eg: 'play', 'album' or 'artist'
        # and the name is the name of the track/album/artist to be played
        action = words[0]
        name = " ".join(words[1:])

        # Current command actions
        try:
            if action == "current":
                if name == "song":
                    """ Display the current song playing. """
                    track = asyncio.run(get_current_song(spotify=sp))
                    print(f"[bold deep_sky_blue2]Current track:[/bold deep_sky_blue2] [italic spring_green3]{track}[/italic spring_green3]")
        except Exception as action_exception:
            print(f"[italic red]Could not underst{action_exception}and.[/italic red]")
            
        # Go command actions
        try:
            if action == 'go':
                if name == 'back':
                    """ Go Back to previous song. """
                    asyncio.run(play_previous_song(spotify=sp))
        except Exception as e:
            print(f"[italic red]{e}[/italic red]")
            
        # try except block to catch InvaliSearchError
        try:
            if action == "play":
                if name == "random":
                    tracks = asyncio.run(get_user_saved_tracks(spotify=sp))
                    random_track = random.choice(tracks)
                    uri = asyncio.run(get_track_uri(spotify=sp, name=random_track))
                    asyncio.run(play_track(spotify=sp, uri=uri))
                    print(f"[bold deep_sky_blue2]Playing track:[/bold deep_sky_blue2] [italic spring_green3]{random_track}[/italic spring_green3]")
                else:
                    uri = asyncio.run(get_track_uri(spotify=sp, name=name))
                    asyncio.run(play_track(spotify=sp, uri=uri))
                    print(f"[bold deep_sky_blue2]Playing track:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")

            if action == "album":
                uri = asyncio.run(get_album_uri(spotify=sp, name=name))
                asyncio.run(play_album(spotify=sp, uri=uri))
                print(f"[bold deep_sky_blue2]Playing album:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
            
            if action == "artist":
                if name == "random":
                    random_artist = random.choice(get_user_followed_artists(spotify=sp))
                    uri = asyncio.run(get_artist_uri(spotify=sp, name=random_artist))
                    asyncio.run(play_artist(spotify=sp, uri=uri))
                    print(f"[bold deep_sky_blue2]Playing artist:[/bold deep_sky_blue2] [italic spring_green3]{random_artist}[/italic spring_green3]")
                else:
                    uri = asyncio.run(get_artist_uri(spotify=sp, name=name))
                    asyncio.run(play_artist(spotify=sp, uri=uri))
                    print(f"[bold deep_sky_blue2]Playing artist:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
            
            if action == "playlist":
                playlists, playlist_ids = asyncio.run(get_user_playlists(spotify=sp))
                if name.lower() in playlists:
                    for i in range(len(playlists)):
                        if name.lower() == playlists[i].lower():
                            id = playlist_ids[i]
                            asyncio.run(play_playlist(spotify=sp, playlist_id=id))
                            print(f"[bold deep_sky_blue2]Playing playlist:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                            break
                else:
                    print("[italic red]Could not find playlist.[/italic red]")
                    continue


            elif action == "volume":
                t = {'one':1,'two':2,'three':3,'four':4,'five':5,'six':6,'seven':7,'eight':8,'nine':9,'ten':10}  # dictionary for volume
                if name in t:
                    """ For some reason speech recognition return 1 - 10 as strings, so we need to convert them to ints."""
                    volume = t[name]
                    asyncio.run(change_volume(spotify=sp, volume=volume))
                    print(f"[bold deep_sky_blue2]Volume set to:[/bold deep_sky_blue2] [italic spring_green3]{volume}[/italic spring_green3]")
                else:
                    """ If volume is not in dictionary, tthen return it as is."""
                    volume = int(name)
                    asyncio.run(change_volume(spotify=sp, volume=volume))
                    print(f"[bold deep_sky_blue2]Volume set to:[/bold deep_sky_blue2] [italic spring_green3]{volume}%[/italic spring_green3]")
            
            elif action == "shuffle":
                state = name
                asyncio.run(shuffle(spotify=sp, state=state))

        except InvalidSearchError:
            print(f"[italic red]Could not find {name}. Try again.[/italic red]")

print("[bold deep_sky_blue2]Goodbye![/bold deep_sky_blue2]")