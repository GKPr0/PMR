import json
import re
from enum import Enum
from pathlib import Path

import speech_recognition as asr

from utils import resources


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


def generate_phn_files(source: str, encoding: str = "utf-8"):
    txt_files = list(Path(source).rglob("**/*.txt"))

    for txt_file in txt_files:
        with open(txt_file, mode="r", encoding=encoding) as txt_f:
            text = normalize_text(txt_f.read())

        phonem_text = g2p(text)
        phn_file = txt_file.with_suffix('.phn')
        with open(phn_file, mode="w", encoding=encoding) as phn_f:
            phn_f.writelines((f"-{phonem_text}-"))


def g2p(text, rule_file=resources["g2p_cz_mapping"]):
    text = normalize_text(text)

    with open(rule_file, mode="r", encoding="utf8") as f:
        rules = json.load(f)
        for rule in rules:
            in_seq = rule.get("in")
            out_seq = rule.get("out")
            context_before = rule.get("context_before", "")
            context_after = rule.get("context_after", "")

            text = re.sub(fr"({context_before})(?:{in_seq})({context_after})", fr"\1{out_seq}\2", text)

    return text


def normalize_text(text: str) -> str:
    return text.lower() \
        .replace("\n", " ")\
        .replace(".", "")\
        .replace(",", "")\
        .replace("?", "")\
        .replace("!", "")\
        .replace(":", "")\
        .replace(";", "")\
        .replace("(", "")\
        .replace(")", "")\
        .replace("-", "")\
        .replace("_", "")\
        .replace("=", "")\
        .replace("+", "")\
        .replace("*", "")\
        .replace("/", "")\
        .replace("\\", "")\
        .replace("\"", "")\
        .replace("'", "")\
        .replace("´", "")\
        .replace("`", "")\
        .replace("´", "")
