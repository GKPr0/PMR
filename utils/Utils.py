from enum import Enum
import speech_recognition as asr


class LanguageCodes(str, Enum):
    Czech = "cs-CZ"
    Danish = "da-DK"
    Slovak = "sk-SK"
    Japanese = "ja-JP"
    Norwegian = "nb-NO"
    Dutch = "nl-NL"
    Polish = "pl-PL"
    Swedish = "sv-SE"
    Finnish = "fi-FI"
    German = "de-DE"


def speech_2_text(audio_file: str,
                    language_code: LanguageCodes,
                    duration: float = None,
                    offset: float = None) -> str:
    recognizer = asr.Recognizer()
    with asr.AudioFile(audio_file) as source:
        audio = recognizer.record(source, duration, offset)

        text = recognizer.recognize_google(audio, language=language_code.value)

    return text