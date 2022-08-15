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

    # set-up speech recognizer
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("[bold deep_sky_blue2]Ready![/bold deep_sky_blue2]")
        audio = r.listen(source)

    command = None
    # recognize speech and using try-except to catch errors
    try:
        command = r.recognize_google(audio_data=audio).lower()
    except sr.UnknownValueError:
        print("[italic red]Could not understand.[/italic red]")
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
                    uri = get_track_uri(spotify=sp, name=name)
                    play_track(spotify=sp, uri=uri)
                    print(f"[bold deep_sky_blue2]Playing track:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                    continue

                elif preset["type"] == "album":
                    name = preset["name"]
                    uri = get_album_uri(spotify=sp, name=name)
                    play_album(spotify=sp, uri=uri)
                    print(f"[bold deep_sky_blue2]Playing album:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                    continue
                
                elif preset["type"] == "artist":
                    name = preset["name"]
                    uri = get_artist_uri(spotify=sp, name=name)
                    play_artist(spotify=sp, uri=uri)
                    print(f"[bold deep_sky_blue2]Playing artist:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                    continue

                elif preset["type"] == "playlist":
                    playlists, playlist_ids = get_user_playlists(spotify=sp)
                    name = preset["name"]
                    for i in range(len(playlists)):
                        if name.lower() == playlists[i].lower():
                            id = playlist_ids[i]
                            play_playlist(spotify=sp, playlist_id=id)
                            print(f"[bold deep_sky_blue2]Playing playlist:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                    continue

        if words[0] == "skip":
            skip_track(spotify=sp)
            print(f"[bold deep_sky_blue2]Skipped![/bold deep_sky_blue2]")
        
        elif words[0] == "pause":
            pause_track(spotify=sp)
            print(f"[bold deep_sky_blue2]Paused![/bold deep_sky_blue2]")

        elif words[0] == "resume":
            resume_track(spotify=sp)
            print(f"[bold deep_sky_blue2]Resumed![/bold deep_sky_blue2]")

        elif words[0] == "quit":
            pause_track(spotify=sp)
            break
        
        elif words[0] == "repeat":
            repeat_track(spotify=sp)
            print(f"[bold deep_sky_blue2]Track on repeat![/bold deep_sky_blue2]")

        else:
            print(f"[italic red]Could not understand.[/italic red]")
            continue
    
    else:
        # here action is the command, eg: 'play', 'album' or 'artist'
        # and the name is the name of the track/album/artist to be played
        action = words[0]
        name = " ".join(words[1:])

        # try except block to catch InvaliSearchError
        try:
            if action == "play":
                if name == "random":
                    tracks = get_user_saved_tracks(spotify=sp)
                    random_track = random.choice(tracks)
                    uri = get_track_uri(spotify=sp, name=random_track)
                    play_track(spotify=sp, uri=uri)
                    print(f"[bold deep_sky_blue2]Playing track:[/bold deep_sky_blue2] [italic spring_green3]{random_track}[/italic spring_green3]")

                else:
                    uri = get_track_uri(spotify=sp, name=name)
                    play_track(spotify=sp, uri=uri)
                    print(f"[bold deep_sky_blue2]Playing track:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")

            elif action == "album":
                uri = get_album_uri(spotify=sp, name=name)
                play_album(spotify=sp, uri=uri)
                print(f"[bold deep_sky_blue2]Playing album:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
            
            elif action == "artist":
                if name == "random":
                    random_artist = random.choice(get_user_followed_artists(spotify=sp))
                    uri = get_artist_uri(spotify=sp, name=random_artist)
                    play_artist(spotify=sp, uri=uri)
                    print(f"[bold deep_sky_blue2]Playing artist:[/bold deep_sky_blue2] [italic spring_green3]{random_artist}[/italic spring_green3]")

                else:
                    uri = get_artist_uri(spotify=sp, name=name)
                    play_artist(spotify=sp, uri=uri)
                    print(f"[bold deep_sky_blue2]Playing artist:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
            
            elif action == "playlist":
                playlists, playlist_ids = get_user_playlists(spotify=sp)
                if name.lower() in playlists:
                    for i in range(len(playlists)):
                        if name.lower() == playlists[i].lower():
                            id = playlist_ids[i]
                            play_playlist(spotify=sp, playlist_id=id)
                            print(f"[bold deep_sky_blue2]Playing playlist:[/bold deep_sky_blue2] [italic spring_green3]{name}[/italic spring_green3]")
                            break
                else:
                    print("[italic red]Could not find playlist.[/italic red]")
                    continue


            elif action == "volume":
                volume = int(name)
                change_volume(spotify=sp, volume=volume)
                print(f"[bold deep_sky_blue2]Volume set to:[/bold deep_sky_blue2] [italic spring_green3]{volume}%[/italic spring_green3]")
            
            elif action == "shuffle":
                state = name
                shuffle(spotify=sp, state=state)

        except InvalidSearchError:
            print(f"[italic red]Could not find {name}. Try again.[/italic red]")

print("[bold deep_sky_blue2]Goodbye![/bold deep_sky_blue2]")