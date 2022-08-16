import speech_recognition as sr
from rich import print
from rich.console import Console
from rich.style import Style
from typing import Union

console = Console()
base_style = Style.parse("cyan")


def initialize_voice(recognizer: sr.Recognizer) -> Union[str, sr.AudioData]:
    command = None
    with sr.Microphone() as source:
        console.print(" ----- Calibrating microphone ----- ", style='bold magenta')
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        console.print("Calibration complete", style='bold green')
        console.print("[bold deep_sky_blue2]Ready![/bold deep_sky_blue2]")
        audio = recognizer.listen(source, 10, 3)  # Set timeouut of listener

    return command, audio