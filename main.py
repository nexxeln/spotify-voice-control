# imports
import spotipy
import os
import dotenv
import speech_recognition as sr
from spotipy.oauth2 import SpotifyOAuth
from rich import print
from methods import *


# load environment variables
dotenv.load_dotenv()


# create spotify object with all scopes
scope = "ugc-image-upload, user-read-playback-state, user-modify-playback-state, user-follow-modify, user-read-private, user-follow-read, user-library-modify, user-library-read, streaming, user-read-playback-position, app-remote-control, user-read-email, user-read-currently-playing, user-read-recently-played, playlist-modify-private, playlist-read-collaborative, playlist-read-private, user-top-read, playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=os.getenv("SPOTIFY_CLIENT_ID"), client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"), redirect_uri="http://localhost:8888/callback"), requests_timeout=300)

# everyone likes ASCII art so why not
print('''[spring_green3]
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
        print("[italic red]Could not understand.[/italic red]")
        continue

    elif len(words) == 1:
        if words[0] == "skip":
            skip_track(spotify=sp)
            print("[bold deep_sky_blue2]Skipped![/bold deep_sky_blue2]")

        elif words[0] == "previous":
            previous_track(spotify=sp)
            print("[bold deep_sky_blue2]Playing previous track![/bold deep_sky_blue2]")
        
        elif words[0] == "pause":
            pause_track(spotify=sp)
            print("[bold deep_sky_blue2]Paused![/bold deep_sky_blue2]")

        elif words[0] == "resume":
            resume_track(spotify=sp)
            print("[bold deep_sky_blue2]Resumed![/bold deep_sky_blue2]")

        elif words[0] == "quit":
            print("[bold deep_sky_blue2]Quitting![/bold deep_sky_blue2]")
            break

        else:
            print("[italic red]Could not understand.[/italic red]")
            continue
    
    else:
        # here action is the command, eg: 'play', 'album' or 'artist'
        # and the name is the name of the track/album/artist to be played
        action = words[0]
        name = " ".join(words[1:])

        # try except block to catch InvaliSearchError
        try:
            if action == "play":
                uri = get_track_uri(spotify=sp, name=name)
                play_track(spotify=sp, uri=uri)
                print(f"[bold deep_sky_blue2]Playing track:[/bold deep_sky_blue2] [italic spring_green3]{name}...[/italic spring_green3]")

            elif action == "album":
                uri = get_album_uri(spotify=sp, name=name)
                play_album(spotify=sp, uri=uri)
                print(f"[bold deep_sky_blue2]Playing album:[/bold deep_sky_blue2] [italic spring_green3]{name}...[/italic spring_green3]")
            
            elif action == "artist":
                uri = get_artist_uri(spotify=sp, name=name)
                play_artist(spotify=sp, uri=uri)
                print(f"[bold deep_sky_blue2]Playing artist:[/bold deep_sky_blue2] [italic spring_green3]{name}...[/italic spring_green3]")
            
            elif action == "skip":
                skip_track(spotify=sp)
                print("[italic orange1]Skipped current track...[/italic orange1]")
            
            elif action == "previous":
                previous_track(spotify=sp)
                print("[italic orange1]Playing previous track...[/italic orange1]")

        except InvalidSearchError:
            print(f"[italic red]Could not find {name}. Try again.[/italic red]")

print("[bold deep_sky_blue2]Goodbye![/bold deep_sky_blue2]")